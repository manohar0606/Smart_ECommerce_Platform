from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Notification, Order


@receiver(pre_save, sender=Order)
def capture_old_order_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_order_status = None
        return

    old_status = sender.objects.filter(
        pk=instance.pk
    ).values_list(
        "order_status",
        flat=True,
    ).first()

    instance._old_order_status = old_status


@receiver(post_save, sender=Order)
def create_order_status_notification(
    sender,
    instance,
    created,
    **kwargs,
):
    if created:
        return

    old_status = getattr(
        instance,
        "_old_order_status",
        None,
    )

    if old_status == instance.order_status:
        return

    messages = {
        "confirmed": f"Order #{instance.id} has been confirmed.",
        "shipped": f"Order #{instance.id} has been shipped.",
        "delivered": f"Order #{instance.id} has been delivered.",
        "cancelled": f"Order #{instance.id} has been cancelled.",
        "pending": f"Order #{instance.id} is pending.",
    }

    message = messages.get(
        instance.order_status,
        f"Order #{instance.id} status changed to {instance.order_status}.",
    )

    Notification.objects.create(
        user_id=instance.user_id,
        type="shipping" if instance.order_status in {
            "shipped",
            "delivered",
        } else "order",
        message=message,
        is_read=False,
    )