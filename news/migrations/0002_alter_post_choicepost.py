# Generated by Django 4.2.11 on 2024-04-05 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='choicePost',
            field=models.CharField(choices=[('NW', 'Новость'), ('AR', 'Статья')], max_length=2),
        ),
    ]
