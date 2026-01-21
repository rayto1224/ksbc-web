from django.db.models import Q, F
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Event, EventParticipant, Donation
from .forms import EventRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.
def activities(request):
    return render(request,'activities/index.html')

class UpcomingEventsListView(ListView):
    model = Event
    template_name = 'activities/event_list.html'
    context_object_name = 'events'
    paginate_by = 4

    def get_queryset(self):
        today = timezone.now().date()
        qs = Event.objects.filter(is_active=True).filter(
            Q(is_announcement=True) |
            Q(start_date__gte=today) |
            Q(appl_deadline__isnull=True)
        ).select_related()
        # Featured first, then by event_id descending (newest first)
        return qs.order_by('-is_featured', 'is_announcement', '-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # No need to manually set page_obj - it's already set by parent
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'activities/event_detail.html'
    pk_url_kwarg = 'event_id'           # because primary key is event_id
    context_object_name = 'event'

    def get_queryset(self):
        return Event.objects.filter(is_announcement=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context['already_registered'] = False
        context['quota_full'] = event.quota_full
        context['is_expired'] = event.is_expired

        # Optional: check if current user/email already registered
        if self.request.user.is_authenticated:
            context['already_registered'] = EventParticipant.objects.filter(
                event=event, email=self.request.user.email
            ).exists()
        # You can also check by email from session/cookies if guest

        return context


class EventRegistrationCreateView(CreateView):
    model = EventParticipant
    form_class = EventRegistrationForm
    template_name = 'activities/event_register.html'
    success_url = reverse_lazy('activities:list')   # or event detail / thank you page

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(
            Event,
            event_id=kwargs.get('event_id'),
            is_announcement=False
        )

        if self.event.is_expired:
            messages.error(request, "This event registration has closed.")
            return redirect('activities:detail', event_id=self.event.event_id)

        if self.event.quota_full and not self.event.unlimited_quota:
            messages.error(request, "Sorry, this event is fully booked.")
            return redirect('activities:detail', event_id=self.event.event_id)

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.event
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def form_valid(self, form):
        form.instance.event = self.event
        
        # Auto-fill user if logged in
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            # Always use user's account email for authenticated users
            # to ensure dashboard can find all their registrations
            form.instance.email = self.request.user.email

        # Decrease quota_left if not unlimited
        if not self.event.unlimited_quota and self.event.quota_left > 0:
            # Use atomic update to avoid race conditions
            Event.objects.filter(
                event_id=self.event.event_id,
                quota_left__gt=0  # Additional safety check
            ).update(quota_left=F('quota_left') - 1)
            # Refresh the event object from database
            self.event.refresh_from_db()

        # Save the form first to get the participant instance
        response = super().form_valid(form)
        
        # Send confirmation email
        try:
            participant = form.instance
            subject = f"Registration Confirmation: {self.event.title}"
            
            # Create email context
            context = {
                'event': self.event,
                'participant': participant,
                'registration_date': participant.registered_at,
            }
            
            # Render HTML email template
            html_message = render_to_string('activities/emails/registration_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                recipient_list=[participant.email],
                html_message=html_message,
                fail_silently=False,
            )
            
        except Exception as e:
            # Log the error but don't crash the registration
            messages.warning(self.request, f"Registration saved but email could not be sent: {str(e)}")
        
        messages.success(self.request, "Registration successful! Check your email.")
        return response
    
    from django.contrib.auth.mixins import LoginRequiredMixin


class UserDashboardView(LoginRequiredMixin, ListView):
    template_name = 'activities/dashboard.html'  # adjust app name if needed
    context_object_name = 'registrations'
    paginate_by = 10  # optional: paginate if many registrations

    def get_queryset(self):
        # Fetch registrations by user's email, ordered by most recent
        return EventParticipant.objects.filter(
            email=self.request.user.email
        ).select_related('event').order_by('-registered_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # for personalization

        # Group donations by Financial Year (April 1 - March 31)
        # Result structure: [ {'financial_year': '2025-2026', 'donations': [obj, obj]}, ... ]
        donations = Donation.objects.filter(user=self.request.user).order_by('-date')
        
        from collections import defaultdict
        grouped_donations = defaultdict(list)
        
        for donation in donations:
            if donation.date.month >= 4:
                fy = f"{donation.date.year}-{donation.date.year + 1}"
            else:
                fy = f"{donation.date.year - 1}-{donation.date.year}"
            grouped_donations[fy].append(donation)
            
        # Convert to a sorted list of tuples/dicts for the template
        # Sort headers descending (e.g. 2025-2026, 2024-2025)
        # sorted_items = sorted(grouped_donations.items(), key=lambda x: x[0], reverse=True)
        # Better: create a list of dicts to be more template-friendly
        
        context['grouped_donations'] = sorted(
            [{'financial_year': k, 'list': v} for k, v in grouped_donations.items()],
            key=lambda x: x['financial_year'],
            reverse=True
        )
        return context



class WithdrawRegistrationView(LoginRequiredMixin, View):
    def get(self, request, registration_id):
        reg = get_object_or_404(
            EventParticipant,
            id=registration_id,
            email=request.user.email  # ensure owned by user via email
        )
        
        if reg.withdrawal_date:
            messages.info(request, "You have already withdrawn from this event.")
        elif reg.event.is_expired:
            messages.error(request, "Cannot withdraw from an expired event.")
        else:
            reg.withdrawal_date = timezone.now().date()
            reg.save()
            
            # Optional: increase quota_left if not unlimited
            if not reg.event.unlimited_quota:
                # Use atomic update to avoid race conditions
                Event.objects.filter(
                    event_id=reg.event.event_id
                ).update(quota_left=F('quota_left') + 1)
                # Refresh the event object from database
                reg.event.refresh_from_db()
            
            messages.success(request, f"Successfully withdrawn from '{reg.event.title}'.")
        
        return redirect('activities:dashboard')
