# Generated by Django 5.1.2 on 2024-12-01 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='exam_paper',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
