from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking, Pitch
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class PitchList(ListView):
    model = Pitch
    template_name = 'pitch_list.html'
    context_object_name = 'pitches'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Pitch.objects.all()
        return Pitch.objects.none()