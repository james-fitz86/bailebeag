from django.shortcuts import render

# Create your views here.
def home(request):
  return render(request, 'config/home.html')

def error_403(request, exception=None):
    return render(request, 'config/errors/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'config/errors/404.html', status=404)

def error_500(request):
    return render(request, 'config/errors/500.html', status=500)
