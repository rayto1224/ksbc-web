from django.db import models


# Create your models here.
class FellowshipEvent(models.Model):
    title = models.CharField("活動名稱", max_length=100)
    date_text = models.CharField(
        "日期（文字）", max_length=50, blank=True
    )  # e.g. 隔星期三
    time_text = models.CharField(
        "時間", max_length=50, blank=True
    )  # e.g. 9:15–11:00 am
    location = models.CharField("地點", max_length=50, blank=True)  # e.g. 810 / Zoom
    poster = models.ImageField("Poster", upload_to="posters/", blank=True, null=True)

    description = models.TextField("內容/簡介", blank=True)
    is_active = models.BooleanField("上架", default=True)
    sort_order = models.PositiveIntegerField("排序", default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "聚會活動"
        verbose_name_plural = "聚會活動"

    def __str__(self):
        return self.title
