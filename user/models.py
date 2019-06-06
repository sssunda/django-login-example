from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

# 전화번호 유효성 체크
phone_regex = RegexValidator(r'(\d{3})-?(\d{3,4})-?(\d{4})', message="000-0000-0000형식으로 입력해주세요.")

# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, validators=[phone_regex])

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except :
        Profile.objects.create(user=instance)

@receiver(post_save, sender= User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    