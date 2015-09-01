import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from membership.models import User


def random_name_generator(size=15):
    """
    create string for given size

    :param size: int
    :return: string
    """

    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def generate_filename(self, name):
    """
    deprecated
    Generate filename for image.

    :param name:
    :return: url
    """

    new_name = random_name_generator()

    name_array = name.split('.')
    extension = name_array[len(name_array) - 1]

    contest_year = Contest.objects.order_by('year').last()

    url = "compositions/{0}/{1}_{2}.{3}".format(contest_year, self.owner.id, new_name, extension)
    print url
    return url


class Device(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Software(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class StageMaterial(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class TrackUpload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, to_field='id')
    datafile = models.FileField()

    def __unicode__(self):
        return self.name


class Composition(models.Model):
    name = models.CharField(max_length=100, default='eser')
    owner = models.ForeignKey(User)
    contest = models.ForeignKey('Contest')
    url = models.URLField(default='')
    devices = models.ManyToManyField('Device', blank=True)
    softwares = models.ManyToManyField('Software', blank=True, related_name='softwares')
    stage_materials = models.ManyToManyField('StageMaterial', blank=True)
    is_qualified = models.BooleanField(default=False)
    is_finalist = models.BooleanField(default=False)
    order = models.SmallIntegerField(default=0)

    def __unicode__(self):
        # return '%s - %s' % self.owner.username, self.name
        return 'composition'


class Contest(models.Model):
    year = models.IntegerField(unique=True)
    theme = models.CharField(max_length=100, null=True)
    poster = models.URLField(null=True)
    description=models.TextField(null=True, blank=True, default='')
    start_date = models.DateField()
    final_date = models.DateField()
    finish_date = models.DateField()
    create_date = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __unicode__(self):
        return str(self.year)


class Vote(models.Model):
    contest = models.ForeignKey(Contest)
    composition = models.ForeignKey(Composition, related_name='composition')
    value = models.IntegerField()
    ip = models.GenericIPAddressField()
    vote_date = models.DateTimeField(auto_created=True, auto_now_add=True)


LINK = 'link'
INDEX = 'index'
contentTypes = ((LINK, LINK), (INDEX, INDEX))


class Content(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=30)
    content = models.TextField(null=True, blank=True)
    category_name = models.CharField(max_length=5, choices=contentTypes, default=LINK)
    create_date = models.DateTimeField(auto_created=True, null=True)
    update_date = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=False)
    is_for_static_content = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
