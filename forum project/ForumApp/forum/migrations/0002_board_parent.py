# Generated by Django 3.2.9 on 2021-12-07 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='parent',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
