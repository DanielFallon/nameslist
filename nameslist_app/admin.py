from django.contrib import admin
from nameslist_app.models import Prospective, Name, Photo, Fact_Type, Fact


# Register your models here.
class FactInline(admin.TabularInline):
    model = Fact

class NameInline(admin.TabularInline):
    model = Name


class PhotoInline(admin.TabularInline):
    model = Photo


class ProspectiveAdmin(admin.ModelAdmin):
    inlines = [NameInline, PhotoInline, FactInline]


admin.site.register(Prospective, ProspectiveAdmin)

admin.site.register(Fact_Type)