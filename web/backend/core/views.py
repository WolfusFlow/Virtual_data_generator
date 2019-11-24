from django.views.generic import ListView
from core.models import VirtualDataTable

class DataList (ListView):
    model = VirtualDataTable 