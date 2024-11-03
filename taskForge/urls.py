from django.contrib import admin
from django.urls import path, include

from taskForge.views import Index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('accounts/', include('taskForge.accounts.urls'))
]
