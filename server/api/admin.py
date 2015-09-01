from django.contrib import admin
from .models import Composition, Contest, Vote, Content

admin.site.register(Content)
admin.site.register(Composition)
admin.site.register(Contest)
admin.site.register(Vote)
