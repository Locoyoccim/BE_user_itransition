from django.shortcuts import render
import json
from .models import User
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def get_users(request):
    if request.method == 'GET':
        user_list = list(User.objects.all().values())
        return JsonResponse(user_list, safe=False)
    elif request.method == 'POST':
        return create_user(request)
    elif request.method == "DELETE":
        return delete_user(request)
    elif request.method == "PUT":
        return update_user(request)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        return login_user(request)
    
#funciones url users
def delete_user(request):
    data = json.loads(request.body)
    for item in data:
        user = get_object_or_404(User, id = item["id"])
        user.delete()

    return JsonResponse(f'Eliminación exitosa', safe=False)

def update_user(request):
    data = json.loads(request.body)

    response = []

    for item in data:
        user = get_object_or_404(User, id=item["id"])
        user.blocked = item['blocked']
        user.updated_at = item['updated_at']
        user.save()

        response.append ({
            'id': user.id,
            'updated_at': user.updated_at,
            'blocked': user.blocked
        })

    return JsonResponse(response, safe=False)

def create_user(request):
    data = json.loads(request.body)

    created_date = datetime.now()

    new_user = User.objects.create(
        name=data['name'],
        company=data['company'],
        position=data['position'],
        email=data['email'],
        last_seen=data['last_seen'],
        created_at=created_date,
        updated_at=created_date,
        blocked=data['blocked'],
    )

    response = {
        'id': new_user.id,
        'name': new_user.name,
        'company': new_user.company,
        'position': new_user.position,
        'email': new_user.email,
        'last_seen': new_user.last_seen,
        'created_at': new_user.created_at,
        'update_at': new_user.updated_at,
        'blocked': new_user.blocked,
    }

    return JsonResponse(response, safe=False, status=201)

# FUNCIONES LOGIN
def login_user(request):
    data = json.loads(request.body)
    email = data.get('email')

    if not email:
        return JsonResponse("Email is required", status=400)
    
    user = User.objects.filter(email=email).first()
    
    if user is None:
        return JsonResponse("User not found", status=404)
    elif user.blocked:
        return JsonResponse("This user are blocked, call admin", safe=False, status=401)

    user.last_seen = datetime.now()
    user.save()

    return JsonResponse({'message': 'Login exitoso'}, status=200)