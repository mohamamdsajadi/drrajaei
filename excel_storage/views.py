import os
import shutil

from django.core.files.storage.filesystem import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from drRajaei import settings


@csrf_exempt
def add_excel_file(request):
    if request.method == 'POST':
        file = request.FILES['excel']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'X'))
        fs2 = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'Y'))
        file_name = fs.save(file.name, file)
        fs2.save(file.name, file)
        return JsonResponse({'address': request.build_absolute_uri(fs.url(file_name)) })