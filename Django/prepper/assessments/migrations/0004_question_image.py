# Generated by Django 5.1.2 on 2024-12-01 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0003_question_qnum'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='question_images/'),
        ),
    ]
