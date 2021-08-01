# Generated by Django 3.2.4 on 2021-07-20 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finance', '0001_initial'),
        ('salonist', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainee',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.customuser')),
            ],
            options={
                'verbose_name': 'Trainee',
                'verbose_name_plural': 'Trainees',
            },
            bases=('user.customuser',),
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0.0)),
                ('date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('salonist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salonist.salonist')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salonist.service')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainee.trainee')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainee.training')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('amount', models.FloatField(default=0.0)),
                ('mpesa', models.CharField(max_length=100)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('finance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.finance')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainee.trainingapplication')),
            ],
        ),
        migrations.CreateModel(
            name='TraineeProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trainee.trainee')),
            ],
            options={
                'verbose_name': 'Trainee Profile',
                'verbose_name_plural': 'Trainees Profile',
            },
            bases=('user.profile',),
        ),
        migrations.CreateModel(
            name='TraineeFeedback',
            fields=[
                ('feedback_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.feedback')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainee.trainee')),
            ],
            options={
                'verbose_name': 'Trainee Feedback',
                'verbose_name_plural': 'Trainees Feedback',
            },
            bases=('user.feedback',),
        ),
    ]