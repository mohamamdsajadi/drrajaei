import os
import random
import string

from django.core.files.storage.filesystem import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from drRajaei import settings


@csrf_exempt
def add_excel_file(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file_']
            grouped_file_path = 'grouped_files', file.name.split('-')[0].split('.')[0]
            path = os.path.join(settings.MEDIA_ROOT, *grouped_file_path)
            fs = FileSystemStorage(location=path)
            fs2 = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT))
            file_name = fs.save(file.name, file)
            hashed_file = fs2.save(
                ''.join(random.choices(string.ascii_letters, k=11)) + '.' + file.name.split('.')[-1], file)
        except Exception as e:
            return HttpResponse(str(e))
        else:
            return JsonResponse({
                'clear_file_address': request.build_absolute_uri(fs.url(os.path.join(*grouped_file_path, file_name))),
                'hashed_address': request.build_absolute_uri(fs2.url(hashed_file))
            })


@csrf_exempt
def hi(request):
    return JsonResponse({'clear_file_address': "+"})


@csrf_exempt
def download_file(request, file_path):
    full_file_path = os.path.join(settings.BASE_DIR, *file_path.split('/'))
    if not os.path.exists(full_file_path):
        return HttpResponse(status=404)
    with open(full_file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(full_file_path)
        return response
