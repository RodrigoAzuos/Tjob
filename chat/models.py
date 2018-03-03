from django.db import models
from comum.models import Base, Perfil

# Create your models here.
class Mensagem(Base):

    MENSAGEM_CHOICES = (
        ('enviada', 'Enviada'),
        ('lida', 'Lida'),
    )

    status = models.CharField('Status', max_length=64,choices= MENSAGEM_CHOICES, default= 'enviada', blank=False, null=False)
    texto = models.CharField('Texto', max_length=256,  blank=False, null=False)
    chat = models.ForeignKey('Chat', related_name='mensagens', blank=False, null=False)
    remetente = models.ForeignKey(Perfil, related_name='minhas_mensagens', blank=False, null=False)

class Chat(Base):

    participantes = models.ManyToManyField(Perfil, related_name='chats', blank=False)

