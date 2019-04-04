from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=13)
    meter_id = models.CharField(max_length=50)

    class Meta:
        unique_together = ('meter_id', 'user', 'contact_number')

    def __str__(self):
        return self.user.__str__()


class Record(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    volt = models.FloatField()
    current = models.FloatField()
    watt = models.FloatField()
    energy = models.FloatField()

    class Meta:
        unique_together = ('profile', 'time')

    def __str__(self):
        return self.profile.__str__() + " " + str(self.time)


class Bill(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    time = models.DateTimeField(
        u"Billing Time", auto_now=False, auto_now_add=False)
    cost = models.FloatField()


def __str__(self):
    return self.profile.__str__() + " " + str(self.time) + " " + self.cost
