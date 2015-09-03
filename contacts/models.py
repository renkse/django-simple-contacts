# coding=utf-8
__author__ = 'renkse'

from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
import datetime

SERVAK = settings.SERVAK
REG_PHONE = r'^[0-9+() -]{5,20}$'


class Contact(models.Model):
    title = models.CharField(max_length=100, verbose_name='название филиала', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес')
    fax = models.CharField(max_length=100, verbose_name='Факс', blank=True, null=True,
                           validators=[RegexValidator(
                               regex=REG_PHONE,
                               message='В факсе допустимы только цифры, пробелы и символы: "+", "-", "(", ")".'
                                       ' Введите не менее 5 и не более 20 символов.'
                           )])
    email = models.EmailField(max_length=200, verbose_name='E-mail', blank=True, null=True)

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.address

    def get_phones(self):
        phones = []
        for phone in self.contactphone_set.all():
            phones.append(phone.phone)
        return phones

    def get_worktime(self):
        time = []
        for worktime in self.worktime_set.all():
            time.append(worktime.time)
        return time

    class Meta:
        verbose_name = u'контакты'
        verbose_name_plural = u'контактная информация'


class ContactPhone(models.Model):
    phone = models.CharField(max_length=100, verbose_name='Контактный телефон',
                             validators=[RegexValidator(
                                 regex=REG_PHONE,
                                 message='В номере телефона допустимы только цифры, пробелы и символы: "+", "-", "(",'
                                         ' ")". Введите не менее 5 и не более 20 символов.'
                             )])
    contacts = models.ForeignKey(Contact)

    def __unicode__(self):
        return u'телефон'

    class Meta:
        verbose_name_plural = u'телефоны'
        verbose_name = u'контактный телефон'


class WorkTime(models.Model):
    time = models.CharField(max_length=255, verbose_name='время')
    contacts = models.ForeignKey(Contact)

    def __unicode__(self):
        return u'время'

    class Meta:
        verbose_name_plural = u'рабочее время'
        verbose_name = u'рабочее время'


class FeedbackMessage(models.Model):
    fields = ['name', 'phone', 'email', 'message']
    name = models.CharField(max_length=255, verbose_name='ФИО')
    phone = models.CharField(max_length=100, verbose_name='Телефон', blank=True, null=True,
                             validators=[RegexValidator(
                                 regex=r'^[0-9+() -]+$',
                                 message='В номере телефона допустимы только цифры, пробелы и символы: "+", "-", "(", ")".'
                             )])
    email = models.EmailField(max_length=255, verbose_name='e-mail')
    branch = models.ForeignKey(Contact, verbose_name='филиал')
    message = models.TextField(verbose_name='Сообщение')
    received_at = models.DateTimeField(verbose_name='Дата и время получения', editable=False)

    class Meta:
        verbose_name = u'сообщение'
        verbose_name_plural = u'сообщения'

    def save(self, *args, **kwargs):
        if not self.id:
            if SERVAK:
                from django.core.mail import send_mail
                if self.branch and self.branch.email:
                    recipients = ['info@autotcn.ru', self.branch.email]
                else:
                    recipients = ['info@autotcn.ru']

                send_mail(
                    u'Сообщение прислал {0}'.format(self.name),
                    self.message, 'nadyojny@yandex.ru',
                    recipients,
                    # ['solomon_art@mail.ru'],
                    fail_silently=False
                )
        if not self.id:
            self.received_at = datetime.datetime.now()
        return super(FeedbackMessage, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name