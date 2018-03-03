from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'job', views.JobViewSet)
router.register(r'perfil', views.PerfilViewSet)
router.register(r'users', views.UserViewSet)
urlpatterns =[
    url(r'^token/', obtain_auth_token, name='api-token'),
    url(r'^', include(router.urls)),
    url(r'^job/(?P<job_pk>\d+)/like/$', views.PerfilViewSet.curtir, name='curtir'),
    url(r'^job/(?P<job_pk>\d+)/deslike/$', views.PerfilViewSet.descurtir, name='descurtir'),
    url(r'^job/(?P<job_pk>\d+)/perfil/(?P<perfil_pk>\d+)/$', views.JobViewSet.escolhido, name='escolher_perfil'),
    url(r'^job/(?P<job_pk>\d+)/reabrir/$', views.JobViewSet.reabrir_job, name= 'reabrir_job'),

    url(r'^perfil/logado', views.PerfilLogado.as_view({'get': 'list'}), name= 'perfil_logado'),
    url(r'^users/logado', views.UsruarioLogado.as_view({'get': 'list'}), name= 'usuario_logado'),

    url(r'^job/(?P<pk>\d+)/comentarios/$',
            views.ComentarioViewSet.as_view({'post': 'create', 'get': 'list'}),
            name='comentarios'),
    url (r'job/(?P<job_pk>\d+)/chat/$',
         views.ChatViewSet.as_view({'post': 'create', 'get': 'list'}),
         name='chat'),
    url(r'^chat/(?P<chat_pk>\d+)/mensagens/$',
        views.MensagemViewSet.as_view({'post': 'create', 'get': 'list'}),
        name='mensagens'),


]

