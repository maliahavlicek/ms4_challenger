from django.db import models
from products.models import ServiceLevel
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('payment_collected', 'Payment Collected'),
    ('payment_rejected', 'Payment Rejected'),
]


class Order(models.Model):
    """
    Users can only order one product
    user - cross references User model
    product - cross references Product model
    status - payment status, if not payment_collected, user will default to FREE tier
    """
    product = models.ForeignKey(ServiceLevel, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=6, decimal_places=2,validators=[
                                             MinValueValidator(0.00),
                                             MaxValueValidator(1500.00)
                                         ])
    date_created = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(choices=ORDER_STATUS_CHOICES, default='pending', max_length=50)

    def __str__(self):
        return "{0} {1} @ {2}".format(self.user.username, self.product.name, self.product.price)

