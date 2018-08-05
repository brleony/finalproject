# Generated by Django 2.0.7 on 2018-08-05 21:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('color', models.CharField(choices=[('blue', 'Blue'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('red', 'Red'), ('orange', 'Orange'), ('yellow', 'Yellow'), ('green', 'Green'), ('teal', 'Teal'), ('cyan', 'Cyan')], default='cyan', max_length=8)),
                ('icon', models.CharField(default='fa-asterisk', max_length=64)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('last_edited', models.DateTimeField(auto_now=True, verbose_name='Last Edited')),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=4)),
                ('unicode_html', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=32, verbose_name='What does it cost?')),
                ('method', models.CharField(choices=[('Debit', 'Debit Card'), ('Credit', 'Credit Card'), ('Cash', 'Cash'), ('Online', 'Online'), ('Paypal', 'PayPal'), ('Mobile', 'Mobile'), ('Transfer', 'Bank Transfer'), ('Cheque', 'Cheque'), ('Other', 'Other')], max_length=8, verbose_name='Payment Method')),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('date_spent', models.DateTimeField(verbose_name='Date Spent')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('last_edited', models.DateTimeField(auto_now=True, verbose_name='Last Edited')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('last_used', models.DateTimeField(auto_now=True, verbose_name='Last Used')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tracker.Currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Wallet'),
        ),
        migrations.AddField(
            model_name='category',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Wallet'),
        ),
    ]
