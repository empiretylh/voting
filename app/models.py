from email.policy import default
from socketserver import ThreadingUnixDatagramServer
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser, Group

from django.core.files.base import ContentFile
# Create your models here.


class User(AbstractUser):
    phoneno = models.CharField(max_length=11, null=True, blank=False)
    name = models.CharField(max_length=255,null=True)
    profileimage = models.ImageField(
        upload_to="img/profile/%y/%mm/%dd", null=True)
    email = models.CharField(max_length=255,null=True)

    address = models.TextField(blank=True, null=True)
   
    def uploadimage(self, profileimage: str):
        temp_file = ContentFile(profileimage)
        self.profileimage.save(f'{self.pk}'.jpeg, temp_file)



class VotingM(models.Model):
    title = models.CharField(max_length=255,null=False,blank=False)
    is_start =  models.BooleanField(default=False)
    is_end = models.BooleanField(default=True)
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Device(models.Model):
    deviceid = models.CharField(max_length=255,null=False,blank=False)
    name = models.CharField(max_length=255,null=False)
    votingm = models.ForeignKey(VotingM,related_name='devices',on_delete=models.CASCADE)

    def __str__(self):
        return self.deviceid + ' ' +self.name





class SelectionKing(models.Model):
    name =  models.CharField(max_length=255,null=False)
    year = models.CharField(max_length=10,null=False)
    fblink = models.TextField(null=True)
    iglink = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vm =  models.ForeignKey(VotingM, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.year;



class SelectionQueen(models.Model):
    name =  models.CharField(max_length=255,null=False)
    year = models.CharField(max_length=10,null=False)
    fblink = models.TextField(null=True)
    iglink = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vm =  models.ForeignKey(VotingM, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.year;


class FinishKingGroup(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    selection =  models.OneToOneField(SelectionKing, on_delete=models.CASCADE)

    def __str__(self):
        return self.device.name + ' '+ self.selection.name



class FinishQueenGroup(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    selection =  models.OneToOneField(SelectionQueen, on_delete=models.CASCADE)

    def __str__(self):
        return self.device.name + ' '+ self.selection.name


class SelectionImageKing(models.Model):
    image = models.ImageField(
        upload_to="img/selection/king/%y/%mm/%dd", null=True)
    sk = models.ForeignKey(SelectionKing, on_delete=models.CASCADE,related_name='images')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SelectionImageQueen(models.Model):
    image = models.ImageField(
        upload_to="img/selection/queen/%y/%mm/%dd", null=True)
    sk = models.ForeignKey(SelectionQueen, on_delete=models.CASCADE,related_name='images')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Sponsor(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False)
    position = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    price = models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return self.name + ': '+ self.position + ' ' + self.price