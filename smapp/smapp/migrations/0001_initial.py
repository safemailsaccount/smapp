# Generated by Django 3.1.7 on 2021-03-17 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_id', models.CharField(max_length=50)),
                ('receiver', models.TextField()),
                ('email_content', models.TextField()),
            ],
        ),
    ]
