import datetime
from django.db import models
from django_currentuser.db.models import CurrentUserField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from users.models import CustomUser, Role


class DocumentStatus(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    roles = models.ManyToManyField(Role, related_name='statuses_role', verbose_name='Доступ')
    status_id = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)], verbose_name='ID статуса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус документа'
        verbose_name_plural = 'Статусы документов'


class DocumentHistory(models.Model):
    status = models.ForeignKey('DocumentStatus', on_delete=models.CASCADE, related_name='histories_status', verbose_name='Статус')
    reciever = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE, related_name='histories_user', verbose_name='Получатель')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    date = models.DateField(default=datetime.date.today(), verbose_name='Дата')
    time = models.TimeField(default=datetime.datetime.now().time(), verbose_name='Время')
    approved = models.BooleanField(default=False, verbose_name='Документ согласован')

    class Meta:
        verbose_name = 'История документа'
        verbose_name_plural = 'Истории документов'


class Contractor(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    inn = models.CharField(max_length=256, unique=True, verbose_name='ИНН')
    kpp = models.CharField(max_length=256, unique=True, verbose_name='КПП')
    ogrn = models.CharField(max_length=256, unique=True, verbose_name='ОГРН')
    okpo = models.CharField(default='11111', max_length=256, verbose_name='ОКПО')
    address = models.TextField(verbose_name='Адрес')
    supervisor = models.CharField(default='None', max_length=256, verbose_name='Руководитель')
    regestration_date = models.DateField(default=datetime.date.today(), verbose_name='Дата регистрации')    

    def __str__(self):
        return self.inn

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    amount = models.IntegerField(verbose_name='Количество')
    units = models.CharField(max_length=256, verbose_name='Единицы измерения')
    price = models.IntegerField(verbose_name='Цена')
    nds = models.FloatField(verbose_name='НДС')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class DocumentCategory(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    document_type = models.CharField(max_length=256, verbose_name='Тип категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория документа'
        verbose_name_plural = 'Категории документов'


class Document(models.Model):
    number = models.CharField(max_length=256, verbose_name='Номер')
    date = models.DateField(default=datetime.date.today(), verbose_name='Дата оформления')
    category = models.ForeignKey('DocumentCategory', on_delete=models.CASCADE, related_name='documents_category', verbose_name='Категория')
    main_contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE, related_name='documents_main_contractor', verbose_name='Главный контрагент') 
    contractors = models.ManyToManyField('Contractor', related_name='documents_contractor', verbose_name='Контрагенты')
    contractors_categories = models.JSONField(verbose_name='Категории контрагентов')
    products = models.ManyToManyField('Product', related_name='documents_product', verbose_name='Товары')
    total_price = models.IntegerField(default=0, verbose_name='Полная стоимость с учётом НДС')
    total_nds = models.IntegerField(default=0, verbose_name='НДС в рублях')
    creator = CurrentUserField(verbose_name='Создатель документа')
    recievers = models.ManyToManyField(CustomUser, related_name='documents_reciever', verbose_name='Получатели')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    status = models.ForeignKey('DocumentStatus', blank=True, null=True, on_delete=models.DO_NOTHING, related_name='documents_status', verbose_name='Статус')
    history = models.ManyToManyField('DocumentHistory', blank=True, null=True, related_name='documents_history', verbose_name='История')
    signed = models.BooleanField(default=False, verbose_name='Документ подписан')
    annuled = models.BooleanField(default=False, verbose_name='Документ аннулирован')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'