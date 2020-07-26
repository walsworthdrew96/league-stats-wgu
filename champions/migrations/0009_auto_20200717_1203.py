# Generated by Django 2.1.7 on 2020-07-17 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('champions', '0008_remove_ability_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ability',
            name='recharge_cooldown',
        ),
        migrations.AddField(
            model_name='ability',
            name='cooldown_rank1',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AddField(
            model_name='ability',
            name='cooldown_rank2',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AddField(
            model_name='ability',
            name='cooldown_rank3',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AddField(
            model_name='ability',
            name='cooldown_rank4',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AddField(
            model_name='ability',
            name='cooldown_rank5',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AddField(
            model_name='ability',
            name='max_stacks',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='ability',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='ability',
            name='recharge_cooldown_rank1',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AddField(
            model_name='ability',
            name='recharge_cooldown_rank2',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AddField(
            model_name='ability',
            name='recharge_cooldown_rank3',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AddField(
            model_name='ability',
            name='recharge_cooldown_rank4',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AddField(
            model_name='ability',
            name='recharge_cooldown_rank5',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='ability',
            name='max_charges',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='cost',
            name='rank1',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='cost',
            name='rank2',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='cost',
            name='rank3',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='cost',
            name='rank4',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='cost',
            name='rank5',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='effect',
            name='rank1',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='effect',
            name='rank2',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='effect',
            name='rank3',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='effect',
            name='rank4',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='effect',
            name='rank5',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='scaling',
            name='rank1',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='scaling',
            name='rank2',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='scaling',
            name='rank3',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='scaling',
            name='rank4',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
        migrations.AlterField(
            model_name='scaling',
            name='rank5',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20),
        ),
    ]