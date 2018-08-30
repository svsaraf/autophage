from django.shortcuts import render

def view(request):
    context = {}
    testvalue = 4777
    return render(request, 'viewerapp/view.html', {})