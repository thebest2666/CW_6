from django.forms import ModelForm

from blog.models import Blog
from mailings.forms import StyleMixin


class BlogForm(StyleMixin, ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "description", "photo")