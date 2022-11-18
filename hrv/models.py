from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #username = models.CharField(max_length=120, unique=True)
    # The additional attributes we wish to include.
    slug = models.SlugField(unique = True)
    #email = models.EmailField(max_length = 120, unique = True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    watch = models.CharField(max_length=200,unique=False, blank=True)
    #pictures = models.ImageField(upload_to='', blank = True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
class UserWatch(models.Model):
    watch = models.CharField(max_length=200,unique=False, blank = True)
    class Meta:
        verbose_name_plural = "watches"



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class PPG(models.Model):
    date = models.DateTimeField('date inserted')
    time_stamp = models.IntegerField(default=0)
    ppg_signal = models.FloatField(default=0.0)
