from datetime import timedelta
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from .models import Action


def create_action(user, details, target=None):
    """
    Create a generic Action for given user, with details to the target object
    :param user: performer of the action
    :param details: details about the action
    :param target: target object on which action is performed
    :return: (Bool) True if entry is saved
    """

    # Avoid adding duplicate action within 1 minute
    now = timezone.now()
    last_minute = now - timedelta(minutes=1)
    similar_actions = Action.objects.filter(user_id=user.id, details=details, created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_tc=target_ct, target_id=target.id)
    if not similar_actions:
        action = Action(user=user, details=details, target=target)
        action.save()
    return similar_actions is None
