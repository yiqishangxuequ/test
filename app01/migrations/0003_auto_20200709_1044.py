# Generated by Django 2.2.9 on 2020-07-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_remove_category_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(default=2233, max_length=64, verbose_name='文章分类'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
