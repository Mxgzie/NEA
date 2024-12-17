# Generated by Django 5.1.2 on 2024-12-01 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('topic', models.CharField(max_length=100)),
                ('exam_board', models.CharField(max_length=7)),
                ('exam_year', models.IntegerField()),
                ('marks', models.IntegerField()),
            ],
        ),
    ]
