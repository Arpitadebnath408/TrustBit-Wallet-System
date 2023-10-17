# Generated by Django 4.2.6 on 2023-10-14 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserWalletDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('balance1', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('transactions', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('total_sent', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('total_sent1', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('total_received', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('total_received1', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('private_key', models.CharField(max_length=500)),
                ('public_key', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('live_bitcoin_price', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('balance_usd', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('total_sent_usd', models.CharField(blank=True, default=0, max_length=500, null=True)),
                ('total_received_usd', models.CharField(blank=True, default=0, max_length=500, null=True)),
            ],
        ),
    ]
