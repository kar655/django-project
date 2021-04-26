# Generated by Django 3.1.7 on 2021-04-26 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frama', '0001_initial'),
    ]

    operations = [
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frama.user')),
            ],
            bases=('frama.basicinformation',),
        ),
    ]
