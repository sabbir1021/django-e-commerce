from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth import get_user_model
User= get_user_model


class User(AbstractUser):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. User'


class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profiles', on_delete=models.CASCADE)
    phone = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = '2. Profile'

    def __str__(self):
        return str(self.user)
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.profiles.save()
    except Exception as e:
        pass


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    TYPE_CHOICES = (
        ('H', 'Home',),
        ('O', 'Office',),
    )
    address_type = models.CharField(max_length=1,choices=TYPE_CHOICES)
    class Meta:
        verbose_name = 'ShippingAddress'
        verbose_name_plural = '3. ShippingAddress'
    def __str__(self):
        return self.address


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    TYPE_CHOICES = (
        ('H', 'Home',),
        ('O', 'Office',),
    )
    address_type = models.CharField(max_length=1,choices=TYPE_CHOICES)
    class Meta:
        verbose_name = 'BillingAddress'
        verbose_name_plural = '4. BillingAddress'
    def __str__(self):
        return self.address
