# Generated by Django 4.2.3 on 2023-08-08 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_postcontent_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='postcontent',
            table='posts_post_content',
        ),
    ]