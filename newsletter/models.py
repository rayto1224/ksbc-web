from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

import os
# Create your models here.
def newsletter_upload_path(instance, filename):
    """Store files like: newsletters/2025/03/newsletter-2025-03-v1.pdf"""
    year = instance.published_date.strftime('%Y')
    month = instance.published_date.strftime('%m')
    return f'newsletters/{year}/{month}/{filename}'


class Newsletter(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="e.g. 'TechBit #42 - March 2025'"
    )
    
    slug = models.SlugField(
        max_length=120,
        unique=True,
        help_text="Used in URLs - auto-generated recommended"
    )
    
    published_date = models.DateField(
        default=timezone.now,
        help_text="Date this issue was/will be considered published"
    )
    
    pdf_file = models.FileField(
        upload_to=newsletter_upload_path,
        help_text="PDF version of the newsletter"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Optional short summary / teaser (appears in archive)"
    )
    
    is_published = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from public archive"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        get_latest_by = 'published_date'
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['is_published', 'published_date']),
        ]

    def __str__(self):
        return f"{self.title} ({self.published_date:%Y-%m})"

    def get_absolute_url(self):
        return reverse('newsletter:detail', kwargs={'slug': self.slug})

    def filename(self):
        return os.path.basename(self.pdf_file.name)