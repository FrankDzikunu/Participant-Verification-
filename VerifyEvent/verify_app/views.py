from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Participant
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def verify_participant(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            participant = Participant.objects.get(code=code)
            participant.status = True  # Set the status to verified
            participant.save()
            return JsonResponse({
                'status': 'success',
                'name': participant.name,
                'company': participant.company
            })
        except Participant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Participant not found.'})

    return render(request, "verify_app/verify.html")

@login_required
def manage_participants(request):
    if request.method == 'POST':
        if 'edit' in request.POST:
            participant_id = request.POST.get('id')
            participant = get_object_or_404(Participant, id=participant_id)
            participant.name = request.POST.get('name')
            participant.company = request.POST.get('company')
            participant.save()
        elif 'delete' in request.POST:
            code = request.POST.get('code')
            Participant.objects.filter(code=code).delete()
        elif 'add' in request.POST:
            name = request.POST.get('name')
            company = request.POST.get('company')
            code = request.POST.get('code')
            Participant.objects.create(name=name, company=company, code=code)
        elif 'toggle_status' in request.POST:  # Check for toggle status action
            participant_id = request.POST.get('toggle_status_id')
            participant = get_object_or_404(Participant, id=participant_id)
            participant.status = not participant.status  # Toggle status
            participant.save()

    participants = Participant.objects.all()
    return render(request, "verify_app/manage.html", {"participants": participants})

@login_required
def toggle_verification(request, participant_id):
    """
    Toggle the verification status of a participant.
    """
    participant = get_object_or_404(Participant, id=participant_id)
    participant.status = not participant.status  # Toggle the status
    participant.save()
    return redirect("manage_participants")  # Redirect to the management page

def admin_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('manage_participants')
        else:
            error = 'Invalid credentials'
    
    return render(request, 'admin_login.html', {'error': error})
