from django.db import models
from django.contrib.auth.models import User 
from .utils import get_random_code
from django.template.defaultfilters import  slugify
from django.db.models import Q
from django.shortcuts import reverse
# Create your models here.

class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self,sender):
        profiles = Profile.objects.all().exclude(user=sender)#excluded my profile qs, from profiles queryset

        profile = Profile.objects.get(user=sender)#my profile queried
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))#all relatioships access, send and accepted both from db

        print(qs)

        accepted = set([])
        for rel in qs:#checking in all relations 
            if rel.status == 'accepted':#if any of the relationship is accepted then add to accepted set
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]#checking if profile status is not accepted from the accepted set ,
                                                                                    #then those profiles are avalible to be send invitation
        print(available)
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(default="no bio...",max_length=300)
    email = models.EmailField(max_length=200,blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png',upload_to='avatars') #install pillow ,create media root
    friends = models.ManyToManyField(User, blank=True,related_name='friends')
    slug = models.SlugField(unique=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    objects = ProfileManager()

    def get_friends(self):
        return self.friends.all()


    def get_friends_no(self):
        return self.friends.all().count()


    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()


    def get_likes_given_no(self):
        like = self.like_set.all()
        total_liked = 0
        for item in like:
            if item.value == 'Like':
                total_liked += 1
        return total_liked


    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%d-%m-%Y')}"


    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + '-' + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + ' ' + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})



STATUS_CHOICES = (
    ('send','send'),
    ('accepted','accepted'),
)


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver,status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='receiver')
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
