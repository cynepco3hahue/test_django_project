from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from log_collector.forms import HostForm
from log_collector.models import Log

# Create your views here.


class IndexView(generic.CreateView):
    form_class = HostForm
    template_name = 'log_collector/index.html'

    def get_success_url(self):
        return reverse('log_collector:index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['log_files'] = Log.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if "_add_host" in request.POST:
            host_form = HostForm(request.POST)
            if host_form.is_valid():
                return self.form_valid(host_form)
            else:
                return HttpResponseRedirect(reverse('log_collector:index'))
        if "_get_logs" in request.POST:
            return reverse('log_collector:index')




# def main_page(request):
#     context_object_name = 'log_files'
#
#     if request.POST:
#         if '_add_host' in request.POST:
#             return
#         elif '_get_logs' in request.POST:
#             return
#     return render(request, 'log_collector/index.html')