from django.db import models
from django.utils.text import slugify
from PIL import Image as PILImage
import io
from django.core.files.base import ContentFile


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Project Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while ProjectCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects'
    )
    short_description = models.CharField(max_length=300, blank=True, default='', help_text='Shown on project card')
    description = models.TextField(blank=True, default='', help_text='Full project detail page content')
    cover_image = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text='Show on Home page')
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower = first)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def compress_image(self, image_field):
        img = PILImage.open(image_field)
        img = img.convert('RGB')
        # Resize if larger than 1200px wide
        if img.width > 1200:
            ratio = 1200 / img.width
            new_height = int(img.height * ratio)
            img = img.resize((1200, new_height), PILImage.LANCZOS)
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=75, optimize=True)
        output.seek(0)
        return ContentFile(output.read(), name=image_field.name)

    def save(self, *args, **kwargs):
        # Auto-compress cover image
        if self.cover_image and hasattr(self.cover_image, 'file'):
            try:
                self.cover_image = self.compress_image(self.cover_image)
            except Exception:
                pass

        # Auto-generate slug
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.project.title} — image {self.order}'

    def save(self, *args, **kwargs):
        # Auto-compress gallery images
        if self.image and hasattr(self.image, 'file'):
            try:
                img = PILImage.open(self.image)
                img = img.convert('RGB')
                if img.width > 1200:
                    ratio = 1200 / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((1200, new_height), PILImage.LANCZOS)
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=75, optimize=True)
                output.seek(0)
                self.image = ContentFile(output.read(), name=self.image.name)
            except Exception:
                pass
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    author_name = models.CharField(max_length=150)
    author_initials = models.CharField(max_length=3, help_text='e.g. PK, AS')
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.author_name} — {self.rating}★'

    @property
    def stars(self):
        return '★' * self.rating


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True, help_text='Internal notes for admin use')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name} — {self.subject} ({self.created_at:%d %b %Y})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'