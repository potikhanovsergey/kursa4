# Generated by Django 3.1.5 on 2021-05-30 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='update_date',
            field=models.DateTimeField(null=True),
        ),
    ]
