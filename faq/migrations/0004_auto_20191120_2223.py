# Generated by Django 2.2.7 on 2019-11-20 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_auto_20191118_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='answers', to='faq.Tag', verbose_name='mots-clé'),
        ),
    ]
