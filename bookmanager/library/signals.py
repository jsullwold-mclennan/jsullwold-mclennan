from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book

@receiver(post_save, sender=Book)
def update_checked_out_status(sender, instance, created, **kwargs):
    if created:
        print(f'New book added: {instance.title}')
    else:
        if instance.checked_out:
            print(f'{instance.title} has been checked out.')
        else:
            print(f'{instance.title} has been checked in.')