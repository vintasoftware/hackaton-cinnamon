# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 23:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('filename', models.CharField(max_length=4096)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('repo_owner', models.CharField(max_length=255)),
                ('repo', models.CharField(max_length=255)),
                ('raw', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('repo_owner', models.CharField(max_length=255)),
                ('repo', models.CharField(max_length=255)),
                ('raw', models.TextField()),
                ('files', models.ManyToManyField(related_name='prs', to='issues.File')),
                ('issues', models.ManyToManyField(related_name='prs', to='issues.Issue')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('relevance', models.FloatField()),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='issues.Issue')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]