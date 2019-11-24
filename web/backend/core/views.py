from django.views.generic import ListView
from core.models import VirtualDataTable
from rest_framework.views import APIView
from rest_framework.response import Response

class DataList (ListView):
    model = VirtualDataTable 
    paginate_by = 25

class HellowView(APIView):
    def get(self, request):
        content = {'message' : 'Hello User!'}
        return Response(content)
