# Generated by Django 2.0.1 on 2018-01-16 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20180116_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='uploaded_at',
            new_name='updated_at',
        ),
    ]
