# Generated by Django 3.2.4 on 2021-07-20 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.customuser')),
            ],
            options={
                'verbose_name': 'Finance',
                'verbose_name_plural': 'Finances',
            },
            bases=('user.customuser',),
        ),
        migrations.CreateModel(
            name='FinanceProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='finance.finance')),
            ],
            options={
                'verbose_name': 'Finance Profile',
                'verbose_name_plural': 'Finances Profile',
            },
            bases=('user.profile',),
        ),
        migrations.CreateModel(
            name='FinanceFeedback',
            fields=[
                ('feedback_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.feedback')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.finance')),
            ],
            options={
                'verbose_name': 'Finance Feedback',
                'verbose_name_plural': 'Finance Feedback',
            },
            bases=('user.feedback',),
        ),
    ]