import django_filters

from comum.models import Job, Perfil

class NullFilter(django_filters.BooleanFilter):
    """Filter on a field set as null or not."""
    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.name: value})
        return qs

class JobFilter(django_filters.FilterSet):

    backlog = NullFilter(name='descricao')

    class Meta:
        model = Job
        fields = ('criador', 'escolhido', 'publico', 'curtidas', )

class PerfilFilter(django_filters.FilterSet):

    backlog = NullFilter(name= 'sexo')

    class Meta:
        model = Perfil
        fields = ('endereco', 'usuario',  )