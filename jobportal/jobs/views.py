from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, JobForm, ApplicationForm
from .models import Job, Application, Profile
from django.contrib.auth.models import User
from django.db.models import Q

# Registration Form where new user will be created
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, role=form.cleaned_data['role'])
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# Login Form where existing user will enter
# But the existing username and password should exist in the database
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # However, redirect will depend on the role of the user
            return redirect('dashboard')
    return render(request, 'login.html')

# Logout View using the logout module from Django.contrib.auth package
def logout_view(request):
    logout(request)
    return redirect('login')

# The dashboard method will redirect to the dashboard based on the role
@login_required
def dashboard(request):
    role = request.user.profile.role
    if role == 'employer':
        return redirect('employer_dashboard')
    else:
        return redirect('applicant_dashboard')

# Dashboard for Employer
@login_required
def employer_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'employer_dashboard.html', {'jobs': jobs})

# Employer Only - Method for Posting Job
@login_required
def post_job(request):
    if request.user.profile.role != 'employer':
        return redirect('dashboard')
    form = JobForm(request.POST or None)
    if form.is_valid():
        job = form.save(commit=False)
        job.posted_by = request.user
        job.save()
        return redirect('employer_dashboard')
    return render(request, 'post_job.html', {'form': form})

# Employer Only - Method for Viewing the Applicant for the Employer
@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    applications = Application.objects.filter(job=job)
    return render(request, 'view_applicants.html', {'job': job, 'applications': applications})

# Dashboard for Applicant
@login_required
def applicant_dashboard(request):
    if request.user.profile.role != 'applicant':
        return render(request, 'unauthorized.html')

    status_filter = request.GET.get('status')
    applications = Application.objects.filter(applicant=request.user)

    if status_filter in ['pending', 'approved', 'rejected']:
        applications = applications.filter(status=status_filter)

    return render(request, 'applicant_dashboard.html', {
        'applications': applications,
        'status_filter': status_filter
    })

# Both Classes - Method for Searching Job
@login_required
def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        )
    return render(request, 'job_list.html', {'jobs': jobs})

# Both Classes - Method for getting info on a Job
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

# Applicant Only - Method for Applying for a Job
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('applicant_dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})

# Employee Only - Method for Reviewing Applications
@login_required
def review_applications(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if application.job.posted_by != request.user:
        return render(request, 'unauthorized.html')

    if request.method == 'POST':
        decision = request.POST.get('decision')
        if decision in ['Approved', 'Rejected']:
            application.status = decision
            application.save()
            return redirect('view_applicants', job_id=application.job.id)

    return render(request, 'review_applications.html', {'application': application})
