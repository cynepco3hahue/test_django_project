from django import forms
from log_collector.models import Host


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['host_name', 'host_root_user', 'host_root_password']
        widgets = {'host_root_password': forms.PasswordInput()}
