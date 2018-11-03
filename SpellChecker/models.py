from django.contrib.auth.models import User
from django.db import models
from SpellChecker.validators import validate_file_contents


class DocumentsQuerySet(models.QuerySet):
    def get_documents_for(self, user):
        assert isinstance(user, User)
        return self.filter(user=user)

class Document(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, blank=True)
    document = models.FileField(upload_to='documents/', validators=[validate_file_contents])
    user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    objects = DocumentsQuerySet.as_manager()



