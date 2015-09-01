# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

MAN = u'Erkek'
WOMAN = u'Kadın'
genderList = ((MAN, MAN), (WOMAN, WOMAN))


class User(AbstractUser):
    # AbstractUser.first_name.blank=False
    AbstractUser._meta.get_field('first_name').blank = False
    AbstractUser._meta.get_field('last_name').blank = False
    AbstractUser._meta.get_field('email').blank = False
    # AbstractUser.first_name = models.CharField(max_length=20)
    # AbstractUser.first_name = models.CharField(max_length=20)
    country = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = PhoneNumberField(max_length=20, null=True)
    gender = models.CharField(max_length=5, choices=genderList, default=MAN)
    resume = models.TextField(null=True, blank=True, default='')

    # REQUIRED_FIELDS = ['first_name']

    def __unicode__(self):
        return self.username
