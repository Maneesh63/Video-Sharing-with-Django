from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser



class CustomUserManager(BaseUserManager):

    def create_user(self,username,password=None, *args,**kwargs):

        user=self.model(username=username,**kwargs)

        user.set_password(password)
        
        user.save(using=self._db)

        return user
    
    def create_superuser(self,username,password=None,**extra):

        extra.setdefault('is_staff',True)

        extra.setdefault('is_superuser',True)

        self.create_user(username,password,**extra)

class CustomUser(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=150, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
   

    
    objects=CustomUserManager()

    USERNAME_FIELD='username'

    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.username
    
    def following_count(self):
        return self.following.count()

    def followers_count(self):
        return self.followers.count()



class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

   
 
class Videostore(models.Model):

    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=577)  
    description = models.TextField()
    video = models.FileField(upload_to='videos/')
    date = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    like_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

class Comment(models.Model):

    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    video=models.ForeignKey(Videostore,on_delete=models.CASCADE)

    comment=models.CharField(max_length=2000,null=False)

    date=models.DateTimeField(auto_now_add=True)

    



