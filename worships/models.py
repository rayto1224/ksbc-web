from django.db import models
from django.utils import timezone


class WorshipSermon(models.Model):
    speaker_name = models.CharField(max_length=100, verbose_name="講員")
    sermon_title = models.CharField(max_length=200, verbose_name="講道題目")
    youtube_link = models.URLField(verbose_name="YouTube連結")
    sermon_date = models.DateField(default=timezone.now, verbose_name="講道日期")

    class Meta:
        ordering = ["-sermon_date"]
        verbose_name = "崇拜講道"
        verbose_name_plural = "崇拜講道集"

    def __str__(self):
        return f"{self.sermon_date} - {self.sermon_title} ({self.speaker_name})"
