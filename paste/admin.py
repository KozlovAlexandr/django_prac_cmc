from django.contrib import admin

from .models import Paste, PasteCatalog, Lang

admin.site.register(Paste)
admin.site.register(PasteCatalog)
admin.site.register(Lang)

# Register your models here.
