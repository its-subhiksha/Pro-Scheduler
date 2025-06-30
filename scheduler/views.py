from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Provider, Availability,Appointment
from .serializers import AvailabilitySerializer, AppointmentSerializer, ProviderSerializer
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.db import transaction

class ProviderCreateView(APIView):
    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ProviderAvailabilityCreateView(APIView):
    def post(self, request, provider_id):
        provider = get_object_or_404(Provider, id=provider_id)
        data = request.data.copy()
        data['provider'] = provider.id

        serializer = AvailabilitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderAvailableSlotsView(APIView):
    def get(self, request, provider_id):
        provider = get_object_or_404(Provider, id=provider_id)
        duration = int(request.query_params.get('duration', 30))  # in minutes

        availabilities = Availability.objects.filter(provider=provider)
        appointments = Appointment.objects.filter(provider=provider)

        slots = []

        for availability in availabilities:
            slot_start = availability.start_time
            slot_end = availability.end_time

            while slot_start + timedelta(minutes=duration) <= slot_end:
                overlap = appointments.filter(
                    start_time__lt=slot_start + timedelta(minutes=duration),
                    end_time__gt=slot_start
                )
                if not overlap.exists():
                    slots.append(slot_start.isoformat())
                slot_start += timedelta(minutes=duration)

        return Response(slots, status=status.HTTP_200_OK)
    
    
class AppointmentCreateView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                provider_id = serializer.validated_data['provider'].id
                start_time = serializer.validated_data['start_time']
                end_time = serializer.validated_data['end_time']

                conflict = Appointment.objects.select_for_update().filter(
                    provider_id=provider_id,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                )
                if conflict.exists():
                    return Response({"detail": "Slot already booked."}, status=status.HTTP_409_CONFLICT)

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderAppointmentsView(APIView):
    def get(self, request, provider_id):
        provider = get_object_or_404(Provider, id=provider_id)
        appointments = Appointment.objects.filter(provider=provider)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
