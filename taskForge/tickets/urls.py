from django.urls import path, include
from .views import (
    TicketListView,
    TicketDetailView,
    TicketCreateView,
    TicketUpdateView, TicketDeleteView, BugReportCreateView, BugReportApproveView, BugReportDenyView,
    BugReportDetailView
)

app_name = 'tickets'

urlpatterns = [
    path('', TicketListView.as_view(), name='list'),
    path('create/', TicketCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('', TicketDetailView.as_view(), name='details'),
        path('edit/', TicketUpdateView.as_view(), name='edit'),
        path('delete/', TicketDeleteView.as_view(), name='delete')
    ])),
    path('report-bug/', BugReportCreateView.as_view(), name='report-bug'),
    path('bugs/<int:pk>', include([
        path('approve/', BugReportApproveView.as_view(), name='approve-bug'),
        path('deny/', BugReportDenyView.as_view(), name='deny-bug'),
        path('', BugReportDetailView.as_view(), name='bug-details')
    ]))
]
