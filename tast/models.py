# coding:utf-8
from comments.models import Comment
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# PLATFORM={
#     '0':'DNA芯片',
#     '1':'RNA芯片',
#     '2':'DNA测序',
#     '3':'RNA测序',
# }
from django.db.models import Q

TRANS = {
    '0': '网络共享',
    '1': '刻盘',
    '2': '网络共享+刻盘',
}

PRIORITY = {
    '0': '标准',
    '1': '加急',
}


class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field):
                    fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)


class Profile(object):
    __metaclass__ = ProfileBase


class MyProfile(Profile):
    nickname = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, default='beijing')


class Platform(models.Model):
    name = models.CharField(max_length=20, verbose_name='平台', blank=True, null=True)

    def __str__(self):
        return self.name


class Habitude(models.Model):
    name = models.CharField(max_length=20, verbose_name='工作性质', blank=True, null=True)

    def __str__(self):
        return self.name


class Detection(models.Model):
    name = models.CharField(max_length=20, verbose_name='检测类型', blank=True, null=True)

    def __str__(self):
        return self.name


class Sequenom(models.Model):
    name = models.CharField(max_length=20, verbose_name='芯片商', blank=True, null=True)

    def __str__(self):
        return self.name


# class Deadline(models.Model):
#     internal = models.IntegerField(verbose_name='内部周期', blank=True, null=True)
#     external = models.IntegerField(verbose_name='外部周期', blank=True, null=True)
#     internal_time = models.DateField(verbose_name='内部到期时间', blank=True, null=True)
#     external_time = models.DateField(verbose_name='外部到期时间', blank=True, null=True)
#     internal_extension = models.BooleanField(verbose_name='内部是否延期', blank=True)
#     external_extension = models.BooleanField(verbose_name='外部时候延期', blank=True)
quarter_dict = {'1': [1, 2, 3], '2': [4, 5, 6], '3': [7, 8, 9], '4': [10, 11, 11]}


class Quarter(models.Manager):
    def get_quarter(self, quarter, sequence, year):
        months = quarter_dict[quarter]
        quarter_tast = Tast.objects.all().filter(
            Q(start_time__month=int(months[0])) | Q(start_time__month=int(months[1])) | Q(
                start_time__month=int(months[2])), start_time__year=year).filter(platform=sequence)
        return quarter_tast


class Tast(models.Model):
    name = models.CharField(max_length=30, verbose_name='合同号')
    priority = models.CharField(max_length=20, choices=PRIORITY.items(), verbose_name='优先级')
    habitude = models.ForeignKey(Habitude, verbose_name='工作性质')
    detection_type = models.ForeignKey(Detection, verbose_name='检测类型')
    tastinfo = models.CharField(max_length=1000, verbose_name='合同详情', blank=True, null=True)
    species = models.CharField(max_length=20, verbose_name='物种', blank=True, null=True)
    sample_num = models.IntegerField(verbose_name='样品数目', blank=True, null=True)
    batch = models.IntegerField(verbose_name='批次', blank=True, null=True)
    sequenom = models.ForeignKey(Sequenom, blank=True, null=True, verbose_name='芯片商')
    additional_analysis = models.CharField(max_length=50, verbose_name='超过芯片张数的分析', blank=True, null=True)
    order_number = models.CharField(max_length=50, verbose_name='K3订单号', blank=True, null=True)
    reads = models.CharField(max_length=20, verbose_name='Reads/样品', blank=True, null=True)
    reads_length = models.CharField(max_length=20, verbose_name='reads长度', blank=True, null=True)
    library_modus = models.CharField(max_length=20, verbose_name='建库方法', blank=True, null=True)
    casaver = models.CharField(max_length=20, verbose_name='数据拆分', blank=True, null=True)
    data_amount = models.CharField(max_length=20, verbose_name='数据量/样本', blank=True, null=True)
    start_time = models.DateField(verbose_name='分析登记日期')
    analysts_name = models.ManyToManyField(User, related_name='chip_analysts_name', blank=True, verbose_name='负责人')
    supporter = models.ManyToManyField(User, related_name='chip_supporter', blank=True, verbose_name='技术支持')
    analysts_demand = models.BooleanField(blank=True, verbose_name='是否分析')
    raw_data = models.DateField(verbose_name='原始数据给出时间', blank=True, null=True)
    analysts_end_time = models.DateField(verbose_name='分析结果给出时间', blank=True, null=True)
    project_infomation = models.CharField(max_length=100, verbose_name='备注', blank=True, null=True)
    working_hour = models.IntegerField(verbose_name='工时', blank=True, null=True)
    machine_hour = models.IntegerField(verbose_name='机时', blank=True, null=True)
    transmission_mode = models.CharField(max_length=20, choices=TRANS.items(), blank=True, null=True,
                                         verbose_name='共享方式')
    platform = models.ForeignKey(Platform, blank=True, verbose_name='平台')
    # deadline = models.OneToOneField(Deadline, blank=True)
    salesman = models.ManyToManyField(User, related_name='chip_salesman', blank=True, verbose_name='销售')
    inspection = models.FileField(upload_to='inspection', blank=True, null=True, verbose_name='检测报告')
    qualitycontrl = models.FileField(upload_to='quality', blank=True, null=True, verbose_name='质控文件')
    internal = models.IntegerField(verbose_name='内部周期', blank=True, null=True)
    external = models.IntegerField(verbose_name='外部周期', blank=True, null=True)
    internal_time = models.DateField(verbose_name='内部到期时间', blank=True, null=True)
    external_time = models.DateField(verbose_name='外部到期时间', blank=True, null=True)
    internal_extension = models.BooleanField(verbose_name='内部是否延期', blank=True, default=False)
    external_extension = models.BooleanField(verbose_name='外部时候延期', blank=True, default=False)
    error_reason = models.CharField(verbose_name=u'出错原因', blank=True, null=True, max_length=200)
    comments = GenericRelation(Comment)  # 评论
    objects = models.Manager()
    QuarterObjects = Quarter()

    def __unicode__(self):
        return self.name


class Ngstast(models.Model):
    name = models.CharField(max_length=30, verbose_name='合同号')
    priority = models.CharField(max_length=20, choices=PRIORITY.items())
    habitude = models.OneToOneField(Habitude)
    detection_type = models.OneToOneField(Detection)
    tastinfo = models.CharField(max_length=100, verbose_name='项目信息')
    species = models.CharField(max_length=20, verbose_name='物种')
    sample_num = models.IntegerField(verbose_name='样品数目')
    reads = models.CharField(max_length=20, verbose_name='Reads/样品')
    reads_length = models.CharField(max_length=20, verbose_name='reads长度')
    library_modus = models.CharField(max_length=20, verbose_name='建库方法')
    casaver = models.CharField(max_length=20, verbose_name='数据拆分')
    data_amount = models.CharField(max_length=20, verbose_name='数据量/样本')
    start_time = models.DateField(verbose_name='分析登记日期')
    analysts_name = models.ManyToManyField(User, related_name='ngs_analysts_name')
    supporter = models.ManyToManyField(User, related_name='ngs_supporter')
    analysts_demand = models.NullBooleanField(blank=True)
    raw_data = models.DateField(verbose_name='原始数据给出时间')
    analysts_end_time = models.DateField(verbose_name='分析结果给出时间')
    project_infomation = models.CharField(max_length=100, verbose_name='项目信息', blank=True, null=True)
    working_hour = models.IntegerField(verbose_name='工时', blank=True, null=True)
    machine_hour = models.IntegerField(verbose_name='机时', blank=True, null=True)
    transmission_mode = models.CharField(max_length=20, choices=TRANS.items())
    platform = models.ForeignKey(Platform)
    # deadline = models.OneToOneField(Deadline)
    salesman = models.ManyToManyField(User, related_name='ngs_salesman')
    inspection = models.FileField(upload_to='inspection')
    qualitycontrl = models.FileField(upload_to='quality')
    internal = models.IntegerField(verbose_name='内部周期', blank=True, null=True)
    external = models.IntegerField(verbose_name='外部周期', blank=True, null=True)
    internal_time = models.DateField(verbose_name='内部到期时间', blank=True, null=True)
    external_time = models.DateField(verbose_name='外部到期时间', blank=True, null=True)
    internal_extension = models.NullBooleanField(verbose_name='内部是否延期', blank=True)
    external_extension = models.NullBooleanField(verbose_name='外部时候延期', blank=True)

    def __str__(self):
        return self.name


# class Analysts(models.Model):
#     name = models.CharField(max_length=20, verbose_name='负责人')
#     email = models.EmailField()
#
#     def __str__(self):
#         return self.name


class Ngsbackup(models.Model):
    backuper = models.OneToOneField(User)
    tast = models.OneToOneField(Ngstast)
    disk_id = models.CharField(max_length=50, verbose_name='备份硬盘')
    backup_time = models.DateField(verbose_name='备份日期')


class Chipbackup(models.Model):
    backuper = models.OneToOneField(User)
    tast = models.OneToOneField(Tast)
    disk_id = models.CharField(max_length=50, verbose_name='备份硬盘')
    backup_time = models.DateField(verbose_name='备份日期')


class NoReadMessage(models.Model):
    user_id = models.OneToOneField(User, verbose_name=u'用户id')
    tast_id = models.OneToOneField(Tast, verbose_name=u'项目id')
    hasreaded = models.IntegerField(verbose_name=u'已读消息')

    def __str__(self):
        return self.hasreaded


