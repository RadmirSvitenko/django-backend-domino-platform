# Generated by Django 5.1.4 on 2024-12-29 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0001_initial'),
        ('category', '0003_remove_category_subcategory_category_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='subcategory',
            field=models.ManyToManyField(related_name='ads', to='category.subcategory'),
        ),
    ]