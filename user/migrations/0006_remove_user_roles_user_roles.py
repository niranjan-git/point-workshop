# Generated by Django 4.0.4 on 2022-04-25 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_role_role_short_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.role'),
            preserve_default=False,
        ),
    ]
