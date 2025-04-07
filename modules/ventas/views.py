from django.shortcuts import render
from rest_framework import generics
from .models import Ticket
from .serializers.ticketFacturasSerializer import TicketCreateSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class CrearTicketView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]