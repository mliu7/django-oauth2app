from django.forms import fields

from oauth2app.validators import CustomURLValidator


class CustomURLFormField(fields.URLField):
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(fields.URLField, self).__init__(max_length, min_length, *args, **kwargs)
        self.validators.append(CustomURLValidator())
