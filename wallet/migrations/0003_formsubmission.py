# Generated by Django 4.2.5 on 2023-10-02 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_alter_userwalletdetails_balance_and_more'),
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
    ]
