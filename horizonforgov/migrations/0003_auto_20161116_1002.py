# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-16 10:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('horizonforgov', '0002_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Floor', models.CharField(max_length=255, verbose_name='\u697c\u5c42')),
                ('Unit', models.CharField(max_length=255, verbose_name='\u5355\u5143\u533a\u57df')),
                ('Status', models.CharField(max_length=255, verbose_name='\u72b6\u6001')),
                ('Deco', models.CharField(max_length=255, verbose_name='\u88c5\u4fee')),
                ('LeaseAvailability', models.DateField(verbose_name='\u53ef\u79df\u65e5\u671f')),
                ('Area', models.CharField(max_length=255, verbose_name='\u53ef\u79df\u8d41\u9762\u79ef')),
                ('Eff', models.CharField(max_length=255, verbose_name='\u5f97\u623f\u7387')),
                ('UnitPrice', models.CharField(max_length=255, verbose_name='\u51fa\u552e\u5355\u4ef7')),
                ('UnitRental', models.CharField(max_length=255, verbose_name='\u79df\u8d41\u5355\u4ef7')),
                ('ManagementFee', models.CharField(max_length=255, verbose_name='\u7269\u4e1a\u7ba1\u7406\u8d39')),
                ('UpdateDate', models.DateField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ImageId', models.CharField(max_length=255)),
                ('DocumentId', models.CharField(max_length=255)),
                ('NameUnicode', models.CharField(max_length=255, unique=True, verbose_name='\u8f7d\u4f53\u540d\u79f0')),
                ('GradeCode', models.CharField(default='', max_length=10, verbose_name='\u7ea7\u522b\u5b9a\u4f4d')),
                ('StreetNameUnicode', models.CharField(default='', max_length=255, verbose_name='\u8857\u9053(CN)')),
                ('StreetFrom', models.CharField(max_length=255, verbose_name='\u95e8\u724c\u53f7')),
                ('YearBuilt', models.CharField(default='', max_length=255, verbose_name='\u5b8c\u5de5\u65f6\u95f4')),
                ('Latitude', models.DecimalField(decimal_places=9, max_digits=12, verbose_name='\u7eac\u5ea6')),
                ('Longitude', models.DecimalField(decimal_places=9, max_digits=12, verbose_name='\u7ecf\u5ea6')),
                ('Type', models.CharField(default='', max_length=255, verbose_name='\u7c7b\u578b')),
                ('VacancyRatio', models.CharField(max_length=255, verbose_name='\u7a7a\u7f6e\u7387')),
                ('EfficiencyPercent', models.CharField(max_length=255, verbose_name='\u5f97\u623f\u7387')),
                ('AvailabilityCount', models.IntegerField(max_length=255, verbose_name='\u53ef\u79df\u8d41\u5355\u5143\u6570\u91cf')),
                ('UpdateDate', models.DateField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('StoryCount', models.CharField(max_length=255, verbose_name='\u603b\u697c\u5c42')),
                ('RentableBuildingArea', models.CharField(max_length=255, verbose_name='\u53ef\u79df\u8d41\u603b\u9762\u79ef')),
                ('TypicalFloorSize', models.CharField(max_length=255, verbose_name='\u6807\u51c6\u697c\u5c42\u9762\u79ef')),
                ('YearRenovated', models.CharField(default='', max_length=255, verbose_name='\u91cd\u88c5\u4fee\u65e5\u671f')),
                ('SubmarketCluster', models.CharField(max_length=255, verbose_name='\u6240\u5c5e\u5206\u4e2d\u5fc3\u533a\u57df')),
                ('CeilingHeightRange', models.CharField(max_length=255, verbose_name='\u5c42\u9ad8\u8303\u56f4')),
                ('CarParking', models.CharField(max_length=255, verbose_name='\u8f66\u4f4d\u6570')),
                ('ParkingRatio', models.CharField(max_length=255, verbose_name='\u8f66\u4f4d\u6bd4')),
                ('LandArea', models.CharField(max_length=255, verbose_name='\u5360\u5730\u9762\u79ef')),
                ('AddressLine1', models.CharField(max_length=255, verbose_name='\u5730\u5740')),
                ('PropertyTypeName', models.CharField(default='', max_length=255, verbose_name='\u8f7d\u4f53\u7c7b\u578b')),
                ('BuildingTypeName', models.CharField(default='', max_length=255, verbose_name='\u5efa\u7b51\u7c7b\u578b')),
                ('MetroLinkage', models.CharField(default='', max_length=255, verbose_name='\u5730\u94c1\u4fe1\u606f')),
                ('Positioning', models.CharField(default='', max_length=255, verbose_name='\u8f7d\u4f53\u6863\u6b21\u5b9a\u4f4d')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.FileField(upload_to='./upload/')),
                ('Property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horizonforgov.Property', verbose_name='\u6240\u5c5e\u8f7d\u4f53')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TenantName', models.CharField(max_length=255, verbose_name='\u79df\u6237\u540d\u79f0')),
                ('TenantType', models.CharField(max_length=255, verbose_name='\u79df\u6237\u5206\u7c7b')),
                ('TenantStatus', models.CharField(max_length=255, verbose_name='\u79df\u6237\u72b6\u6001')),
                ('TenantStartDate', models.DateField(verbose_name='\u79df\u8d41\u8d77\u59cb\u65f6\u95f4')),
                ('TenantEndDate', models.DateField(verbose_name='\u79df\u8d41\u5230\u671f\u65f6\u95f4')),
                ('PhoneNumber', models.CharField(max_length=255, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('ContactorName', models.CharField(max_length=255, verbose_name='\u8054\u7cfb\u4eba\u59d3\u540d')),
                ('ContactorPosition', models.CharField(max_length=255, verbose_name='\u8054\u7cfb\u4eba\u79f0\u8c13')),
                ('Description', models.CharField(max_length=255, verbose_name='\u5907\u6ce8')),
                ('Property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horizonforgov.Property', verbose_name='\u6240\u5c5e\u8f7d\u4f53')),
            ],
        ),
        migrations.AddField(
            model_name='availability',
            name='Property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horizonforgov.Property', verbose_name='\u6240\u5c5e\u8f7d\u4f53'),
        ),
    ]
