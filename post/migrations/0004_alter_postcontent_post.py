# Generated by Django 4.2.3 on 2023-08-27 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_post_user_alter_postcontentaudio_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcontent',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='post.post'),
        ),
    ]
