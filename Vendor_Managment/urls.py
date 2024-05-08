
from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('VMapp.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls'))

     
]


