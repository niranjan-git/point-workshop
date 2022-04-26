# Generated by Django 4.0.4 on 2022-04-26 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_workshop', '0004_alter_branch_created_alter_city_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pincode',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='state',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userassignedrole',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='zone',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
