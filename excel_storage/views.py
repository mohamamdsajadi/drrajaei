import os

from django.core.files.storage.filesystem import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from drRajaei import settings


@csrf_exempt
def add_excel_file(request):
    if request.method == 'POST':
        file = request.FILES['excel']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,
                                                     'grouped_files',
                                                     file.name.split('.')[0]))
        fs2 = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'XVGSAWE'))
        file_name = fs.save(file.name, file)
        hashed_file = fs2.save(hash(file.name), file)
        return JsonResponse({'clear_file_address': request.build_absolute_uri(fs.url(file_name)),
                             'hashed_address': request.build_absolute_uri(fs2.url(hashed_file))})
