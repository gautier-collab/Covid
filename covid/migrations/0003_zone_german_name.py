# Generated by Django 3.2 on 2021-05-01 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0002_metric_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='german_name',
            field=models.CharField(max_length=32, null=True),
        ),
    ]