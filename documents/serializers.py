from rest_framework import serializers
from documents.models import *
from users.serializers import CustomUserSerializer, RoleSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'amount', 'units', 'price', 'nds')


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('id', 'name', 'inn', 'kpp', 'ogrn', 'okpo', 'address', 'supervisor', 'regestration_date')


class DocumentStatusSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, required=False)

    class Meta:
        model = DocumentStatus
        fields = ('id', 'name', 'roles', 'status_id')


class DocumentHistorySerializer(serializers.ModelSerializer):
    status = DocumentStatusSerializer(required=False)
    reciever = CustomUserSerializer(required=False)

    class Meta:
        model = DocumentHistory
        fields = ('id', 'status', 'reciever', 'comment', 'date', 'time', 'approved')


class DocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = ('id', 'name', 'document_type')


class DocumentReadDetailSerializer(serializers.ModelSerializer):
    category = DocumentCategorySerializer(required=False)
    status = DocumentStatusSerializer(required=False)
    main_contractor = ContractorSerializer(required=False)
    contractors = ContractorSerializer(many=True, required=False)
    products = ProductSerializer(many=True, required=False)
    creator = CustomUserSerializer(required=False)
    history = DocumentHistorySerializer(many=True, required=False)

    class Meta:
        model = Document
        fields = ('id', 'number', 'date', 'category', 'main_contractor', 'contractors', 'contractors_categories', 'products', 'total_price', 'total_nds', 'creator', 'recievers', 'comment', 'status', 'history', 'signed', 'annuled')


class DocumentReadListSerializer(serializers.ModelSerializer):
    main_contractor = ContractorSerializer(required=False)
    contractors = ContractorSerializer(many=True, required=False)
    category = DocumentCategorySerializer(required=False)
    status = DocumentStatusSerializer(required=False)
    history = DocumentHistorySerializer(many=True, required=False)

    class Meta:
        model = Document
        fields = ('id', 'number', 'date', 'category', 'main_contractor', 'contractors', 'contractors_categories', 'products', 'total_price', 'total_nds', 'creator', 'recievers', 'comment', 'status', 'history', 'signed', 'annuled')


class DocumentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'number', 'date', 'category', 'main_contractor', 'contractors', 'contractors_categories', 'products', 'total_price', 'total_nds', 'creator', 'recievers', 'comment', 'status', 'history', 'signed', 'annuled')