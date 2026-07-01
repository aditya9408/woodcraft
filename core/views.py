from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Project, ProjectCategory, Testimonial
from .forms import ContactForm


def home(request):
    featured_projects = Project.objects.filter(is_featured=True).select_related('category')[:4]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    contact_form = ContactForm()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            msg = contact_form.save()
            _send_contact_notification(msg)
            messages.success(request, 'Thank you! Your message has been sent. We\'ll get back to you within 24 hours.')
            return redirect('home')

    context = {
        'featured_projects': featured_projects,
        'testimonials': testimonials,
        'contact_form': contact_form,
        'active_page': 'home',
    }
    return render(request, 'core/home.html', context)


def projects(request):
    categories = ProjectCategory.objects.all()
    category_slug = request.GET.get('category', '')

    all_projects = Project.objects.select_related('category')
    if category_slug:
        all_projects = all_projects.filter(category__slug=category_slug)

    context = {
        'projects': all_projects,
        'categories': categories,
        'active_category': category_slug,
        'active_page': 'projects',
    }
    return render(request, 'core/projects.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    gallery = project.images.all()
    related = Project.objects.filter(category=project.category).exclude(pk=project.pk)[:3]

    context = {
        'project': project,
        'gallery': gallery,
        'related': related,
        'active_page': 'projects',
    }
    return render(request, 'core/project_detail.html', context)


def about(request):
    testimonials = Testimonial.objects.filter(is_active=True)

    context = {
        'testimonials': testimonials,
        'active_page': 'about',
    }
    return render(request, 'core/about.html', context)


def contact(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            _send_contact_notification(msg)
            messages.success(request, 'Your message has been sent! We\'ll get back to you within 24 hours.')
            return redirect('contact')

    context = {
        'form': form,
        'active_page': 'contact',
    }
    return render(request, 'core/contact.html', context)


# ── helpers ────────────────────────────────────────────────────────────────────

def _send_contact_notification(msg):
    """Email the admin when a new contact message arrives."""
    subject = f'[WoodCraft] New message from {msg.full_name}: {msg.subject}'
    body = (
        f'New contact message received on WoodCraft website.\n\n'
        f'Name:    {msg.full_name}\n'
        f'Phone:   {msg.phone_number}\n'
        f'Subject: {msg.subject}\n\n'
        f'Message:\n{msg.description}\n\n'
        f'---\nTo reply or manage: /admin/core/contactmessage/{msg.pk}/change/'
    )
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
        fail_silently=True,
    )