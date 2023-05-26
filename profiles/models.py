from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import RawSQL
import uuid
import datetime
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, default='', blank=False)
    HAIR_COLOUR = (
        ('BLACK', 'Black'),
        ('BLONDE', 'Blonde'),
        ('BROWN', 'Brown'),
        ('RED', 'Red'),
        ('GREY', 'Grey'),
        ('BALD', 'Bald'),
        ('BLUE', 'Blue'),
        ('PINK', 'Pink'),
        ('GREEN', 'Green'),
        ('PURPLE', 'Purple'),
        ('OTHER', 'Other'),
    )
    BODY_TYPE = (
        ('THIN', 'Thin'),
        ('AVERAGE', 'Average'),
        ('FIT', 'Fit'),
        ('MUSCULAR', 'Muscular'),
        ('A LITTLE EXTRA', 'A Little Extra'),
        ('CURVY', 'Curvy'),
    )
    LOOKING_FOR = (
        ('MALE', 'Men'),
        ('FEMALE', 'Women'),
    )

    HAIR_LENGTH = (
        ('LONG', 'Long'),
        ('SHOULDER LENGTH', 'Shoulder Length'),
        ('AVERAGE', 'Average'),
        ('SHORT', 'Short'),
        ('SHAVED', 'Shaved')
    )
    ETHNICITY = (
        ('WHITE', 'White'),
        ('ASIAN: INDIAN', 'Asian: Indian'),
        ('ASIAN: PAKISTANI', 'Asian: Pakistani'),
        ('ASIAN: BANGLADESHI', 'Asian: Bangladeshi'),
        ('ASIAN: CHINESE', 'Asian: Chinese'),
        ('BLACK', 'Black'),
        ('MIXED', 'Mixed'),
        ('OTHER ETHNICITY', 'Other Ethnicity')
    )
    RELATIONSHIP_STATUS = (
        ('NEVER MARRIED', 'Never Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
        ('SEPARATED', 'Separated')
    )
    EDUCATION = (
    ('HIGH SCHOOL', 'High School'),
    ('COLLEGE', 'College'),
    ('BACHELORS DEGREE', 'Bachelors Degree'),
    ('MASTERS', 'Masters'),
    ('PHD / POST DOCTORAL', 'PhD / Post Doctoral'),
    )
    GENDER = (
        ("MALE", "Male"),
        ("FEMALE", "Female"))


    gender = models.CharField(choices=GENDER, default="Мужчина", max_length=7)
    hair_length = models.CharField(choices=HAIR_LENGTH, default="Длинные", blank=False, max_length=100)
    ethnicity = models.CharField(choices=ETHNICITY, default="Белый", blank=False, max_length=100)
    relationship_status = models.CharField(choices=RELATIONSHIP_STATUS, default="Не женат", blank=False, max_length=100)
    education = models.CharField(choices=EDUCATION, default="Среднее", blank=False, max_length=100)
    height = models.DecimalField(max_digits=10, default=170, decimal_places=0)
    hair_colour = models.CharField(choices=HAIR_COLOUR, default="Брюнет", blank=False, max_length=10)
    body_type = models.CharField(choices=BODY_TYPE, default="Худой", blank=False, max_length=15)
    looking_for = models.CharField(choices=LOOKING_FOR, default='Мужчина', blank=False, max_length=7)
    children = models.BooleanField(default=False)
    location = models.CharField(max_length=100, default='', blank=False)
    birth_date = models.DateField(null=True, default='1990-01-01', blank=True)

    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25  )

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

def image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('media/', filename)

class ProfileImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=image_filename, blank=True)
