# Generated by Django 2.1.7 on 2020-07-17 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('champions', '0002_auto_20200717_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ability',
            name='cost1',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost_1', to='champions.Cost'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='cost2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost_2', to='champions.Cost'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='effect1',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_1', to='champions.Effect'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='effect2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_2', to='champions.Effect'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='effect3',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_3', to='champions.Effect'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='effect4',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_4', to='champions.Effect'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='effect5',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_5', to='champions.Effect'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='effect6',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_6', to='champions.Effect'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='effect7',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_7', to='champions.Effect'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='effect8',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_8', to='champions.Effect'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='effect9',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_9', to='champions.Effect'),
        ),
        migrations.AlterField(
            model_name='champion',
            name='ability_e1',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ability_e1', to='champions.Ability'),
        ),
        migrations.AlterField(
            model_name='champion',
            name='ability_e2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ability_e2', to='champions.Ability'),
        ),
        migrations.AlterField(
            model_name='champion',
            name='ability_q1',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ability_q1', to='champions.Ability'),
        ),
        migrations.AlterField(
            model_name='champion',
            name='ability_q2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ability_q2', to='champions.Ability'),
        ),
        migrations.AlterField(
            model_name='champion',
            name='ability_r1',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ability_r1', to='champions.Ability'),
        ),
        migrations.AlterField(
            model_name='champion',
            name='ability_r2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ability_r2', to='champions.Ability'),
        ),
        migrations.AlterField(
            model_name='champion',
            name='ability_w1',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ability_w1', to='champions.Ability'),
        ),
        migrations.AlterField(
            model_name='champion',
            name='ability_w2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ability_w2', to='champions.Ability'),
        ),
        migrations.AlterField(
            model_name='cost',
            name='cost_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost_type', to='champions.CostType'),
        ),
        migrations.AlterField(
            model_name='effect',
            name='effect_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='effect_type', to='champions.EffectType'),
        ),
        migrations.AlterField(
            model_name='effect',
            name='scaling_1',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scaling_1', to='champions.Scaling'),
        ),
        migrations.AlterField(
            model_name='effect',
            name='scaling_2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scaling_2', to='champions.Scaling'),
        ),
        migrations.AlterField(
            model_name='scaling',
            name='scaling_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scaling_type', to='champions.ScalingType'),
        ),
    ]
