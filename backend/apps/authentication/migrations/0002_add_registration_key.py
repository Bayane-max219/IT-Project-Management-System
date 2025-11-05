# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('developer', 'Développeur'), ('client', 'Client')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('is_used', models.BooleanField(default=False)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_keys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "Clé d'inscription",
                'verbose_name_plural': "Clés d'inscription",
                'db_table': 'registration_keys',
            },
        ),
    ]
