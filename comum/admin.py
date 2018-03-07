from django.contrib import admin
from .models import *

# Register your models here.


class ComentarioInline(admin.TabularInline):
    model = Comentario
    fields = ('descricao', )
    extra = 1

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display =  ('status', 'descricao', 'criador', 'quant_curtidas','get_comentarios')

    inlines = (ComentarioInline, )

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sexo', 'telefone', 'data_nascimento', 'usuario', 'curtidas',  )

    fieldsets = (
        (None, {
            'fields': ('usuario', ('sexo', 'data_nascimento',), ('endereco', 'telefone'),  'perfil_profissional', 'gitHub', 'experiencia',     )
        }),
    )

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('logradouro', 'cidade', 'estado', )

