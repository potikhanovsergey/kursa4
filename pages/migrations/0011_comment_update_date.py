# Generated by Django 3.1.5 on 2021-05-30 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_remove_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='update_date',
            field=models.DateField(null=True),
        ),
    ]
