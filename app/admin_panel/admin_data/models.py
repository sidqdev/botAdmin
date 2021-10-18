from django.db import models


class WebUsers(models.Model):
    user_id = models.BigIntegerField(verbose_name="Айди юзера", primary_key=True)
    user_name = models.CharField(verbose_name='Юзернейм', max_length=256)
    name = models.CharField(verbose_name='Имя', max_length=256)
    photo = models.ImageField(verbose_name='Аватарка')
    comment = models.TextField(verbose_name='Коментарий', default='')


class Chats(models.Model):
    chat_id = models.BigIntegerField(verbose_name="Айди юзера", primary_key=True)
    create_date = models.DateTimeField(verbose_name='Время создания')
    status = models.CharField(verbose_name='Статус чата', max_length=255)


class MessageTypes(models.Model):
    id = models.CharField(verbose_name='Айди типа', primary_key=True, max_length=256)
    name = models.CharField(verbose_name='Название типа', max_length=256)


class WebMessages(models.Model):
    insert_date = models.DateTimeField(verbose_name='Время отправки')

    chat = models.ForeignKey(verbose_name='Чат', to=Chats,
                                on_delete=models.SET_NULL, null=True)

    from_user = models.ForeignKey(verbose_name='Юзер', to=WebUsers,
                                     on_delete=models.SET_NULL, null=True)

    message_type = models.ForeignKey(verbose_name='Тип сообщения', to=MessageTypes,
                                     on_delete=models.SET_NULL, null=True)

    content = models.TextField(verbose_name='контент')


class MessageUpdates(models.Model):
    message = models.ForeignKey(verbose_name='Сообщение', to=WebMessages,
                                     on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(verbose_name='Статус отправки', default=False)
