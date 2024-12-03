# Generated by Django 5.1.3 on 2024-11-15 08:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=250)),
                ('cover_img', models.FileField(upload_to='media/%y/%m/%d')),
                ('description', models.TextField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('contact_number', models.IntegerField(blank=True, unique=True)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Contact Us',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(blank=True, max_length=100)),
                ('estimated_delivery_time', models.DateTimeField(blank=True, null=True)),
                ('delivery_status', models.CharField(default='Pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(max_length=250, unique=True)),
                ('image', models.ImageField(upload_to='dishes/%y/%m/%d')),
                ('ingredients', models.TextField()),
                ('price', models.FloatField()),
                ('discounted_price', models.FloatField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuickBite.category')),
            ],
            options={
                'verbose_name_plural': 'Dish Table',
            },
        ),
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.IntegerField()),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile/%y/%m/%d')),
                ('address', models.TextField(blank=True, max_length=250, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='QuickBite.order')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuickBite.signup')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuickBite.signup'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('dish', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuickBite.dish')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='QuickBite.order')),
            ],
            options={
                'unique_together': {('dish', 'order')},
            },
        ),
    ]
