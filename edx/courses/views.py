from django.apps import apps
from django.db.models import Count
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import redirect, get_object_or_404
from django.forms.models import modelform_factory

from braces.views import CsrfExemptMixin, JSONRequestResponseMixin

from .forms import ModuleFormSet
from .models import Course, Module, Content, Subject
from .mixins import AuthorCourseMixin, AuthorCourseEditMixin
from edx.student.views import CourseEnrollForm
from edx.common.utils import get_item_from_cache, set_item_in_cache
from edx.common.constants import KEY_ALL_COURSES


class ManageCourseListView(AuthorCourseMixin, ListView):
    permission_required = 'courses.view_course'
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(AuthorCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(AuthorCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(AuthorCourseEditMixin, DeleteView):
    permission_required = 'courses.delete_course'
    template_name = 'courses/manage/course/delete.html'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, author=request.user)

        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({
            'course': self.course, 'formset': formset
        })

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('edx:courses:manage_course_list')
        return self.render_to_response({
            'course': self.course, 'formset': formset
        })


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['file', 'video', 'image', 'text']:
            return apps.get_model(app_label='courses', model_name=model_name)

        return None

    def get_form(self, model, *args, **kwargs):
        form = modelform_factory(model, exclude=['author', 'order', 'created', 'updated'])
        return form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):

        self.module = get_object_or_404(Module, id=module_id, course__author=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, author=request.user)

        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, model_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({
            'form': form, 'object': self.obj, 'name': self.model.__name__
        })

    def post(self, request, model_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)

            return redirect('edx:courses:module_content_list', self.module.id)

        return self.render_to_response({
            'form': form, 'object': self.obj
        })


class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__author=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('edx:courses:module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__author=request.user)
        return self.render_to_response({
            'module': module
        })


class ModuleOrderView(CsrfExemptMixin, JSONRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__author=request.user).update(order=order)
        return self.render_json_response({'saved': 'ok'})


class ContentOrderView(CsrfExemptMixin, JSONRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__author=request.user).update(order=order)
        return self.render_json_response({'saved': 'ok'})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):

        subjects = get_item_from_cache(KEY_ALL_COURSES)

        if not subjects:
            subjects = Subject.objects.annotate(
                total_courses=Count('courses')
            )
            set_item_in_cache(KEY_ALL_COURSES, subjects)
        courses = Course.objects.annotate(
            total_modules=Count('modules')
        )
        all_courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            subject_key = f'subject_{subject.id}_courses'
            courses = get_item_from_cache(subject_key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                set_item_in_cache(subject_key, courses)
            else:
                courses = get_item_from_cache(KEY_ALL_COURSES)
                courses = all_courses
                set_item_in_cache(KEY_ALL_COURSES, all_courses)
        return self.render_to_response({
            'subjects': subjects, 'courses': courses, 'subject': subject
        })


class CourseDetailsView(DetailView):
    model = Course
    template_name = 'courses/course/details.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailsView, self).get_context_data(**kwargs)
        context['enrolment_form'] = CourseEnrollForm(initial={'course': self.object})
        return context
