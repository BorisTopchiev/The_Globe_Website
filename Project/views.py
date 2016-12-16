from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt


def header(request):
    return render_to_response('header.html')

def materials_page(request):
    return render_to_response('materials_page.html')