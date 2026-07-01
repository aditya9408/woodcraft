from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html
from .models import Project, ProjectCategory, ProjectImage, Testimonial, ContactMessage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 2
    fields = ('image', 'caption', 'order')


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'order', 'created_at')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured', 'order')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Display', {
            'fields': ('is_featured', 'order')
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_initials', 'rating', 'is_active', 'order')
    list_editable = ('is_active', 'order')


def send_reply_email(modeladmin, request, queryset):
    """Admin action: send a reply email to selected contact messages."""
    sent = 0
    for msg in queryset:
        if msg.admin_notes:
            send_mail(
                subject=f'Re: {msg.subject} — WoodCraft',
                message=msg.admin_notes,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[],   # Add recipient logic if storing email
                fail_silently=True,
            )
            msg.status = 'replied'
            msg.save()
            sent += 1
    modeladmin.message_user(request, f'{sent} message(s) marked as replied.')

send_reply_email.short_description = 'Mark selected as replied'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'phone_number', 'subject', 'status', 'created_at', 'send_email_link'
    )
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'subject', 'description')
    readonly_fields = ('first_name', 'last_name', 'phone_number', 'subject', 'description', 'created_at')
    actions = [send_reply_email]
    fieldsets = (
        ('Message Details', {
            'fields': ('first_name', 'last_name', 'phone_number', 'subject', 'description', 'created_at')
        }),
        ('Admin', {
            'fields': ('status', 'admin_notes')
        }),
    )

    def send_email_link(self, obj):
        mailto = (
            f'mailto:?subject=Re: {obj.subject}'
            f'&body=Dear {obj.full_name},%0A%0A'
        )
        return format_html('<a href="{}" target="_blank">📧 Reply</a>', mailto)
    send_email_link.short_description = 'Quick Reply'

    def has_add_permission(self, request):
        return False  # Messages are created only via the contact form