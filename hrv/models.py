from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import json

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique = True)
    email = models.EmailField(max_length = 120, unique = True, default = 'abc@gmail.com')
    picture = models.ImageField(upload_to='profile_images', blank=True)

    watch = models.CharField(max_length=200,unique=False, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username




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
class Data(models.Model):
    time = models.CharField(max_length=200, unique=False)
    user_id = models.CharField(max_length=200)
    bpm = models.FloatField(null = True)
    ibi = models.FloatField(null = True)
    sdnn = models.FloatField(null = True)
    sdsd = models.FloatField(null = True)
    rmssd = models.FloatField(null = True)
    pnn20 = models.FloatField(null = True)
    pnn50 = models.FloatField(null = True)
    hr_mad = models.FloatField(null = True)
    sd1 = models.FloatField(null = True)
    sd2 = models.FloatField(null = True)
    s = models.FloatField(null = True)
    sd1_sd2 = models.FloatField(null = True)
    breathingrate = models.FloatField(null = True)
    vlf = models.FloatField(null = True)
    lf = models.FloatField(null = True)
    hf = models.FloatField(null = True)
    lf_hf = models.FloatField(null = True)
    p_total = models.FloatField(null = True)
    vlf_perc = models.FloatField(null = True)
    lf_perc = models.FloatField(null = True)
    hf_perc = models.FloatField(null = True)
    lf_nu = models.FloatField(null = True)
    hf_nu = models.FloatField(null = True)



    def save(self, *args, **kwargs):
        super(Data, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_id + " " + self.time
    class Meta:
        verbose_name_plural = 'Data'
