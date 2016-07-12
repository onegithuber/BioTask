#!/usr/bin/env python
# coding=utf-8
from django import forms
from django.contrib.auth.models import User, Group
from models import Platform, Tast, Habitude, Detection, Sequenom


class RegisterForm(forms.Form):
    username = forms.CharField(
        label=u'姓名',
        help_text=u'昵称，不能包含空格和@字符。',
        max_length=20,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label=u'邮箱',
        help_text=u'邮箱可用于登录，最重要的是需要邮箱来找回密码，所以请输入您的可用邮箱。',
        max_length=50,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    password = forms.CharField(
        label=u'密码',
        help_text=u'密码只有长度要求，长度为 6 ~ 18 。',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    confirm_password = forms.CharField(
        label=u'确认密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label=u'请选择身份',
        label=u'身份',
        required=True,
    )

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        group = self.cleaned_data['group']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.groups.add(group)
        user.save()


TRANS = (
    (0, '网络共享'),
    (1, '刻盘'),
    (2, '网络共享+刻盘'),
)
PRIORITY = {
    (0, '标准'),
    (1, '加急'),
}


class EditForm(forms.Form):
    platform = forms.ModelChoiceField(
        queryset=Platform.objects.all(),
        label=u'平台*',
        error_messages={'required': u'必选项'},
        widget=forms.Select(
            attrs={'class': 'form-control select select-primary mrs mbm', "data-toggle": "select"}),
        required=True,
    )
    name = forms.CharField(
        label=u'合同号*',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
    )
    start_time = forms.DateField(
        label=u'分析日期*',
        error_messages={'required': u'必选项'},
        required=True,
        widget=forms.TextInput(),
    )
    analysts_end_time = forms.DateField(
        label=u'刻盘日期',
        required=False,
        widget=forms.TextInput(),
    )
    project_infomation = forms.CharField(
        label=u'备注',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'width:320px'}),
    )
    sample_num = forms.IntegerField(
        label=u'样品数目*',
        error_messages={'required': u'必选项'},
        required=True,
    )
    working_hour = forms.IntegerField(
        label=u'工时',
        required=False,
    )
    machine_hour = forms.IntegerField(
        label=u'机时',
        required=False,
    )
    transmission_mode = forms.ChoiceField(
        label=u'状态',
        widget=forms.Select(
            attrs={'class': 'form-control select select-primary mrs mbm', "data-toggle": "select"}),
        choices=TRANS,
    )
    analysts_name = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name=u'分析人员'),
        label=u'负责人*',
        error_messages={'required': u'必选项'},
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'type': 'checkboxlist'}),
    )
    salesman = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name=u'销售人员'),
        label=u'销售人员*',
        error_messages={'required': u'必选项'},
        widget=forms.Select(
            attrs={'class': 'form-control select select-primary mrs mbm', "data-toggle": "select"}),
        required=True,
    )
    sequenom = forms.ModelChoiceField(
        queryset=Sequenom.objects.all(),
        label=u'芯片商*',
        error_messages={'required': u'必选项'},
        widget=forms.Select(
            attrs={'class': 'form-control select select-primary mrs mbm', "data-toggle": "select"}),
        required=True,
    )
    inspection = forms.FileField(
        label=u'检测报告',
        required=False,
    )
    qualitycontrl = forms.FileField(
        label=u'质检报告',
        required=False,
    )
    habitude = forms.ModelChoiceField(
        queryset=Habitude.objects.all(),
        label=u'工作性质*',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control select select-primary mrs mbm', "data-toggle": "select"}),
        error_messages={'required': u'必选项'},
    )
    detection_type = forms.ModelChoiceField(
        queryset=Detection.objects.all(),
        label=u'检测类型*',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control select select-primary mrs mbm', "data-toggle": "select"}),
        error_messages={'required': u'必选项'}
    )
    analysts_demand = forms.TypedChoiceField(
        label=u'分析需求',
        coerce=lambda x: x == 'True',
        required=False,
        choices=((False, 'False'), (True, 'True')),
        widget=forms.RadioSelect
    )
    internal_extension = forms.TypedChoiceField(
        label=u'内部延期',
        coerce=lambda x: x == 'True',
        choices=((False, 'False'), (True, 'True')),
        widget=forms.RadioSelect,
        required=False,
    )
    external_extension = forms.TypedChoiceField(
        label=u'外部延期',
        coerce=lambda x: x == 'True',
        choices=((False, 'False'), (True, 'True')),
        widget=forms.RadioSelect,
        required=False,
    )
    species = forms.CharField(
        label=u'物种*',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
    )
    tastinfo = forms.CharField(
        label='合同详情',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    batch = forms.IntegerField(
        label='批次',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    additional_analysis = forms.CharField(
        label='超过芯片分析',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    order_number = forms.CharField(
        label='K3订单',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    reads = forms.CharField(
        label='Reads/样品',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    reads_length = forms.CharField(
        label='Reads长度',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    library_modus = forms.CharField(
        label='建库方法',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    casaver = forms.CharField(
        label='数据拆分',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    data_amount = forms.CharField(
        label='数据量/样品',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    supporter = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name=u'技术支持'),
        label=u'技术支持*',
        error_messages={'required': u'必选项'},
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control select select-primary mrs mbm', "data-toggle": "select"}),
    )
    raw_data = forms.DateField(
        label=u'原始数据给出时间',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
    )
    internal = forms.IntegerField(
        label='内部周期（天）',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    external = forms.IntegerField(
        label='外部周期（天）',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
        required=False,
    )
    internal_time = forms.DateField(
        label=u'内部到期时间',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
    )
    external_time = forms.DateField(
        label=u'外部到期时间',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'}),
    )
    priority = forms.ChoiceField(
        label=u'优先级*',
        choices=PRIORITY,
        widget=forms.Select(
            attrs={'class': 'form-control select select-primary mrs mbm', "data-toggle": "select"}),
    )
    error_reason = forms.CharField(
        label=u'错误原因',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:320px'})
    )

    def save(self):
        platform = self.cleaned_data['platform']
        analysts_name = self.cleaned_data['analysts_name']
        name = self.cleaned_data['name']
        start_time = self.cleaned_data['start_time']
        analysts_end_time = self.cleaned_data['analysts_end_time']
        project_infomation = self.cleaned_data['project_infomation']
        sample_num = self.cleaned_data['sample_num']
        transmission_mode = self.cleaned_data['transmission_mode']
        working_hour = self.cleaned_data['working_hour']
        salesman_name = self.cleaned_data['salesman']
        inspection = self.cleaned_data['inspection']
        qualitycontrl = self.cleaned_data['qualitycontrl']
        habitude_name = self.cleaned_data['habitude']
        detection_type_name = self.cleaned_data['detection_type']
        analysts_demand = self.cleaned_data['analysts_demand']
        external_extension = self.cleaned_data['external_extension']
        internal_extension = self.cleaned_data['internal_extension']
        sequenom = self.cleaned_data['sequenom']
        species = self.cleaned_data['species']
        machine_hour = self.cleaned_data['machine_hour']
        tastinfo = self.cleaned_data['tastinfo']
        batch = self.cleaned_data['batch']
        additional_analysis = self.cleaned_data['additional_analysis']
        order_number = self.cleaned_data['order_number']
        reads = self.cleaned_data['reads']
        reads_length = self.cleaned_data['reads_length']
        library_modus = self.cleaned_data['library_modus']
        casaver = self.cleaned_data['casaver']
        data_amount = self.cleaned_data['data_amount']
        supporter = self.cleaned_data['supporter']
        raw_data = self.cleaned_data['raw_data']
        external = self.cleaned_data['external']
        internal = self.cleaned_data['internal']
        internal_time = self.cleaned_data['internal_time']
        external_time = self.cleaned_data['external_time']
        priority = self.cleaned_data['priority']
        error_reason = self.cleaned_data['error_reason']
        n = Tast.objects.create(name=name, start_time=start_time, analysts_end_time=analysts_end_time,
                                project_infomation=project_infomation, working_hour=working_hour,
                                transmission_mode=transmission_mode, sample_num=sample_num, platform=platform,
                                habitude=habitude_name, detection_type=detection_type_name, sequenom=sequenom,
                                inspection=inspection, qualitycontrl=qualitycontrl, analysts_demand=analysts_demand,
                                internal_extension=internal_extension, external_extension=external_extension,
                                species=species, machine_hour=machine_hour, tastinfo=tastinfo, batch=batch,
                                additional_analysis=additional_analysis, order_number=order_number, reads=reads,
                                reads_length=reads_length, library_modus=library_modus, casaver=casaver,
                                data_amount=data_amount, raw_data=raw_data, external=external, internal=internal,
                                internal_time=internal_time, external_time=external_time, priority=priority,
                                error_reason=error_reason)
        for analyst in analysts_name:
            n.analysts_name.add(analyst)
        n.salesman.add(salesman_name)
        n.supporter.add(supporter)
        n.save()
