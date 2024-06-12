# repairs/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from pymongo import MongoClient
from bson import ObjectId

# MongoDB setup - Replace with MongoDB info from Declann
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
repairs_collection = db['repairs']

def repair_form(request, repair_id):
    return render(request, 'repairs/repair_form.html', {'repair_id': repair_id})

@require_http_methods(["PATCH", "POST"])
def update_repair_status_and_steps(request, repair_id):
    try:
        repair = repairs_collection.find_one({'_id': ObjectId(repair_id)})
        if not repair:
            return JsonResponse({'error': 'Repair not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    if request.method == "POST":
        data = {
            'status': request.POST.get('status'),
            'steps': request.POST.get('steps')
        }
    else:
        data = json.loads(request.body)

    repair_status = data.get('status')
    repair_steps = data.get('steps')

    update_data = {}
    if repair_status:
        update_data['status'] = repair_status
    if repair_steps:
        update_data['steps'] = repair_steps

    try:
        result = repairs_collection.update_one(
            {'_id': ObjectId(repair_id)},
            {'$set': update_data}
        )
        if result.matched_count == 0:
            return JsonResponse({'error': 'Repair not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Repair updated successfully'}, status=200)

def home(request):
    return render(request, 'home.html')
