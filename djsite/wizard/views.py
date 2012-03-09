# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core import serializers
from distutils.sysconfig import get_python_lib
import os, shutil, datetime
import djos
from models import Project, Temp
from forms import ProjectForm

def welcome(request):
    vars = {}
    vars['template']   = 'content/welcome.html'
    vars['next']       = 'project-details'
    vars['scantailor'] = djos.is_scantailor()
    return render_to_response(vars['template'], {'vars': vars})

def mountpoint(request):
    state = request.GET.get('state','before')
    vars = {}
    vars['template']   = 'content/get-mountpoint.html'
    
    if state == 'before':
        request.session['mounted_before'] = djos.get_drives()
        vars['instructions'] = '' 
    else:
        request.session['mounted_after'] = djos.get_drives() 
        vars['path'] = djos.get_mountpoint(request)
    
    return render_to_response(vars['template'], {'vars': vars})


def project_details(request):
    vars = {}
    vars['template'] = 'content/project-details.html'
    vars['previous'] = '/'
    vars['next']     = '/import-gui'
    vars['redirect'] = vars['next'] 
    vars['path'] = request.session.get('path',djos.project_path())
    #vars['debug']    = True
    form = ProjectForm(initial={'date_created': datetime.datetime.now(), 'path': vars['path']})
    
    # submitting
    if request.method == 'POST': 
        sess = request.session.get('title', False)
        if sess: # old
            p = Project.objects.get(title=request.session['title'])
            form = ProjectForm(request.POST, instance=p)
        elif not sess: # new
            form = ProjectForm(request.POST)
        if form.is_valid(): # new and old
            form.save()
            request.session['title'] = form.cleaned_data['title']
            request.session['path'] = form.cleaned_data['path']
            request.session['fullpath'] = request.session.get('path','Error') + os.sep + request.session.get('title','Error')
            return HttpResponseRedirect(vars['redirect'])
    # displaying
    elif request.session.get('title', False): # old
        try:
            p = Project.objects.get(title=request.session['title'])
            form = ProjectForm(instance=p)
        except ObjectDoesNotExist:
            vars['errors'] = {'Missing title': 'I could not find this title for some reason! Please enter a different title.'}
            request.session.pop('title')
            request.session.pop('path')
            request.session.pop('fullpath')
        except MultipleObjectsReturned:
            vars['errors'] = {'Too many titles': 'There were too many projects with this name. That should not happen. Please enter a different title.'}
            request.session.pop('title')
            request.session.pop('path')
            request.session.pop('fullpath')
        except:
            vars['errors'] = {'oops': 'I received some unexpected, unknown error. You might want to report this.'}
    else: # new
        pass
    return render_to_response(vars['template'], {'form': form, 'vars': vars})

def import_gui(request):
    vars = {}
    vars['template'] = 'content/import-gui.html'
    vars['previous'] = '/project-details'
    vars['next']     = '/scantailor'
    vars['redirect'] = vars['next']
    vars['projectpath'] = request.session.get('path','Error') + os.sep + request.session.get('title','Error')
    #vars['debug']    = True
    form             = []
    return render_to_response(vars['template'], {'form': form, 'vars': vars})

def import_cmd(request):
    src              = request.GET['src'] # intentionally cause error if not provided
    src              = src.replace('%3A',':').replace('%5C','\\').replace('%2F','/')
    dst              = request.session['fullpath']
    card             = request.GET['card']
    vars             = {}
    vars['template'] = 'content/import-cmd.html'
    vars['output']   = djos.import_pages(Temp, src, dst, card)
    return HttpResponse(vars['output'])

def import_cmd_is_valid(request):
    src              = request.GET['src'] # intentionally cause error if not provided
    src              = src.replace('%3A',':').replace('%5C','\\').replace('%2F','/').replace('+',' ')
    types            = ('jpg', 'jpeg', 'tif', 'tiff', 'png', 'jp2')
    photos           = False
    try:
        files = os.listdir(src.replace('\\','/')) # eg 'e:/dcim'
        for item in files:
            i = item.split('.')
            ext = i[-1] # -1 returns last part
            if ext.lower() in types:
                photos = True
        if photos:
            return HttpResponse('[{"success": "Valid path."}]') # JSON syntax
        else:
            return HttpResponse('[{"error": "No images found."}]') # JSON syntax
    except:
        result = '[{"error": "This directory does not exist."}]' # JSON syntax
    return HttpResponse(result)
    
def import_cmd_get_progress(request):
    vars             = {}
    vars['template'] = 'content/import-cmd-get-progress.html'
    vars['output']    = serializers.serialize('json', Temp.objects.all())
    return HttpResponse(vars['output']) #render_to_response(vars['template'], {'vars': vars})

def scantailor(request):
    vars = {}
    vars['template'] = 'content/scantailor.html'
    vars['previous'] = '/import-gui'
    vars['next']     = '/scantailor'
    vars['redirect'] = vars['next']
    vars['projectpath'] = request.session.get('path','Error') + os.sep + request.session.get('title','Error')
    #vars['debug']    = True
    form             = []
    return render_to_response(vars['template'], {'form': form, 'vars': vars})
