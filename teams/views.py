from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import TeamForm
from .models import Team


# Create your views here.
@login_required
def create_team(request):
    if request.user.role not in ['chairman', 'secretary']:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()

    return render(request, 'teams/create_team.html', {'form': form})

class TeamList(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'


class TeamDetail(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/create_team.html'
    success_url = reverse_lazy('team_list')

    def test_func(self):
        return self.request.user.role in ['chairman', 'secretary']


class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('team_list')

    def test_func(self):
        return self.request.user.role in ['chairman', 'secretary']
