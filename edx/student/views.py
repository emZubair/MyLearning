from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = 'edx:student:student_course_list'

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd.get('username'), password=cd.get('password'))
        login(self.request, user)
        return result
