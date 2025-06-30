from django.urls import path
from scheduler import views

urlpatterns = [
    path('providers/', views.ProviderCreateView.as_view()),
    path('providers/<int:provider_id>/availability', views.ProviderAvailabilityCreateView.as_view()),
    path('providers/<int:provider_id>/availability/slots', views.ProviderAvailableSlotsView.as_view()),
    path('appointments', views.AppointmentCreateView.as_view()),
    path('providers/<int:provider_id>/appointments', views.ProviderAppointmentsView.as_view()),
]
