# Generated by Django 2.2.7 on 2019-11-28 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20191127_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFHolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(blank=True, upload_to='recipes_pdfs/', verbose_name='Fichier PDF')),
            ],
        ),
    ]
