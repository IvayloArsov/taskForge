from django.contrib import admin
from django.urls import path, include

from taskForge.views import Index, AboutView, ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('accounts/', include('taskForge.accounts.urls')),
    path('projects/', include('taskForge.projects.urls')),
    path('tickets/', include('taskForge.tickets.urls')),
    path('comments/', include('taskForge.comments.urls'))
]
