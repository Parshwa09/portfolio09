from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile, Skill, Project, Education, Experience, Contact
from .forms import ContactForm
import json

def home(request):
    """Home page view with all portfolio sections"""
    try:
        profile = Profile.objects.first()
        skills = Skill.objects.all()
        featured_projects = Project.objects.filter(featured=True)[:3]
        all_projects = Project.objects.all()[:6]
        education = Education.objects.all()
        experience = Experience.objects.all()
        
        # Group skills by category
        skills_by_category = {}
        for skill in skills:
            category = skill.get_category_display()
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        context = {
            'profile': profile,
            'skills_by_category': skills_by_category,
            'featured_projects': featured_projects,
            'all_projects': all_projects,
            'education': education,
            'experience': experience,
        }
        
        return render(request, 'details/home.html', context)
    except Exception as e:
        # Handle any errors gracefully
        context = {
            'error': f'Error loading portfolio data: {str(e)}'
        }
        return render(request, 'details/home.html', context)

def about(request):
    """About page view"""
    try:
        profile = Profile.objects.first()
        skills = Skill.objects.all()
        education = Education.objects.all()
        experience = Experience.objects.all()
        
        # Group skills by category
        skills_by_category = {}
        for skill in skills:
            category = skill.get_category_display()
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        context = {
            'profile': profile,
            'skills_by_category': skills_by_category,
            'education': education,
            'experience': experience,
        }
        
        return render(request, 'details/about.html', context)
    except Exception as e:
        context = {'error': f'Error loading about data: {str(e)}'}
        return render(request, 'details/about.html', context)

def projects(request):
    """Projects page view"""
    try:
        all_projects = Project.objects.all()
        featured_projects = Project.objects.filter(featured=True)
        
        context = {
            'all_projects': all_projects,
            'featured_projects': featured_projects,
        }
        
        return render(request, 'details/projects.html', context)
    except Exception as e:
        context = {'error': f'Error loading projects: {str(e)}'}
        return render(request, 'details/projects.html', context)

def project_detail(request, project_id):
    """Individual project detail view"""
    try:
        project = get_object_or_404(Project, id=project_id)
        related_projects = Project.objects.exclude(id=project_id)[:3]
        
        context = {
            'project': project,
            'related_projects': related_projects,
        }
        
        return render(request, 'details/project_detail.html', context)
    except Exception as e:
        messages.error(request, f'Error loading project: {str(e)}')
        return redirect('projects')

def skills(request):
    """Skills page view"""
    try:
        all_skills = Skill.objects.all()
        
        # Group skills by category
        skills_by_category = {}
        for skill in all_skills:
            category = skill.get_category_display()
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        context = {
            'skills_by_category': skills_by_category,
        }
        
        return render(request, 'details/skills.html', context)
    except Exception as e:
        context = {'error': f'Error loading skills: {str(e)}'}
        return render(request, 'details/skills.html', context)

from django.http import JsonResponse

def contact(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Save contact message to database
                contact_message = Contact(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    subject=form.cleaned_data['subject'],
                    message=form.cleaned_data['message']
                )
                contact_message.save()

                # Send email notification (optional - configure in settings)
                try:
                    send_mail(
                        f"Portfolio Contact: {form.cleaned_data['subject']}",
                        f"Name: {form.cleaned_data['name']}\n"
                        f"Email: {form.cleaned_data['email']}\n\n"
                        f"Message:\n{form.cleaned_data['message']}",
                        form.cleaned_data['email'],
                        ['your-email@example.com'],  # Replace with your email
                        fail_silently=True,
                    )
                except:
                    pass  # Email sending is optional

                # ✅ Return JSON if it's a fetch/AJAX request
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"success": True})
                else:
                    messages.success(request, 'Thank you for your message! I will get back to you soon.')
                    return redirect('contact')

            except Exception as e:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "error": str(e)})
                else:
                    messages.error(request, f'Error sending message: {str(e)}')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors})
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    # Normal GET: render template
    try:
        profile = Profile.objects.first()
        context = {
            'form': form,
            'profile': profile,
        }
        return render(request, 'details/contact.html', context)
    except Exception as e:
        context = {'form': form, 'error': f'Error loading contact data: {str(e)}'}
        return render(request, 'details/contact.html', context)


def api_skills(request):
    """API endpoint to get skills data as JSON"""
    try:
        skills = Skill.objects.all().values('name', 'category', 'proficiency')
        skills_data = list(skills)
        return JsonResponse({'skills': skills_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def api_projects(request):
    """API endpoint to get projects data as JSON"""
    try:
        projects = Project.objects.all().values(
            'id', 'title', 'description', 'technologies', 
            'project_url', 'github_url', 'status', 'featured'
        )
        projects_data = list(projects)
        return JsonResponse({'projects': projects_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)