# Generated by Django 4.2.3 on 2023-08-13 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='postcontentaudio',
            unique_together={('post_content', 'audio_url')},
        ),
        migrations.AlterUniqueTogether(
            name='postcontent',
            unique_together={('post', 'level')},
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('title', 'user')},
        ),
    ]
