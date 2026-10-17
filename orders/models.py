import uuid
from datetime import date

from django.db import models

from catalog.models import Package, package_for_due_date


class Order(models.Model):
    PLAN_SUBSCRIPTION = 'subscription'
    PLAN_SINGLE = 'single'
    PLAN_CHOICES = [(PLAN_SUBSCRIPTION, 'Abonnement (månedligt)'), (PLAN_SINGLE, 'Enkelt boks')]

    STATUS_CHOICES = [
        ('pending', 'Afventer betaling'),
        ('paid', 'Betalt / aktiv'),
        ('past_due', 'Betaling fejlet'),
        ('cancelled', 'Opsagt'),
        ('completed', 'Afsluttet'),
        ('demo', 'Demo (ingen betaling)'),
    ]

    reference = models.CharField(max_length=20, unique=True, editable=False)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name='orders')
    due_date = models.DateField(null=True, blank=True, help_text='Terminsdato (hvis gravid)')
    birth_date = models.DateField(null=True, blank=True, help_text='Fødselsdato (efter fødslen-pakken)')
    amount = models.DecimalField(max_digits=8, decimal_places=2, help_text='Beløb pr. levering (DKK)')

    # Filled from Stripe Checkout
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=2, blank=True, default='DK')
    marketing_consent = models.BooleanField(default=False)
    include_extras = models.BooleanField(default=True, help_text='Komplet (med tillæg) eller Basis (kun SST)')
    skip_calcium = models.BooleanField(default=False, help_text='Kunden får ≥ ½ liter mælk dagligt → intet calciumtilskud (SST)')

    stripe_session_id = models.CharField(max_length=255, blank=True, db_index=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ordre'
        verbose_name_plural = 'ordrer'

    def __str__(self):
        return f'{self.reference} – {self.email or "ukendt"}'

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = 'MB' + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    @property
    def is_active_subscription(self):
        return self.plan == self.PLAN_SUBSCRIPTION and self.status == 'paid'

    def package_for(self, on_date=None):
        """Which box this customer should receive on a given date.

        Pregnant customers follow their due date. "Ønsker at blive gravid" stays on the TTC box until the customer
        tells us a due date. Postpartum is a single stage.
        """
        on_date = on_date or date.today()
        if self.due_date:
            pkg, _ = package_for_due_date(self.due_date, today=on_date)
            return pkg
        return self.start_package

    def package_for_shipment(self, on_date=None):
        if self.plan == self.PLAN_SINGLE:
            return self.start_package
        return self.package_for(on_date)


class Shipment(models.Model):
    """One physical box sent to a customer. Created by staff when packing (or via the admin action)."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipments')
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=80, blank=True)
    note = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'forsendelse'
        verbose_name_plural = 'forsendelser'

    def __str__(self):
        return f'{self.order.reference}: {self.package.label}'


class ShipmentLine(models.Model):
    """What physically went into a box. Drives the refill ledger (how long each customer's supply lasts)."""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='lines')
    item = models.ForeignKey('catalog.Item', on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1, help_text='Antal pakninger')
    units_per_day = models.DecimalField(max_digits=4, decimal_places=2, default=1)
    reason = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = 'indhold'
        verbose_name_plural = 'indhold'

    def __str__(self):
        return f'{self.quantity} × {self.item.name}'


class CustomerRequest(models.Model):
    """Fortrydelse (withdrawal) or opsigelse (cancellation) submitted through the website. Kept as evidence."""
    KIND_CHOICES = [('withdrawal', 'Fortrydelse'), ('cancellation', 'Opsigelse af abonnement')]
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name='requests')
    reference = models.CharField(max_length=40, blank=True)
    name = models.CharField(max_length=160, blank=True)
    email = models.EmailField()
    details = models.TextField(blank=True)
    result = models.CharField(max_length=300, blank=True)
    handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'kundehenvendelse (fortryd/opsig)'
        verbose_name_plural = 'kundehenvendelser (fortryd/opsig)'

    def __str__(self):
        return f'{self.get_kind_display()} {self.reference} {self.email}'


class StripeEvent(models.Model):
    """Processed webhook events (idempotency)."""
    event_id = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=100)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type} {self.event_id}'
