import os
import shutil
from log_collector import help_methods
from log_collector import constants
from django.core.urlresolvers import reverse
import django.core.exceptions as errors
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib import messages

from log_collector.forms import HostForm
from log_collector.models import Log, Host

# Create your views here.


class IndexView(generic.CreateView):
    form_class = HostForm
    template_name = 'log_collector/index.html'

    def get_success_url(self):
        return reverse('log_collector:index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['log_files'] = Log.objects.all()
        context['hosts'] = Host.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if "_add_host" in request.POST:
            if Host.objects.all().count() == 10:
                message = ("You can't add more than ten hosts,"
                           " please remove some hosts")
                messages.add_message(request, messages.WARNING, message)
                return HttpResponseRedirect(reverse("log_collector:index"))
            host_form = HostForm(request.POST)
            if host_form.is_valid():
                return self.__add_host(host_form)
        elif "_get_logs" in request.POST:
            local_path = help_methods.generate_new_folder(
                constants.LOCAL_LOG_DIR
            )
            try:
                self.__download_via_ssh(request, local_path)
            except help_methods.ConnectionException as e:
                shutil.rmtree(local_path)
                messages.add_message(request, messages.ERROR, e)
                return HttpResponseRedirect(reverse("log_collector:index"))
            archive_name = ".".join([local_path, 'zip'])
            io_bytes = help_methods.zip_dir(local_path)
            response = HttpResponse(
                io_bytes.getvalue(),
                content_type='application/x-zip-compressed'
            )
            response['Content-Disposition'] = (
                'attachment; filename="%s"' % archive_name
            )
            hosts = Host.objects.all()
            for host in hosts:
                host.delete()
            return response
        elif "_delete_hosts" in request.POST:
            hosts_to_delete = request.POST.getlist('hosts[]')
            for host in hosts_to_delete:
                Host.objects.filter(host_name=host).delete()
            return HttpResponseRedirect(reverse("log_collector:index"))

    def __add_host(self, host_form):
        """
        Handle add host request
        :param host_form: instance of HostForm
        :return: instance of HttpResponseRedirect
        """
        try:
            host_object = Host.objects.get(
                host_name=host_form.cleaned_data['host_name']
            )
            for field in host_form.cleaned_data:
                setattr(
                    host_object, field, host_form.cleaned_data[field]
                )
            host_object.save()
            return HttpResponseRedirect(reverse('log_collector:index'))
        except errors.ObjectDoesNotExist:
            return self.form_valid(host_form)

    @classmethod
    def __download_via_ssh(cls, request, local_path):
        """
        Download log files from remote machines on local machine via ssh

        :param request: Instance of request
        :param local_path: local path to save fiels
        :return: local directory path, where all logs
        """
        hosts = request.POST.getlist('hosts[]')
        logs = request.POST.getlist('logs[]')
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        for host_name in hosts:
            host_object = Host.objects.get(host_name=host_name)
            host_path = os.path.join(local_path, host_name)
            if not os.path.exists(host_path):
                os.makedirs(host_path)
            for log_name in logs:
                log_object = Log.objects.get(log_name=log_name)
                help_methods.get_file_via_ssh(
                    getattr(log_object, 'log_path'), host_path,
                    getattr(host_object, 'host_name'),
                    getattr(host_object, 'host_root_user'),
                    getattr(host_object, 'host_root_password')
                )
