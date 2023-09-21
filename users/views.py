from rest_framework import permissions
from rest_framework import generics
from users.serializers import *
from users.models import *
    

class RoleAPIListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    

