from django.core.mail import send_mail


def send_email(request, post, form_data):

    post_url = request.build_absolute_uri(post.get_absolute_url())
    subject = f"{form_data.get('name')} recommends to read post: {post.title}"
    message = f"Read {post.title} at {post_url} \nComments by {form_data.get('name')}: {form_data.get('comments')}"
    return send_mail(subject, message, from_email=form_data.get('email'), recipient_list=[
        form_data.get('receiver_email')])
