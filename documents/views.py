from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from documents.models import *
from documents.permissions import IsEmployeeOrReadOnly, IsRecieverAndRole, IsCreatorOrReciever
from documents.serializers import *


class DocumentAPIListView(generics.ListAPIView):
    serializer_class = DocumentReadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(Q(creator=self.request.user.id) | Q(recievers__in=[self.request.user.id]))
    

class DocumentAPIFilterListView(generics.ListAPIView):
    serializer_class = DocumentReadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        documents = Document.objects
        contractor_approve = self.request.GET.get('contractor_approve', None)
        contractor_annule = self.request.GET.get('contractor_annule', None)
        documents_status = self.request.GET.get('tag', None)

        if contractor_approve:
            documents.filter(main_contractor=int(contractor_approve), status__status_id__gte=0)

        elif contractor_annule:
            documents.filter(main_contractor=int(contractor_annule), status__status_id=0)

        elif documents_status:
            documents.filter(status__status_id=int(documents_status))

        return documents
    

class DocumentAPIContractorApproveListView(generics.ListAPIView):
    serializer_class = DocumentReadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(main_contractor=int(self.kwargs['pk']), status__status_id__gte=0)
    

class DocumentAPIContractorAnnuleListView(generics.ListAPIView):
    serializer_class = DocumentReadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(main_contractor=int(self.kwargs['pk']), status__status_id=0)
    

class DocumentAPIStatusListView(generics.ListAPIView):
    serializer_class = DocumentReadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(status__status_id=int(self.kwargs['pk']))
    

class DocumentAPICreateView(generics.CreateAPIView):
    serializer_class = DocumentWriteSerializer
    permission_classes = [IsEmployeeOrReadOnly]

    def post(self, request):
        serializer = DocumentWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            instance = Document.objects.get(pk=serializer.data['id'])

            instance.status = DocumentStatus.objects.filter(status_id=1)[0]

            if instance.products.all():
                price = 0
                nds = 0

                for product in instance.products.all():
                    price_all = product.amount * product.price
                    price += price_all + price_all * product.nds
                    nds += price_all * product.nds

                instance.total_price = price 
                instance.total_nds = nds

            if instance.recievers.all():
                doc_history = DocumentHistory.objects.create(status=instance.status, reciever=instance.recievers.all()[0], comment=instance.comment)
                doc_history.save()

                instance.history.set([DocumentHistory.objects.get(pk=doc_history.pk)])

            instance.save()

            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


class DocumentAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentWriteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk']:
            document = Document.objects.get(pk=self.kwargs['pk'])
            serializer = DocumentReadDetailSerializer(document)
                
            return Response(serializer.data)
    
        return Response([], status=status.HTTP_404_NOT_FOUND)
    

class DocumentAPIApproveView(generics.UpdateAPIView):
    serializer_class = DocumentWriteSerializer
    permission_classes = [IsRecieverAndRole]

    def update(self, request, *args, **kwargs):
        obj = Document.objects.get(pk=self.kwargs['pk'])
        
        if obj.status.status_id < 4 and obj.status.status_id != 0:
            last_doc_history = obj.history.last()
            last_doc_history.approved = True
            last_doc_history.save()

            doc_reciever = int(request.GET.get('reciever', None))
            obj.recievers.add(doc_reciever)

            obj.status = DocumentStatus.objects.get(pk=obj.status.pk+1)
            obj.save()

            if obj.status.status_id == 4:
                new_history = DocumentHistory.objects.create(status=obj.status, approved=True)
                obj.signed = True
                obj.history.add(new_history.pk)

            elif obj.status.status_id < 3:
                new_history = DocumentHistory.objects.create(status=DocumentStatus.objects.filter(pk=obj.status.pk+1)[0], reciever=CustomUser.objects.filter(pk=doc_reciever)[0])
                obj.history.add(new_history.pk)

            obj.save()

        serializer = DocumentReadDetailSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

class DocumentAPIAnnuleView(generics.UpdateAPIView):
    serializer_class = DocumentWriteSerializer
    permission_classes = [IsRecieverAndRole]

    def update(self, request, *args, **kwargs):
        obj = Document.objects.get(pk=self.kwargs['pk'])
        
        if obj.status.status_id == 3:
            obj.status = DocumentStatus.objects.get(status_id=0)
            obj.save()

            new_history = DocumentHistory.objects.create(status=obj.status)
            obj.history.add(new_history.pk)
            obj.annuled = True
            
            obj.save()

        serializer = DocumentReadDetailSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

class DocumentAPIListRecieversView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs['pk'] < 3:
            return CustomUser.objects.filter(role__in=DocumentStatus.objects.get(pk=self.kwargs['pk']+2).roles.all())
        
        return []


class DocumentCategoryAPIListView(generics.ListAPIView):
    queryset = DocumentCategory.objects.all()
    serializer_class = DocumentCategorySerializer
    permission_classes = [IsAuthenticated]


class DocumentStatusAPIListView(generics.ListAPIView):
    queryset = DocumentStatus.objects.all()
    serializer_class = DocumentStatusSerializer
    permission_classes = [IsAuthenticated]


class ContractorAPIListView(generics.ListAPIView):
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        contractors = Document.objects.values_list('main_contractor', flat=True).distinct()
        
        return Contractor.objects.filter(pk__in=contractors)
    

class ContractorAPICreateView(generics.CreateAPIView):
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]


class ContractorAPIRetrieveView(generics.RetrieveAPIView):
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        contractor_inn = self.kwargs['inn']

        if contractor_inn:
            contractor = Contractor.objects.get(inn=contractor_inn)
            serializer = ContractorSerializer(contractor)
            
            return Response(serializer.data) 
        
        return Response([], status=status.HTTP_404_NOT_FOUND)


class ProductAPICreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]





    
