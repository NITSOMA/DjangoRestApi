# Generated by Django 4.2.7 on 2023-12-01 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_api', '0002_delete_new'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appraisalrequest',
            old_name='more_info',
            new_name='requested_info',
        ),
    ]
