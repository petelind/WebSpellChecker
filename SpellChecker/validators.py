from binaryornot.check import is_binary
from django.core.files.base import ContentFile
import os
import mimetypes
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.forms import FileField


def validate_file_contents(upload: FileField):
    tmp_path = 'tmp/%s' % upload.name
    default_storage.save(tmp_path, ContentFile(upload.file.read()))
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
    default_storage.save(tmp_path, ContentFile(upload.file.read()))
    result = mimetypes.guess_type(full_tmp_path)
    heuristics_result = is_binary(full_tmp_path)
    if result[0] == 'text/plain' and heuristics_result is False:
        default_storage.delete(full_tmp_path)
        return
    else:
        default_storage.delete(tmp_path)
        raise ValidationError('As of now only text files as supported!')