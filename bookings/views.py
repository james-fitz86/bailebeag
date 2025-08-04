from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from .models import Booking, Pitch
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)

            if request.user.is_authenticated:
                # Attach user info to booking for authenticated users
                booking.created_by = request.user
                booking.name = request.user.get_full_name()
                booking.email = request.user.email

                role = request.user.role
                pitch_name = booking.pitch.name.lower()

                is_astro = 'astro' in pitch_name
                is_main = 'main' in pitch_name

                # Default to pending for all roles, changed below based on role
                booking.status = 'pending'

                # Chairman or Secretary auto-approve all Main pitch bookings
                if role in ['chairman', 'secretary'] and is_main:
                    booking.status = 'approved'

                # Manager logic
                elif role == 'manager':
                    if is_astro:
                        # Managers auto-approved for Astro pitch
                        booking.status = 'approved'
                    elif is_main:
                        # Managers approved for Main pitch only if no conflict
                        conflict = Booking.objects.filter(
                            pitch=booking.pitch,
                            start_time__lt=booking.end_time,
                            end_time__gt=booking.start_time,
                            status='approved'
                        ).exists()
                        booking.status = 'conflicting' if conflict else 'approved'

                # Coach logic (Main pitch only, Astro always pending)
                elif role == 'coach' and is_main:
                    # Coaches approved for Main pitch only if no conflict
                    conflict = Booking.objects.filter(
                        pitch=booking.pitch,
                        start_time__lt=booking.end_time,
                        end_time__gt=booking.start_time,
                        status='approved'
                    ).exists()
                    booking.status = 'conflicting' if conflict else 'approved'

                # For all non-managers, set method to 'web'
                if role != 'manager':
                    booking.method = 'web'

            else:
                # Public users: always web method and pending status
                booking.method = 'web'
                booking.status = 'pending'

            booking.save()
            return redirect('booking_list')
    else:
        form = BookingForm(user=request.user)

    return render(request, 'bookings/create_booking.html', {'form': form})



class BookingList(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'

class BookingDetail(DetailView):
    model = Booking

class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Booking
  form_class = BookingForm
  success_url = reverse_lazy('booking_list')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs
    
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
  
  def test_func(self):
    booking = self.get_object()
    user = self.request.user
    return (
        user == booking.created_by or
        user.role in ['manager', 'secretary', 'chairman']
    )

class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Booking
  success_url = reverse_lazy('booking_list')
  
  def test_func(self):
    booking = self.get_object()
    user = self.request.user
    return (
        user == booking.created_by or
        user.role in ['manager', 'secretary', 'chairman']
    )

class PitchList(ListView):
    model = Pitch
    template_name = 'pitch_list.html'
    context_object_name = 'pitches'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Pitch.objects.all()
        return Pitch.objects.none()

def is_authorised_approver(user):
    return user.is_authenticated and user.role in ['manager', 'secretary', 'chairman']

@login_required
@user_passes_test(is_authorised_approver)
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST' and booking.status == 'pending':
        booking.status = 'approved'
        booking.save()
    return redirect('booking_detail', pk=booking.id)

@login_required
@user_passes_test(is_authorised_approver)
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST' and booking.status == 'pending':
        booking.status = 'rejected'
        booking.save()
    return redirect('booking_detail', pk=booking.id)