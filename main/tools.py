import os.path

from django.utils.deconstruct import deconstructible
from uuid import uuid4


@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path, use_instance=False):
        self.sub_path = path
        self.use_instance = use_instance

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        if len(ext) >= 4:
            if ext[:4] == "jpeg":
                ext = "jpg"
        if self.use_instance and instance.pk:
            filename = f"{uuid4().hex}.{ext}"
            return os.path.join(self.sub_path, str(instance.pk), filename)
        else:
            filename = f"{uuid4().hex}.{ext}"
            return os.path.join(self.sub_path, filename)
