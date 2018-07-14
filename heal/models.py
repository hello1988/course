from pytz import timezone
from datetime import datetime
from django.db import models

def today_format():
    tz = timezone('Asia/Taipei')
    dt = datetime.now(tz=tz)
    return dt.date().isoformat()

# Create your models here.
class Basis(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Member(Basis):
    line_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=64, default='')
    display_name = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.display_name

class Course(Basis):
    name = models.CharField(max_length=32, verbose_name='課程名稱')
    desc = models.CharField(max_length=60, verbose_name='課程簡介')
    description = models.TextField(default='', verbose_name='課程說明')
    image_url = models.URLField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name

class CourseSchedule(Basis):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.CharField(max_length=32, default=today_format, db_index=True, verbose_name='開課日期')
    start_time = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return '{} - {}'.format( self.course.name, self.start_date )

    def save(self, *args, **kwargs):
        tz = timezone('Asia/Taipei')
        dt = datetime.strptime(self.start_date, '%Y-%m-%d')
        dt.replace(tzinfo=tz)
        self.start_time = dt.timestamp()

        super(CourseSchedule, self).save(*args, **kwargs)

class CourseApply(Basis):
    schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

