# Generated by Django 2.1.7 on 2020-07-18 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('champions', '0021_effect_effect_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, unique=True)),
                ('is_percentage', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='EffectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, unique=True)),
                ('is_percentage', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ScalingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, unique=True)),
                ('is_percentage', models.BooleanField()),
            ],
        ),
        migrations.AlterField(
            model_name='ability',
            name='cost2_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost2_type', to='champions.CostType'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='cost_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost_type', to='champions.CostType'),
        ),
        migrations.AlterField(
            model_name='effect',
            name='effect_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_type', to='champions.EffectType'),
        ),
        migrations.AlterField(
            model_name='effect',
            name='scaling2_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scaling2_type', to='champions.ScalingType'),
        ),
        migrations.AlterField(
            model_name='effect',
            name='scaling_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scaling_type', to='champions.ScalingType'),
        ),
    ]
