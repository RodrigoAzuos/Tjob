from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, authentication, permissions, filters, status, exceptions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from comum.models import Job, Perfil, Comentario, Endereco
from django.contrib.auth import get_user_model
from .serializers import JobSerializer, PerfilSerializer, UserSerializer, \
    EnderecoSerializer, ComentarioSerializer, JobSimplesSerializer, ChatSerializer, MensagemSerializer

from chat.models import Chat, Mensagem

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from api.forms import JobFilter, PerfilFilter

User = get_user_model()


# Create your views here.
class DefaultsMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class JobViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Job.objects.order_by('criado_em')
    serializer_class = JobSerializer
    filter_class = JobFilter
    search_fields = ('status',)
    ordering_fields = ('criado_em',)

    def get_queryset(self):

        qs = Job.objects.order_by('-criado_em')
        if not self.request.user.is_superuser:
            qs = Job.objects.filter(publico=True).order_by('-criado_em')
            qs2 = Job.objects.filter(criador__endereco__cidade=self.request.user.perfil.endereco.cidade).order_by('-criado_em')

            qs = qs | qs2

        return qs

    def list(self, request):
        qs = self.get_queryset()
        criador = self.request.query_params.get('criador', None)
        escolhido = self.request.query_params.get('escolhido', None)
        curtidas = self.request.query_params.get('curtidas', None)

        if criador is not None:
            qs = qs.filter(criador=criador)

        elif escolhido is not None:
            qs = qs.filter(escolhido=escolhido)

        elif curtidas is not None:
            qs = qs.filter(curtidas=curtidas)

        serializer = JobSimplesSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        job = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    @api_view()
    @authentication_classes(authentication_classes=DefaultsMixin.authentication_classes)
    @permission_classes(permission_classes=DefaultsMixin.permission_classes)
    def escolhido(request, job_pk, perfil_pk):

        try:
            job = Job.objects.get(pk=job_pk)
            perfil = Perfil.objects.get(pk=perfil_pk)

            if job.definir_escolhido(perfil):
                return Response({"mensagem": "Perfil escolhido com sucesso!"}, status=status.HTTP_200_OK)
        except:
            return Response({"mensagem": "Perfil ou Job não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"mensagem": "Não realizado"}, status=status.HTTP_400_BAD_REQUEST)

    @api_view()
    @authentication_classes(authentication_classes=DefaultsMixin.authentication_classes)
    @permission_classes(permission_classes=DefaultsMixin.permission_classes)
    def reabrir_job(request, job_pk):
        print(job_pk)
        try:
            job = Job.objects.get(pk=job_pk)
            if job.reabrir_job():
                return Response({"mensage": "Job reaberto!"}, status=status.HTTP_200_OK)
        except:
            return Response({"mensagem": "Job não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"mensagem": "Não realizado"},status=status.HTTP_400_BAD_REQUEST)


class PerfilViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    filter_class = PerfilFilter
    search_fields = ('sexo',)
    ordering_fields = ('criado_em',)

    @api_view()
    @authentication_classes(authentication_classes=DefaultsMixin.authentication_classes)
    @permission_classes(permission_classes=DefaultsMixin.permission_classes)
    def curtir(request, job_pk):
        if job_pk != None:
            job = Job.objects.get(pk=job_pk)
            user = request.user

            if user.perfil.curtir(job):
                return Response({"mensagem": "Job curtido!"}, status=status.HTTP_200_OK)

        return Response({"mensagem": "falha."}, status=status.HTTP_400_BAD_REQUEST)

    @api_view()
    @authentication_classes(authentication_classes=DefaultsMixin.authentication_classes)
    @permission_classes(permission_classes=DefaultsMixin.permission_classes)
    def descurtir(request, job_pk):
        if job_pk != None:
            job = Job.objects.get(pk=job_pk)
            user = request.user

            if user.perfil.descurtir(job):
                return Response({"mensagem": "Job retirado da lista de curtidas!"}, status=status.HTTP_200_OK)

        return Response({"mensagem": "falha!"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer


class EnderecoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Endereco.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = Endereco.objects.all()

        return queryset

    serializer_class = EnderecoSerializer


class ComentarioViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

    def create(self, request, pk, *args, **kwargs):
        serializer = ComentarioSerializer(data=request.data,
                                          context={'job_pk': pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, pk, *args, **kwargs):
        queryset = self.filter_queryset(Comentario.objects.filter(job__pk=pk))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChatViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def get_queryset(self):
        qs = Chat.objects.all()
        if self.request.user.is_superuser:
            qs = Chat.objects.filter(participantes__pk=self.request.user.perfil.pk)
        return qs

    def create(self, request, job_pk, *args, **kwargs):
        try:
            job = Job.objects.get(pk=job_pk)
        except Job.DoesNotExist:
            raise exceptions.NotFound(detail='Job não localizado.')
        except:
            raise exceptions.NotAcceptable(detail='Não foi possível criar o chat.')

        print(job.escolhido)
        if job.escolhido != None:
            chat = Chat.objects.create()
            chat.participantes.add(job.criador)
            chat.participantes.add(job.escolhido)
            chat.save()

            serializer = ChatSerializer(chat)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'detail': 'Este Job não tem um perfil escolhido'}, status=status.HTTP_400_BAD_REQUEST)


class MensagemViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = MensagemSerializer
    queryset = Mensagem.objects.all()

    def create(self, request, chat_pk, *args, **kwargs):
        print(chat_pk)
        perfil_pk = request.user.perfil.pk
        serializer = MensagemSerializer(data=request.data, context={'chat_pk': chat_pk, 'perfil_pk': perfil_pk})

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, chat_pk, *args, **kwargs):
        queryset = self.filter_queryset(Mensagem.objects.filter(chat__pk=chat_pk))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UsruarioLogado(DefaultsMixin, viewsets.ModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = User.objects.all()
        user_pk = self.request.user.pk
        qs = qs.filter(pk=user_pk)

        return qs


class PerfilLogado(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()


    def get_queryset(self):
        qs = None
        try:
            perfil_pk = self.request.user.perfil.pk
        except:
            return qs
        qs = Perfil.objects.all()
        qs = qs.filter(pk=perfil_pk)

        return qs
