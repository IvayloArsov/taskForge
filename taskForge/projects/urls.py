from django.urls import path, include

from .views import ProjectDetailView, ProjectCreateView, ProjectListView, ProjectUpdateView, ProjectDeleteView

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='list'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('',ProjectDetailView.as_view(), name='details' ),
        path('edit/', ProjectUpdateView.as_view(), name='edit'),
        path('delete/', ProjectDeleteView.as_view(), name='delete')
    ]))
]
