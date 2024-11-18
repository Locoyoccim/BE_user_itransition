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
    
@csrf_exempt
def user_path(request, id):
    if request.method == 'PUT':
        return update_user(request, id)

def delete_user(request):
    data = json.loads(request.body)
    for item in data:
        user = get_object_or_404(User, id = item["id"])
        user.delete()

    return JsonResponse(f'Eliminación exitosa', safe=False)

# funciones user_path
def update_user(request, id):
    user = get_object_or_404(User, id=id)
    data = json.loads(request.body)

    user.blocked = data['blocked']
    user.last_seen = data['last_seen']

    response = {
        'id': user.id,
        'last_seen': user.last_seen,
        'blocked': user.blocked
    }

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