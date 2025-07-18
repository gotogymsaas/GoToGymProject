# Generated by Django 5.2.4 on 2025-07-15 13:40

import django.db.models.deletion
import influencer.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InfluencerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referral_code', models.CharField(default=influencer.models.generate_referral_code, max_length=36, unique=True)),
                ('commission_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_referred', models.PositiveIntegerField(default=0)),
                ('total_sales', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='influencer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
