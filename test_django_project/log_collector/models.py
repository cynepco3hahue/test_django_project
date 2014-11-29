from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.


class Log(models.Model):
    def __str__(self):
        return self.log_name

    def __unicode__(self):
        return u'%s' % self.log_name

    log_name = models.CharField(max_length=50)
    log_path = models.CharField(max_length=100)


class Host(models.Model):
    def __str__(self):
        return self.host_name

    def __unicode__(self):
        return u'%s' % self.host_name

    host_name = models.CharField(
        max_length=50, validators=[MinLengthValidator(1)])
    host_root_user = models.CharField(
        max_length=20, validators=[MinLengthValidator(1)])
    host_root_password = models.CharField(
        max_length=20, validators=[MinLengthValidator(1)])
