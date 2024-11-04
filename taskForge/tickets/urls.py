from django.urls import path, include
from .views import (
    TicketListView,
    TicketDetailView,
    TicketCreateView,
    TicketUpdateView, TicketDeleteView
)

app_name = 'tickets'

urlpatterns = [
    path('', TicketListView.as_view(), name='list'),
    path('create/', TicketCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('', TicketDetailView.as_view(), name='details'),
        path('edit/', TicketUpdateView.as_view(), name='edit'),
        path('delete/', TicketDeleteView.as_view(), name='delete')
    ]))
]
