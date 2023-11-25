from django.shortcuts import render
from django.views.generic import ListView
from tasks.models import ToDo, Subject, Exam
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group

@method_decorator(login_required, name='dispatch')
class MarkSheetListView(ListView):
    model = ToDo
    template_name = 'marksheet.html'
    context_object_name = 'marksheet'

    def get_queryset(self):
        username = self.request.user
        return ToDo.objects.filter(username=username).select_related('subject', 'exam')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['exams'] = Exam.objects.all()

        # Check if the user is in the 'Leader' group
        is_leader = self.request.user.groups.filter(name='Leader').exists()
        context['is_leader'] = is_leader

        return context
