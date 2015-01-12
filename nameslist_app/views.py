from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404, HttpResponse
import json
import re

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
        name = models.Name(prospective_id=prospective, name=request.POST['name'], correct=True)
        name.save()
    except:
        prospective.delete()
        return send_status("fail")
    try:
        facts = []
        pattern = re.compile(r"^field_type_id(?P<field_type>\d)")
        for (key, field_type_response) in request.POST.items():
            field_type_id = pattern.match(key)
            if field_type_id:
                facts.append(models.Fact(
                    prospective_id=prospective,
                    fact_type_id=models.Fact_Type.objects.get(pk=int(field_type_id.group('field_type'))),
                    fact=field_type_response))
        models.Fact.objects.bulk_create(facts)
    except:
        prospective.delete()
        return send_status("fail")

    name.save()
    return send_status("success")


