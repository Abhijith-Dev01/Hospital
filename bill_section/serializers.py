from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class PharmacyBillItemSerializer(ModelSerializer):
    pharmacy_item =serializers.PrimaryKeyRelatedField(queryset=Pharmacy.objects.all())
    class Meta:
        model = PharmacyBillItem
        fields = ['pharmacy_item','quantity','cost']
        
        
class PharmacyBillSerializer(ModelSerializer):
    items = PharmacyBillItemSerializer(many=True)
    class Meta:
        model = PharmacyBill
        fields = "__all__"      
    
    def create(self,validated_data):
        items_data = validated_data.pop('items')
        pharmacy_bill = PharmacyBill.objects.create(**validated_data)
        for item in items_data:
            PharmacyBillItem.objects.create(pharmacy_bill=pharmacy_bill,
                        pharmacy_item=item['pharmacy_item'],quantity=item['quantity'],
                        cost=item['cost'])

        return validated_data

class OperationSerializer(ModelSerializer):
    
    class Meta:
        model = OperationCost
        fields = "__all__"
        

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        
class BedRestSerializer(ModelSerializer):
    room= RoomSerializer()
    
    class Meta:
        model = BedRestCost
        fields = "__all__"
    
    def create(self,validated_data):
        room_data = dict(validated_data.pop('room'))
        room = Room.objects.create(**room_data)
        
        validated_data['room'] = room
        BedRestCost.objects.create(**validated_data)
        return validated_data