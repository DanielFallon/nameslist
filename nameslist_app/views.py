from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404, HttpResponse
from nameslist_app.models import Prospective,Name
import json
import re

# Create your views here.
from django.shortcuts import render_to_response

from nameslist_app import models


def index(request):
    form_elements = models.Fact_Type.objects.filter(public=True)
    return render(request, 'index.html', {'form_elements': form_elements})


def send_status(status, message):
    response = {'status': status, 'message': message}
    return HttpResponse(json.dumps(response), content_type="application/json")


def submit(request):
    prospective = models.Prospective()
    prospective.save()

    try:
        name = models.Name(prospective_id=prospective, name=request.POST['name'], correct=True)
        name.save()
    except:
        prospective.delete()
        return send_status("fail", "Prospectives need a name")
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
        return send_status("fail", "Creation Failed")

    name.save()
    return send_status("success", "Creation succeeded")

@login_required
def profile(request, prospective_id):
    prospective = Prospective.objects.get(pk=int(prospective_id))
    return render(request, 'profile.html', {'prospective': prospective})


def photo(request, *args, prospective_id=None, photo_id=None, action=None):
    # if we got a photo id, return that photo
    prospective = Prospective.objects.get(pk=prospective_id)
    if photo_id:
        photo_obj = prospective.photo_set.get(pk=int(photo_id))
        if photo_obj:
            output = photo_obj.to_json()
            output["status"] = 'success'
            output["message"] = 'photo retrieved'
            return HttpResponse(json.dumps(output), content_type="application/json")
        else:
            output = {'status': 'failed', 'message': 'No such photo'}
            return HttpResponse(json.dumps(output), content_type="application/json")
        pass
    # if we got an action, perform it
    if action:
        if action == "add":
            try:
                photo_obj = models.Photo(prospective_id=prospective,
                                         user_id=request.user,
                                         url=request.POST['url'],
                                         primary=bool(request.POST.items.get('primary')),
                                         )
                photo_obj.save()
                return send_status('success', 'Photo Added')
            except:
                return send_status('fail', 'Photo addition failed')
        if action == "delete":
            print("Delete currently unsupported")
            pass
        if action == "list":
            try:
                output = {'status': 'success', 'message': 'Photos Added', 'photo_list':
                    [prospective_photo.to_json() for prospective_photo in prospective.photo_list]
                }
                return HttpResponse(json.dumps(output),
                                    content_type="application/json")
            except:
                return send_status('fail', 'Cannot get list')

    # otherwise, return the best photo
    photo_obj = prospective.photo
    if photo_obj:
        output = photo_obj.to_json()
        output["status"] = 'success'
        output["message"] = 'photo retrieved'
        return HttpResponse(json.dumps(output), content_type="application/json")
    else:
        output = {'status': 'failed', 'message': 'No best photo'}
        return HttpResponse(json.dumps(output), content_type="application/json")


def name(request, prospective_id, action=None):
    if action:
        # accept the posted image
        pass
    # Otherwise return the correct name
    pass


def fact(request, prospective_id, action=None, fact_id=None):
    if action:  # must be add due to the regex
        # add a fact to the prospective
        pass
    if fact_id:
        # return just that fact_id
        pass
    # otherwise return a list of all the facts
    pass


def opinion(request, prospective_id, action=None, opinion_id=None):
    if action:  # must be add due to the regex
        # add a opinion to the prospective
        pass
    if opinion_id:
        # return just that opinion_id
        pass
    # otherwise return a list of all the opinions
    pass


def list_debug(request):
    prospectiveList = Prospective.objects.all()
    print(prospectiveList[0].name_list)
    return render_to_response('list.html')