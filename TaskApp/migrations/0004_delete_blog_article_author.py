# Generated by Django 5.0.1 on 2024-01-31 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskApp', '0003_blog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blog',
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
