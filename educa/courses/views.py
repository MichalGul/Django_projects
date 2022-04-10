from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet

# Mixins are a special kind of multiple inheritance for a class.
# You can use them to provide common discrete functionality that, when added to other mixins,
# allows you to define the behavior of a class

# Used for views that interact with any model that contains owner attribute
class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


# handles the formset to add, update, and delete modules for a specific course (Class based view with multiple functionality
class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    # This method is provided by the View class. It takes an HTTP request and its
    # parameters and attempts to delegate to a lowercase method that matches the HTTP
    # method used. A GET request is delegated to the get() method and a POST request to post(),
    # respectively. In this method, you use the get_object_or_404() shortcut function to get the
    # Course object for the given id parameter that belongs to the current user. You include this code
    # in the dispatch() method because you need to retrieve the course for both GET and POST requests.
    # You save it into the course attribute of the view to make it accessible to other methods.
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    # build empty form set
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({"course": self.course,
                                        "formset": formset})

    # post filled form set
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')

        return self.render_to_response({'course': self.course,
                                        "formset": formset})



# to render some list of objects
# class ManageCourseListView(ListView):
#     model = Course
#     template_name = 'courses/manage/course/list.html'
#     def get_queryset(self): # overrite to get courses created by the current user
#         qs = super().get_queryset()
#         return qs.filter(owner=self.request.user)



