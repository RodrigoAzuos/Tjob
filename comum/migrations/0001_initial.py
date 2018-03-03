# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-29 02:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualizado em')),
                ('descricao', models.CharField(max_length=256, verbose_name='Descricao')),
            ],
            options={
                'ordering': ('criado_em',),
                'verbose_name_plural': 'Comentários',
                'verbose_name': 'Comentário',
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualizado em')),
                ('logradouro', models.CharField(max_length=255, verbose_name='Logradouro')),
                ('cidade', models.CharField(max_length=64, verbose_name='Cidade')),
                ('estado', models.CharField(max_length=64, verbose_name='Estado')),
                ('cep', models.FloatField(blank=True, null=True, verbose_name='cep')),
            ],
            options={
                'verbose_name': 'Endereco',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualizado em')),
                ('status', models.CharField(choices=[('aberto', 'Aberto'), ('producao', 'Producão'), ('finalizado', 'Finalizado'), ('reaberto', 'Reaberto'), ('em_analise', 'Em analise')], default='aberto', max_length=64, verbose_name='Status')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição')),
                ('publico', models.BooleanField(default=True, verbose_name='Publico')),
            ],
            options={
                'ordering': ('criado_em',),
                'verbose_name_plural': 'Jobs',
                'verbose_name': 'Job',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualizado em')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=16, verbose_name='Sexo')),
                ('telefone', models.CharField(max_length=16, verbose_name='Telefone')),
                ('data_nascimento', models.DateField(verbose_name='Data de nascimento')),
                ('perfil_profissional', models.TextField(help_text='Formação, Cursos extras', verbose_name='Perfil proficional')),
                ('experiencia', models.CharField(max_length=512, verbose_name='Experiencia')),
                ('curtida', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curtidas', to='comum.Job')),
                ('endereco', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comum.Endereco')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Perfis',
                'verbose_name': 'Perfil',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='criador',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Jobs', to='comum.Perfil'),
        ),
        migrations.AddField(
            model_name='job',
            name='escolhido',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='comum.Perfil'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='comum.Job'),
        ),
    ]