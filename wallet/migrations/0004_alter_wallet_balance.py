# Generated by Django 4.2.3 on 2023-07-17 13:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallet", "0003_alter_wallet_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="balance",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
