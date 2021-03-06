# Generated by Django 3.1.7 on 2021-05-02 14:22

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
            name='BasicInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_valid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('basicinformation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='frama.basicinformation')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('parent_directory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frama.directory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'user')},
            },
            bases=('frama.basicinformation',),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('basicinformation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='frama.basicinformation')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('file_field', models.FileField(upload_to='uploads/')),
                ('parent_directory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frama.directory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'user')},
            },
            bases=('frama.basicinformation',),
        ),
        migrations.CreateModel(
            name='FileSection',
            fields=[
                ('basicinformation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='frama.basicinformation')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(choices=[('Procedure', 'Procedure'), ('Property', 'Property'), ('Lemma', 'Lemma'), ('Assertion', 'Assertion'), ('Invariant', 'Invariant'), ('Precondition', 'Precondition'), ('Postcondition', 'Postcondition')], max_length=13)),
                ('status', models.CharField(choices=[('Proved', 'Proved'), ('Invalid', 'Invalid'), ('Counterexample', 'Counterexample'), ('Unchecked', 'Unchecked')], max_length=14)),
                ('status_data', models.CharField(blank=True, max_length=100, null=True)),
                ('file_referred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frama.file')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('frama.basicinformation',),
        ),
    ]
