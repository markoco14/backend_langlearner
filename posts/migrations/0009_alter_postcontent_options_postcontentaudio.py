# Generated by Django 4.2.3 on 2023-08-12 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_user_alter_post_title_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcontent',
            options={'verbose_name_plural': 'Post contents'},
        ),
        migrations.CreateModel(
            name='PostContentAudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_url', models.CharField(max_length=255)),
                ('timestamps', models.JSONField()),
                ('post_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audio', to='posts.postcontent')),
            ],
            options={
                'verbose_name_plural': 'Post content audios',
                'db_table': 'posts_post_content_audio',
                'unique_together': {('post_content', 'audio_url')},
            },
        ),
    ]