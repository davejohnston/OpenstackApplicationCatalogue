import logging
import sys

from horizon import views

#from .stack import Stack

from openstack_dashboard import api
from horizon import exceptions
from horizon import forms
from horizon import messages

from django.views.generic.base import View
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import json

LOG = logging.getLogger(__name__)

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'project/applications/index.html'

    def get_data(self, request, context, *args, **kwargs):

        application_json=open('/etc/catalogue/db/app.json')
        applications = json.load(application_json)
        paginator = Paginator(applications, 9)
        page = request.GET.get('page')

        try:
            stacks = paginator.page(page)
        except PageNotAnInteger:
            stacks = paginator.page(1)
        except EmptyPage:
            stacks = paginator.page(paginator.num_pages)

        context['stacks'] = stacks 
        return context

class ApplicationDetailedView(views.APIView):

    template_name = 'project/applications/application_detail.html'

    def get_data(self, request, context, *args, **kwargs):

        application_json=open('/etc/catalogue/db/app.json')
        applications = json.load(application_json)

        app_id = request.GET.get('id')

        for app in applications:
            if app['id'] == app_id:
                context['application'] = app

        return context

class ApplicationLaunchView(views.APIView):

    template_name = 'project/applications/application_launch.html'

    def get_data(self, request, context, *args, **kwargs):

        application_json=open('/etc/catalogue/db/app.json')
        applications = json.load(application_json)

        network_list = api.neutron.network_list_for_tenant(
                request,
                request.user.tenant_id)

        subnet_list = api.neutron.subnet_list(request)

        app_id = request.GET.get('id')

        for app in applications:
            if app['id'] == app_id:
                context['application'] = app

        context['networks'] = network_list
        context['subnets'] = subnet_list
        context['my_id'] = request.user.tenant_id
        context['my_name'] = request.user.tenant_name
        context['my_key'] = request.user
        return context

class ApplicationStackLaunchView(views.APIView):

    template_name = 'project/applications/application_launch.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            # Need to grab the context 
            # if nil redirect, otherwise do something else
            #
            context = self.post_data(request, context, *args, **kwargs)
        except Exception:
            exceptions.handle(request)

        if context.has_key('redirect_url'):
            redirect_url = context['redirect_url']
            return HttpResponseRedirect(redirect_url)
        else:
            return self.render_to_response(context)

    def post_data(self, request, context, *args, **kwargs):

        application_json=open('/etc/catalogue/db/app.json')
        applications = json.load(application_json)

        params = dict()

        app_id = request.POST.get('id')
        app = None
        for app in applications:
            if app['id'] == app_id:
                for param in app['map']:
                    params[param['name']] = request.POST.get(param['name'])
                break;

        

        fields = {
            'stack_name': request.POST.get('stack_name'),
            'timeout_mins': '60',
            'disable_rollback': 'true', 
            'parameters': params,
            'template_url' : request.build_absolute_uri(app['template_url'])
        }

        try:
            data = api.heat.stack_create(request, **fields)
            stack_id = data['stack']['id']
            stack_url = '/project/stacks/stack/%s' % stack_id
            context['redirect_url'] = stack_url
            messages.success(request, "Stack creation started.")
        except Exception as e:
            exceptions.handle(request, e or _('Stack creation failed.'))


        context['submitted'] = params
        return context

    def get_data(self, request, context, *args, **kwargs):
        return context
