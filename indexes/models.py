# indexes/models.py - 簡化版（只有兩個模型）
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class Ministry(models.Model):
    """事工動態"""

    title = models.CharField("標題", max_length=200)
    description = models.TextField("描述", blank=True)
    activity_date = models.DateField("活動日期", default=timezone.now)
    location = models.CharField("地點", max_length=100, blank=True)
    image = models.ImageField(
        "圖片",
        upload_to="ministries/%Y/%m/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif"])],
    )
    is_active = models.BooleanField("是否顯示", default=True)
    display_order = models.IntegerField("顯示順序", default=0)

    class Meta:
        verbose_name = "事工動態"
        verbose_name_plural = "事工動態"
        ordering = ["-activity_date", "display_order"]

    def __str__(self):
        return self.title


class Prayer(models.Model):
    """代禱事項"""

    title = models.CharField("標題", max_length=200)
    content = models.TextField("代禱內容")
    is_urgent = models.BooleanField("緊急代禱", default=False)
    is_active = models.BooleanField("是否顯示", default=True)
    display_date = models.DateField("顯示日期", default=timezone.now)

    class Meta:
        verbose_name = "代禱事項"
        verbose_name_plural = "代禱事項"
        ordering = ["-is_urgent", "-display_date"]

    def __str__(self):
        return self.title
