# Generated by Django 4.1.3 on 2023-04-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_productimage_image_alter_productimage_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to='static\\images'),
        ),
    ]