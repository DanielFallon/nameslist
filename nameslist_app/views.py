from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404, HttpResponse
import json

# Create your views here.
from django.shortcuts import render_to_response

from nameslist_app import models


def index(request):
    form_elements = models.Fact_Type.objects.filter(public=True)
    return render(request, 'index.html', {'form_elements': form_elements})


def submit(request):
    prospective = models.Prospective()
    prospective.save()

    def send_status(status):
        response = {'status': status}
        return HttpResponse(json.dumps(response), content_type="application/json")

    try:
        name = models.Name(prospective_id=prospective.id, name=request.POST['name'], correct=True)
    except:
        prospective.delete()
        send_status("fail")
    try:
        models.Fact.bulk_create(
            [models.Fact(prospective_id=prospective.id, fact_type_id=field_type_id, fact=field_type_response)
             for (field_type_id, field_type_response) in request.POST['field_type_id'].items()])
    except:
        prospective.delete()
        send_status("fail")

    name.save()
    send_status("success")


