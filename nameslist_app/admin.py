from django.contrib import admin
from nameslist_app.models import Prospective,Name,Photo

# Register your models here.
class NameInline(admin.TabularInline):
    model = Name

class PhotoInline(admin.TabularInline):
    model = Photo
class ProspectiveAdmin(admin.ModelAdmin):
    inlines = [NameInline,PhotoInline]
admin.site.register(Prospective,ProspectiveAdmin)