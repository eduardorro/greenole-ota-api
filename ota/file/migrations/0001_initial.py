# Generated by Django 5.1.3 on 2024-12-03 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_script', models.FilePathField()),
                ('target_update', models.FilePathField()),
            ],
        ),
    ]