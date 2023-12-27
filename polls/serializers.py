from django.db import models
from django.db.models import fields

from .models import Reviews
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer 
class ReveiwSerializers(ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'
