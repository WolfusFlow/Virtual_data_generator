from django.views.generic import ListView
from core.models import Data

class DataList(ListView):
    model = Data