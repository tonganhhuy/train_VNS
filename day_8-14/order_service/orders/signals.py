from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .tasks import send_order_email_task


@receiver(post_save, sender=Order)
def order_created_signal(sender, instance, created, **kwargs):
    if created:
        # Nếu order mới được tạo, trigger celery task gửi email
        send_order_email_task.delay(instance.id)
