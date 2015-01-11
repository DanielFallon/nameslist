from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response

from nameslist_app import models


def index(request):
    form_elements = models.Fact_Type.objects.filter(public=True)
    return render(request, 'index.html', {'form_elements': form_elements})

