# Generated by Django 5.1.2 on 2024-12-01 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0002_question_exam_paper'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='Qnum',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]
