# Generated by Django 4.2.3 on 2023-07-13 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScienceSubjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='موضوع علمی')),
                ('url_title', models.CharField(max_length=500, null=True, unique=True, verbose_name=' موضوع علمی در url')),
                ('text1', models.TextField(verbose_name='متن')),
                ('text2', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('text3', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('text4', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('text5', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('text6', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('text7', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('text8', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('image_on_science_list_page', models.ImageField(upload_to='science', verbose_name='تصویر در لیست موضوعات علمی')),
                ('image_on_science_detail_page', models.ImageField(upload_to='science', verbose_name='تصویر در جزییات موضوع علمی')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال / غیر فعال')),
            ],
            options={
                'verbose_name': 'موضوع علمی',
                'verbose_name_plural': 'موضوعات علمی',
            },
        ),
    ]
