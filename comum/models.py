from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Base(models.Model):
    criado_em = models.DateTimeField('Criado em', auto_now_add=True, blank=False, null=False)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

class Job(Base):

    STATUS_JOB =(
        ('aberto', 'Aberto'),
        ('producao', 'Producão'),
        ('finalizado', 'Finalizado'),
        ('reaberto', 'Reaberto'),
        ('em_analise', 'Em ana  lise'),
    )

    status = models.CharField('Status', max_length=64, choices= STATUS_JOB, default='aberto', blank=False, null=False)
    titulo = models.CharField('Titulo', max_length=256, blank=True, null=True)
    descricao = models.TextField('Descrição',  blank=False, null=False, help_text= 'Fale detalhes do serviço pretendido.')
    publico = models.BooleanField('Publico', default=True, blank=False, null=False)
    criador = models.ForeignKey('Perfil', on_delete=models.CASCADE, related_name= 'Jobs', blank=False, null=False)
    escolhido = models.ForeignKey('Perfil', related_name= 'matches', blank=True, null=True)

    class Meta:

        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ('criado_em', )

    def __str__(self):
        return '%s - %s' % (self.descricao, self.criador.usuario.first_name)

    def quant_curtidas(self):
         return len(self.curtidas.all())

    def get_comentarios(self):
        return self.comentarios.all()

    def nome_criador(self):
        return self.criador.nome()

    def cidade(self):
        return self.criador.endereco.cidade

    def definir_escolhido(self, perfil):
        self.escolhido = perfil
        self.status = 'producao'
        self.save()
        return True


    def reabrir_job(self):
        self.escolhido = None
        self.status = 'reaberto'
        self.save()
        return True


    def job_em_analise(self):
        self.status = 'em_analise'
        self.save()
        return True

class Comentario(Base):

    descricao = models.CharField('Descricao', max_length=512, blank=False, null=False, )
    job = models.ForeignKey('Job',on_delete=models.CASCADE, related_name= 'comentarios' , blank=False, null=False, )

    class Meta:

        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ('criado_em', )

    def __str__(self):
        return self.descricao

class Endereco(Base):

    logradouro = models.CharField('Logradouro', max_length=255, blank=False, null=False)
    cidade = models.CharField('Cidade', max_length=64, blank=False, null=False)
    estado = models.CharField('Estado', max_length=64, blank=False, null=False)
    cep = models.FloatField('cep', blank=True, null=True )
    #perfil = models.OneToOneField('Perfil', on_delete=models.CASCADE, related_name='endereco', blank=False, null=False,)

    class Meta:
        verbose_name = 'Endereco'
        verbose_name_plural = "Enderecos"
        ordering = ('criado_em', )

    def __str__(self):
        return '%s - %s - %s' %(self.logradouro, self.cidade, self.estado)

class Perfil(Base):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    sexo = models.CharField('Sexo', max_length=16, choices=SEXO_CHOICES, blank=False, null=False)
    telefone = models.CharField('Telefone', max_length=16, blank=False, null=False)
    data_nascimento = models.CharField('Data de nascimento',max_length=20, blank=False, null=False)
    perfil_profissional = models.TextField('Perfil profissional', blank=False, null=False, help_text='Formação, Cursos extras')
    experiencia = models.TextField('Experiencia', blank=True, null=True, help_text= 'Projetos feitos')
    gitHub = models.CharField('GitHub', max_length=56, null=True, blank=True)
    usuario = models.OneToOneField(User, related_name='perfil')
    endereco = models.OneToOneField('Endereco', on_delete=models.CASCADE, related_name='perfis' ,blank=False, null=False)
    curtida = models.ManyToManyField(Job, related_name='curtidas',  blank=True)


    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return self.nome()

    def nome(self):
        return '%s %s' % (self.usuario.first_name, self.usuario.last_name)

    def curtidas(self):
        return self.curtida.all()

    def curtir(self, job):
        self.curtida.add(job)
        self.save()
        return True

    def descurtir(self, job):
        self.curtida.remove(job)
        self.save()
        return True






