from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.conf import settings


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    appl_deadline = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active / Visible",
        help_text="Uncheck to hide this event from the public listing (e.g. draft, cancelled, postponed)"
    )

    is_free = models.BooleanField(default=False, verbose_name="Free event")
    fee_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)],
        verbose_name="Ticket price / Fee"
    )
    fee_currency = models.CharField(max_length=3, default='HKD')
    early_bird_fee = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0.00)],
        verbose_name="Early bird price",
        help_text="Optional discounted price"
    )
    is_announcement = models.BooleanField(
        default=False,
        verbose_name="Informational only",
        help_text="Check if this is just an informational poster/announcement (no registration allowed)."
    )

    unlimited_quota = models.BooleanField(
        default=False,
        verbose_name="Unlimited quota",
        help_text="If checked, there is no limit on the number of participants"
    )
    
    quota_left = models.IntegerField(
        default=0,
        verbose_name="Quota left",
        help_text="Number of available spots remaining. Only relevant if unlimited_quota is False."
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        if self.appl_deadline is None:
            return False
        return self.appl_deadline < timezone.now().date()

    @property
    def display_price(self):
        if self.is_free or self.fee_amount == 0:
            return "Free"
        return f"{self.fee_amount} {self.fee_currency}"

    @property
    def quota_full(self):
        return not self.unlimited_quota and self.quota_left <= 0

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_id']),
        ]


class EventParticipant(models.Model):
    """
    Stores who registered for an event.
    - Email is required and unique **per event**
    - Optional link to a site User (if they are logged in / members)
    - Allows guest / non-member registrations
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='participants',
        related_query_name='participant'
    )
    
    # Core identifier
    email = models.EmailField(
        verbose_name="Registration email",
        help_text="Used as the main unique identifier per event"
    )
    
    # Optional: if the person has a user account on the site
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='event_registrations',
        verbose_name="Registered user (optional)",
        help_text="Filled automatically if registration was done while logged in"
    )
    
    # Personal info (optional / partial — depending on your form requirements)
    full_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Full name",
        help_text="Optional — may be collected during registration"
    )
    
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telephone number",
        help_text="Optional contact number"
    )
    
    # Registration metadata
    registered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Registration date"
    )
    
    # Withdrawal date (if participant withdraws)
    withdrawal_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Withdrawal date",
        help_text="Date when participant withdrew from the event"
    )
    
    # Optional notes / admin use
    notes = models.TextField(blank=True, help_text="Internal notes, special requests, etc.")

    class Meta:
        # Prevent the same email from registering twice for one event
        unique_together = [['event', 'email']]
        
        # Most recent registrations first
        ordering = ['-registered_at']
        
        verbose_name = "Event Participant"
        verbose_name_plural = "Event Participants"
        
        indexes = [
            models.Index(fields=['event', 'email']),
            models.Index(fields=['user']),
            models.Index(fields=['registered_at']),
        ]

    def __str__(self):
        name_part = self.full_name or self.email
        user_part = f" ({self.user.username})" if self.user else ""
        return f"{name_part} → {self.event.title}{user_part}"

    @property
    def is_member(self):
        return self.user is not None

    @property
    def registration_status(self):
        if self.withdrawal_date is not None:
            return "Withdrawn"
        if self.event.is_expired:
            return "Event ended"
        # Check if event quota is full
        if self.event.quota_full:
            return "Rejected"
        return "Accepted"


class Donation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donations',
        verbose_name="User"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        verbose_name="Donation Amount"
    )
    date = models.DateField(default=timezone.now, verbose_name="Donation Date")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.date})"

