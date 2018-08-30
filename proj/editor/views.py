from django.shortcuts import render
import os
import glob
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from django.shortcuts import redirect

@ensure_csrf_cookie
def page(request, page='view'):
    file = open('viewerapp/views.py', 'r')
    path = os.getcwd().split('/')[1:]
    path = path[path.index('Projects') + 1:]
    otherfiles = glob.glob("*")
    otherfiles = list(filter(lambda x: x.find('__') == -1, otherfiles))
    context = {'file': file.read(), 'path': path, 'otherfiles': otherfiles, 'filename': '/Users/svsaraf/Projects/slate/proj/viewerapp/views.py'}
    return render(request, 'editor/index.html', context)

def save(request):
    if request.method == 'POST' and request.is_ajax():
        filename = json.loads(request.body)['filename']
        file = open(filename, 'w')
        file.write(json.loads(request.body)['file'])
        file.close()
        return HttpResponse(json.dumps({'message': 'Wrote data to ' + filename}), content_type="application/json")
    else:
        return redirect('index')

def bounce(request):
    if request.method == 'POST' and request.is_ajax():
        os.system('sh restart.sh')
        print(os.getcwd())
        return HttpResponse(json.dumps({'val': 'bouncing'}), content_type="application/json")
    else:
        return redirect('index')

def cd(request):
    if request.method == 'POST' and request.is_ajax():
        values = json.loads(request.body)
        path = values['path']
        otherfiles = values['otherfiles']
        clicked = values['clicked']
        which = values['which']
        filetoopen = None
        filename = None
        if which == 'parent':
            if clicked == len(path) - 1:
                pass
                #parent directory is already selected
            else:
                path = path[:clicked+1]
                globpath = '/Users/svsaraf/Projects/' + '/'.join(path)
                otherfilesfullpaths = glob.glob(globpath + '/*')
                otherfiles = list(map(lambda x: x.split('/')[-1], otherfilesfullpaths))
                otherfiles = list(filter(lambda x: x.find('__') == -1, otherfiles))
        elif which == 'other':
            if otherfiles[clicked].find('.') != -1:
                filename = '/Users/svsaraf/Projects/' + '/'.join(path) + '/' + otherfiles[clicked]
                file = open(filename, 'r')
                filetoopen = file.read()
            else:
                path.append(otherfiles[clicked])
                globpath = '/Users/svsaraf/Projects/' + '/'.join(path)
                otherfilesfullpaths = glob.glob(globpath + '/*')
                otherfiles = list(map(lambda x: x.split('/')[-1], otherfilesfullpaths))
                otherfiles = list(filter(lambda x: x.find('__') == -1, otherfiles))
        return HttpResponse(json.dumps({'path': path, 'otherfiles': otherfiles, 'file': filetoopen, 'filename': filename}), content_type="application/json")
    else:
        return redirect('index')


# Create your views here.
