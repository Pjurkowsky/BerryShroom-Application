# Generated by Django 3.2.7 on 2021-10-01 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Relay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('display_name', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.BooleanField(default=False)),
                ('mode', models.CharField(choices=[('M', 'MANUAL'), ('A', 'AUTO'), ('S', 'SENSOR'), ('T1', 'TIME_1'), ('T2', 'TIME_2')], max_length=2)),
                ('t_on', models.CharField(default='00:00:00', max_length=9)),
                ('t_off', models.CharField(default='00:00:00', max_length=9)),
                ('interval', models.IntegerField(default=0)),
                ('hysteresis', models.IntegerField(default=0)),
                ('set_value', models.IntegerField(default=0)),
                ('sensor_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('display_name', models.CharField(blank=True, max_length=20, null=True)),
                ('delay_time', models.IntegerField(blank=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('relays', models.ManyToManyField(to='mushfarm.Relay')),
            ],
        ),
    ]