from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages

# Create your views here.
def register(request):
  if request.user.is_authenticated:
    return redirect('profile')

  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      return redirect('home')
  else:
    form = UserRegisterForm()
  return render(request, 'users/register.html', {'form': form} )

@login_required
def profile(request):
  if request.method == 'POST':
    form = UserUpdateForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, f'Your account has been updated')
      return redirect('profile')
  else:
    form = UserUpdateForm(instance=request.user)

  context = {
    'form': form,
  }
  return render(request, 'users/profile.html', context)