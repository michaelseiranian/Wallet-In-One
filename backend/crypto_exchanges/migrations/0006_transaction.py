# Generated by Django 4.1.5 on 2023-03-09 22:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_exchanges', '0005_remove_cryptoexchangeaccount_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.CharField(max_length=15)),
                ('transaction_type', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('crypto_exchange_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto_exchanges.cryptoexchangeaccount')),
            ],
        ),
    ]
