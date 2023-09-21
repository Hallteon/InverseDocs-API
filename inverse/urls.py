"""
URL configuration for HelloDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from inverse.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import *
from documents.views import *

schema_view = get_schema_view(
   openapi.Info(
      title='Inverse Docs API',
      default_version='v1',
      description='Платформа для работы с документами',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='belogurov.ivan@list.ru'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Documents
    path('api/documents/', DocumentAPIListView.as_view()),
    path('api/documents/create/', DocumentAPICreateView.as_view()),
    path('api/documents/<int:pk>/', DocumentAPIDetailView.as_view()),
    path('api/documents/<int:pk>/approve/', DocumentAPIApproveView.as_view()),
    path('api/documents/<int:pk>/annule/', DocumentAPIAnnuleView.as_view()),
    path('api/documents/contractors/<int:pk>/approve/', DocumentAPIContractorApproveListView.as_view()),
    path('api/documents/contractors/<int:pk>/annule/', DocumentAPIContractorAnnuleListView.as_view()),
    path('api/documents/statuses/<int:pk>/', DocumentAPIStatusListView.as_view()),
    path('api/documents/statuses/<int:pk>/recievers/', DocumentAPIListRecieversView.as_view()),
    path('api/documents/statuses/', DocumentStatusAPIListView.as_view()),
    path('api/documents/products/create/', ProductAPICreateView.as_view()),
    path('api/documents/contractors/inn/<str:inn>/', ContractorAPIRetrieveView.as_view()),
    path('api/documents/contractors/', ContractorAPIListView.as_view()),
    path('api/documents/contractors/create/', ContractorAPICreateView.as_view()),
    path('api/documents/categories/', DocumentCategoryAPIListView.as_view()),
    # path('api/documents/filter/', DocumentAPIFilterListView.as_view()),

    # Users
    path('api/users/roles/', RoleAPIListView.as_view()),
    path('api/users/auth/', include('djoser.urls')),
    re_path(r'^api/users/auth/', include('djoser.urls.authtoken')),

    # Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)