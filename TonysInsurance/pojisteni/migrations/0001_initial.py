# Generated by Django 4.2 on 2023-04-18 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pojistenec', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20)),
                ('creation_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=200)),
                ('sum_assurance', models.PositiveIntegerField()),
                ('premium', models.PositiveIntegerField()),
                ('tenure', models.PositiveIntegerField()),
                ('creation_date', models.DateField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pojisteni.category')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('admin_comment', models.CharField(default='Nothing', max_length=200)),
                ('asked_date', models.DateField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pojistenec.customer')),
            ],
        ),
        migrations.CreateModel(
            name='PolicyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Čeká na schválení', max_length=100)),
                ('creation_date', models.DateField(auto_now=True)),
                ('Policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pojisteni.policy')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pojistenec.customer')),
            ],
        ),
    ]