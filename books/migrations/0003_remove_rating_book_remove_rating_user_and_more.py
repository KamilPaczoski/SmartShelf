# Generated by Django 5.0.6 on 2024-06-17 10:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_rating_alter_book_totalratings'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='book',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='totalratings',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='shelf_type',
            field=models.CharField(choices=[('read_later', 'Read Later'), ('favourite', 'Favourite'), ('rated', 'Rated')], max_length=50),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('rating', models.IntegerField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
