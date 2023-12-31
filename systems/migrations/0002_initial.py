# Generated by Django 4.2.6 on 2023-11-09 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agents', '0002_initial'),
        ('systems', '0001_initial'),
        ('fleet', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='markettransaction',
            name='ship_symbol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.ship'),
        ),
        migrations.AddField(
            model_name='markettransaction',
            name='trade_good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.tradegood'),
        ),
        migrations.AddField(
            model_name='markettradegoodlink',
            name='trade_good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.tradegood'),
        ),
        migrations.AddField(
            model_name='marketimportlink',
            name='trade_good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.tradegood'),
        ),
        migrations.AddField(
            model_name='marketexportlink',
            name='trade_good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.tradegood'),
        ),
        migrations.AddField(
            model_name='marketexchangelink',
            name='trade_good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.tradegood'),
        ),
        migrations.AddField(
            model_name='jumpgate',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jump_gate_origins', to='systems.waypoint'),
        ),
        migrations.AddField(
            model_name='jumpgate',
            name='waypoint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jump_gate_destinations', to='systems.waypoint'),
        ),
        migrations.AddField(
            model_name='constructionsite',
            name='TradeGood',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='construction_site', to='systems.tradegood'),
        ),
        migrations.AddField(
            model_name='constructionsite',
            name='waypoint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='construction_site', to='systems.waypoint'),
        ),
        migrations.AddField(
            model_name='markettransaction',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.market'),
        ),
        migrations.AddField(
            model_name='markettradegoodlink',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.market'),
        ),
        migrations.AddField(
            model_name='marketimportlink',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.market'),
        ),
        migrations.AddField(
            model_name='marketexportlink',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.market'),
        ),
        migrations.AddField(
            model_name='marketexchangelink',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.market'),
        ),
        migrations.AddField(
            model_name='market',
            name='exchanges',
            field=models.ManyToManyField(related_name='exchanges', through='systems.MarketExchangeLink', to='systems.tradegood', verbose_name='the list of goods that are bought and sold between agents at this market.'),
        ),
        migrations.AddField(
            model_name='market',
            name='exports',
            field=models.ManyToManyField(related_name='exports', through='systems.MarketExportLink', to='systems.tradegood', verbose_name='the list of goods that are exported from this market.'),
        ),
        migrations.AddField(
            model_name='market',
            name='imports',
            field=models.ManyToManyField(related_name='imports', through='systems.MarketImportLink', to='systems.tradegood', verbose_name='the list of goods that are sought as imports in this market.'),
        ),
        migrations.AddField(
            model_name='market',
            name='trade_goods',
            field=models.ManyToManyField(blank=True, related_name='market', through='systems.MarketTradeGoodLink', to='systems.tradegood', verbose_name='the list of goods that are traded at this market. Visible only when a ship is present at the market.'),
        ),
        migrations.AddField(
            model_name='chart',
            name='submitted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.agent', verbose_name='the agent that submitted the chart for this waypoint.'),
        ),
    ]
