from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from comum.models import Job, Perfil, Comentario, Endereco
from chat.models import Chat, Mensagem

User = get_user_model()


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:

        model = Comentario
        fields = ('id', 'descricao', 'job')
        read_only_fields = ('id', 'job')

    def create(self, validated_data):

        job_pk = self.context.get('job_pk')
        descricao = validated_data['descricao']

        try:
            job = Job.objects.get(pk=job_pk)
            comentario = Comentario.objects.create(job=job, descricao=descricao)
            return comentario
        except Job.DoesNotExist:
            raise exceptions.NotFound(detail='Job não localizado.')
        except:
            raise exceptions.NotAcceptable(detail='Não foi possível adicionar o comentários.')


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('id', 'logradouro', 'cidade', 'estado', 'cep',)


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'first_name', 'last_name', 'is_active', 'email', 'password',)
        read_only_fields = ('id', 'is_active',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password_data = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password_data)
        user.save()

        return user


class PerfilSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer(many=False)

    class Meta:
        model = Perfil
        fields = ('id', 'nome', 'telefone', 'data_nascimento', 'sexo',
                  'perfil_profissional', 'gitHub', 'experiencia', 'usuario', 'endereco',)

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        cidade = endereco_data.pop('cidade')
        endereco = Endereco.objects.create(cidade=cidade.upper(), **endereco_data)
        perfil = Perfil.objects.create(endereco=endereco, **validated_data)

        return perfil


class JobSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)
    curtidas = PerfilSerializer(many=True, read_only=True)
    escolhido = PerfilSerializer(many=False, read_only=True)

    class Meta:
        model = Job
        fields = (
        'id', 'status','titulo', 'descricao', 'criador', 'nome_criador', 'publico', 'escolhido', 'comentarios', 'curtidas',
        'cidade',)
        read_only_fields = ('id','nome_criador','comentarios', 'curtidas')


class JobSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'status', 'titulo', 'descricao', 'criador', 'nome_criador', 'publico', 'curtidas',)
        read_only_fields = ('id',)


class ChatSerializer(serializers.ModelSerializer):
    participantes = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ('id', 'participantes')
        read_only_fields = ('id', 'participantes')


class MensagemSerializer(serializers.ModelSerializer):
    class Meta:

        model = Mensagem
        fields = ('id', 'texto', 'chat', 'remetente',)
        read_only_fields = ('id','remetente','chat',)

    def create(self, validated_data):
        chat_pk = self.context.get('chat_pk')
        perfil_pk = self.context.get('perfil_pk')
        texto = validated_data['texto']
        print(chat_pk, perfil_pk)

        try:
            chat = Chat.objects.get(pk=chat_pk)
            perfil = Perfil.objects.get(pk=perfil_pk)
            mensagem = Mensagem.objects.create(chat=chat, texto=texto, remetente=perfil)

            return mensagem
        except  Chat.DoesNotExist:
            raise exceptions.NotFound(detail='Chat não localizado.')
        except:
            raise exceptions.NotAcceptable(detail='Não foi possível enviar a mensagem.')
