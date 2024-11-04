# Generated by Django 5.0.3 on 2024-11-04 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_alter_complaint_body_alter_complaint_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='body',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='image_link',
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='img',
            field=models.ImageField(max_length=5000, null=True, upload_to=''),
        ),
    ]