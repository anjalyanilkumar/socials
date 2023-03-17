from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
#Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to="profilepics",default="profilepics/default-propic.png")
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    followers = models.ManyToManyField(User, related_name="followers")
    

    def __str__(self):
        return f'{self.user.username}'
    
    @property
    def followerscount(self):
         return self.followers.all().count()
    
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Posts(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    caption=models.CharField(max_length=200)
    images=models.ImageField(null=True,upload_to="images",blank=True)
    likes = models.ManyToManyField(Profile, related_name="likes")
    created_date=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
                   
    def __str__(self):     
        return self.caption
    
    @property
    def postlikecount(self):
        return self.likes.all().count()

    @property
    def post_comments(self):
        return self.comments_set.all().annotate(u_count=Count('cmt_likes')).order_by('-u_count')

class Comments(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    cmt_likes=models.ManyToManyField(Profile,related_name="cmt_likes")


    def __str__(self):
        return self.comment

    @property
    def likecount(self):
        return self.cmt_likes.all().count()




