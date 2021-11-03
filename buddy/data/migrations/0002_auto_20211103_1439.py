# Generated by Django 3.2.8 on 2021-11-03 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candle',
            name='symbol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candles', to='data.symbol'),
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favourited_on', models.DateTimeField(auto_now=True)),
                ('symbol_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='data.symbol')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='favourite',
            constraint=models.UniqueConstraint(fields=('user_id', 'symbol_id'), name='unique_symbol_favourites'),
        ),
    ]
