# Generated by Django 5.0.6 on 2024-06-16 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, default='../static/images/default_avatar.webp', null=True, upload_to='../media/user_avatars/'),
        ),
    ]
