from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Notification

# Create your views here.
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "alerts/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        return (
            Notification.objects
            .filter(recipient=self.request.user)
            .order_by("-created_at")
        )


class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = "alerts/notification_detail.html"
    context_object_name = "notification"

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        
        if not self.object.is_read:
            self.object.is_read = True
            self.object.save(update_fields=["is_read"])
        return response