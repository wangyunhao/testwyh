# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput
from models import Property, Availability, Tenant

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"用户名",
            }
        ),
    )    
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码",
            }
        ),
    )  
    
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()
            
            
class PropertyForm(forms.Form):
    class Meta:
        model = Property
        only = ['NameUnicode', 'Name', 'VacancyRatio', 'AvailabilityCount',
            'RentableBuildingArea', 'GradeCode',
            'StreetNameUnicode', 'StreetFrom', 'SubmarketCluster',
            'YearBuilt', 
            'Latitude', 'Longitude', 'Type',  'EfficiencyPercent', 
            'StoryCount', 'TypicalFloorSize',
            'YearRenovated', 'CeilingHeightRange', 'DriverIns', 'ParkingRatio', 
            'LandArea', 'PropertyTypeName', 'BuildingTypeName', 'MetroLinkage',
            'Positioning', 'AreaRetail']
            
    _field_order = ['NameUnicode', 'Name', 'VacancyRatio', 'AvailabilityCount',
            'RentableBuildingArea', 'GradeCode',
            'StreetNameUnicode', 'StreetFrom', 'SubmarketCluster',
            'YearBuilt', 
            'Latitude', 'Longitude', 'Type',  'EfficiencyPercent', 
            'StoryCount', 'TypicalFloorSize',
            'YearRenovated', 'CeilingHeightRange', 'DriverIns', 'ParkingRatio', 
            'LandArea', 'PropertyTypeName', 'BuildingTypeName', 'MetroLinkage',
            'Positioning', 'AreaRetail', 'Photo', 'PDF']
    
    Image = FileField(u'上传载体图片',validators=[
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    Document = FileField(u'上传载体资料文档',validators=[
        FileAllowed(['pdf'], 'PDFs only!')
    ])
    
    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        field_order = getattr(self, '_field_order')
        visited = []
        if field_order:
            new_fields = OrderedDict()
            for field_name in field_order:
                if field_name in self._fields:
                    new_fields[field_name] = self._fields[field_name]
                    visited.append(field_name)
            for field_name in self._fields:
                if field_name in visited:
                    continue
                new_fields[field_name] = self._fields[field_name]
            self._fields = new_fields  
        

class AvailabilityForm(ModelForm):
    class Meta:
        model = Availability
        only = ['Floor', 'Unit', 'Status', 'Deco', 'LeaseAvailability', 'Area',
                'Eff', 'UnitPrice', 'UnitRental', 'ManagementFee']



class TenantForm(ModelForm):
    class Meta:
        model = Tenant
        only = ['TenantName', 'TenantType', 'TenantStatus', 'TenantProperty', 'TenantStartDate1', 'TenantStartDate2', 'TenantStock','PhoneNumber',
                'ContactorName', 'ContactorPhone', 'ContactorPosition', 'Description']