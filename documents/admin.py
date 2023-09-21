from django.contrib import admin
from documents.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'units', 'price', 'nds')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class ContractorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'inn', 'kpp', 'ogrn', 'okpo', 'address', 'supervisor', 'regestration_date')
    search_fields = ('id', 'name', 'inn', 'kpp', 'ogrn', 'okpo')
    list_filter = ('id', 'name', 'inn', 'kpp', 'ogrn', 'okpo')


class DocumentHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'reciever', 'date', 'time', 'comment')
    search_fields = ('id', 'status', 'reciever')
    list_filter = ('id', 'status', 'reciever')


class DocumentStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status_id')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'document_type')
    search_fields = ('id', 'name', 'document_type')
    list_filter = ('id', 'name')


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'date', 'category', 'main_contractor', 'total_price', 'total_nds', 'creator', 'status', 'comment', 'signed', 'annuled') 
    search_fields = ('id', 'number', 'date', 'total_price', 'total_nds')
    list_filter = ('id', 'number', 'date', 'total_price', 'total_nds', 'signed', 'annuled')


admin.site.register(Contractor, ContractorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(DocumentHistory, DocumentHistoryAdmin)
admin.site.register(DocumentStatus, DocumentStatusAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(Document, DocumentAdmin)