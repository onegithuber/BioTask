#!/usr/bin/env python
# coding=utf-8
import base64
import os, csv
from email import MIMEText

from django.shortcuts import render, render_to_response
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from form import RegisterForm, EditForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from models import Tast, Platform
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from collections import OrderedDict
from django.contrib.auth.decorators import permission_required
from django.core.mail import EmailMultiAlternatives
from email.header import make_header, Header
from django.core import serializers
from tast_manage.settings import PROJECT_ROOT
from django.core.servers.basehttp import FileWrapper

from django.core.paginator import Paginator

"""
重写分页类
"""


class RangePaginator(Paginator):
    def __init__(self, object_list, per_page, range_num=5, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num

    def page(self, number):
        if number is not None and number != "":
            self.page_num = int(number)
        else:
            self.page_num = number
        return super(RangePaginator, self).page(number)

    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1
        if self.num_pages <= num_count:
            return range(1, self.num_pages + 1)
        num_list = [self.page_num]
        for i in range(1, self.range_num + 1):
            if self.page_num - i <= 0:
                num_list.append(num_count + self.page_num - i)
            else:
                num_list.append(self.page_num - i)

            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - num_count)
        num_list.sort()
        return num_list

    page_range_ext = property(_page_range_ext)


def home(request):
    return render_to_response('home.html', )


def loginview(request):
    errors = []
    username = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('username'):
            errors.append(0)
        else:
            username = request.POST.get('username')
        if not request.POST.get('password'):
            errors.append(1)
        else:
            password = request.POST.get('password')
        if username is not None and password is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = HttpResponseRedirect('/all')
                    response.set_cookie('username', username, 3600)
                    return response
                else:
                    errors.append(3)
            else:
                errors.append(2)
    return render_to_response('login.html', {'errors': errors}, context_instance=RequestContext(request)
                              )


def loginoutview(request):
    logout(request)
    return HttpResponseRedirect('/all')


class BaseMixmi(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixmi, self).get_context_data(**kwargs)
        context['platforms'] = Platform.objects.all()
        return context

    """
    将类视图增加使用login_required() 装饰器
    """

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(BaseMixmi, cls).as_view(**initkwargs)
        return login_required(view, login_url='/login/')


class RegisterView(FormView):
    template_name = 'register.html'
    success_url = '/all'
    form_class = RegisterForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)


class EditView(BaseMixmi, FormView):
    template_name = 'edit.html'
    success_url = '/all'
    form_class = EditForm

    def form_valid(self, form):
        # form = self.form_class(request.POST)
        name = form.cleaned_data.get('name')
        # sample_nume = form.cleaned_data.get('sample_num')
        analysis_name = form.cleaned_data.get('analysts_name')
        salesman = form.cleaned_data.get('salesman')
        # print analysis_name, salesman
        analysis_email = User.objects.get(id=analysis_name).email
        salesman_email = User.objects.get(username=salesman).email
        # inspection = form.cleaned_data.get('inspection')
        # quality = form.cleaned_data.get('qualitycontrl')
        # print salesman_email, analysis_email
        form.save()

        msg = EmailMultiAlternatives(name, '您好！您有新项目来了，请注意查收', from_email='bioinfo@capitalbiotech.com',
                                     to=[analysis_email, salesman_email])
        inspection_name = os.path.join(PROJECT_ROOT, list(Tast.objects.all())[-1].inspection.name.replace('/', '/'))
        # print inspection_name,list(Tast.objects.all())[-1].inspection.name
        quality_name = os.path.join(PROJECT_ROOT, list(Tast.objects.all())[-1].qualitycontrl.name.replace('/', '/'))
        # print quality_name,list(Tast.objects.all())[-1].qualitycontrl.name
        if os.path.isfile(inspection_name) and os.path.isfile(quality_name):
            msg.attach_file(inspection_name)
            msg.attach_file(quality_name)
            # send_mail(name, u'您好！您有新项目来了，请注意查收！', from_email='bioinfo@capitalbiotech.com',
            #           recipient_list=[analysis_email, salesman_email], fail_silently=True)
            msg.content_subtype = "html"
            msg.send()
        else:
            msg.content_subtype = "html"
            msg.send()
        return super(EditView, self).form_valid(form)


@login_required(login_url='/login/')
def index(request):
    user = request.user
    tasts = Tast.objects.all().order_by('-id')
    platforms = Platform.objects.all()
    #json = serializers.serialize('json', tasts)
    # print type(json)
    paginator = RangePaginator(tasts, 100)
    page_num = request.GET.get('page')
    try:
        tasts = paginator.page(page_num)
        print tasts.paginator.page_range_ext
    except PageNotAnInteger:
        tasts = paginator.page(1)
    except EmptyPage:
        tasts = paginator.page(paginator.num_pages)
    return render_to_response('index.html', locals())


def jsonlist(request):
    # draw = request.GET['draw']
    # start = int(request.GET['start'])
    # length = int(request.GET['length'])
    # order_column = int(request.GET['order[0][column]'])
    # order_direction = '' if request.GET['order[0][dir]'] == 'desc' else '-'
    # column = [i.name for n, i in enumerate(Tast._meta.get_fields()) if n == order_column][0]
    # global_search = request.GET['search[value]']
    all_objects = Tast.objects.all()
    # a=Tast._meta.get_all_field_names()
    columns = [i for i in Tast._meta.get_all_field_names()][1:]
    objects = []
    for i in all_objects.values():
        for j in columns:
            try:
                ret = i[j]
                objects.append(ret)
            except KeyError:
                pass
    filtered_count = all_objects.count()
    total_count = Tast.objects.count()
    return JsonResponse({

        "iTotalRecords": total_count,
        "iTotalDisplayRecords": filtered_count,
        "aaData": objects,
    })


@login_required(login_url='/login')
def platform(request, id):
    user = request.user
    platform = Platform.objects.get(id=id)
    tasts = platform.tast_set.all()
    platforms = Platform.objects.all()
    paginator = RangePaginator(tasts, 50)
    page_num = request.GET.get('page')
    try:
        tasts = paginator.page(page_num)
    except PageNotAnInteger:
        tasts = paginator.page(1)
    except EmptyPage:
        tasts = paginator.page(paginator.num_pages)
    return render_to_response('index.html', locals())


@login_required(login_url='/login')
def reedit(request, id):
    user = request.user
    errors = []
    tast = Tast.objects.get(id=id)
    platforms = Platform.objects.all()
    marker = 0
    for analyst in tast.analysts_name.all():
        analyst_name = str(analyst)
        user_name = str(user)
        if user_name == analyst_name or user.has_perm('tast.can_reedit_tast'):
            errors = []
            marker = 1
            break
        else:
            print type(user_name), user_name
            print type(analyst_name), analyst_name
            errors.append('亲，这不是您的项目，so你没有权限哦！')
    if marker:
        if request.method == "POST":
            form = EditForm(request.POST)
            if form.is_valid():
                tast.platform = form.cleaned_data.get('platform')
                analysts_name = form.cleaned_data.get('analysts_name')
                tast.name = form.cleaned_data.get('name')
                tast.start_time = form.cleaned_data.get('start_time')
                tast.analysts_end_time = form.cleaned_data.get('analysts_end_time')
                tast.project_infomation = form.cleaned_data.get('project_infomation')
                tast.sample_num = form.cleaned_data.get('sample_num')
                tast.transmission_mode = form.cleaned_data.get('transmission_mode')
                tast.working_hour = form.cleaned_data.get('working_hour')
                salesman_name = form.cleaned_data.get('salesman')
                tast.inspection = form.cleaned_data.get('inspection')
                tast.qualitycontrl = form.cleaned_data.get('qualitycontrl')
                tast.habitude = form.cleaned_data.get('habitude')
                tast.detection_type = form.cleaned_data.get('detection_type')
                tast.analysts_demand = form.cleaned_data.get('analysts_demand')
                tast.external_extension = form.cleaned_data.get('external_extension')
                tast.internal_extension = form.cleaned_data.get('internal_extension')
                tast.sequenom = form.cleaned_data.get('sequenom')
                tast.species = form.cleaned_data.get('species')
                tast.machine_hour = form.cleaned_data.get('machine_hour')
                tast.tastinfo = form.cleaned_data.get('tastinfo')
                tast.batch = form.cleaned_data.get('batch')
                tast.additional_analysis = form.cleaned_data.get('additional_analysis')
                tast.order_number = form.cleaned_data.get('order_number')
                tast.reads = form.cleaned_data.get('reads')
                tast.reads_length = form.cleaned_data.get('reads_length')
                tast.library_modus = form.cleaned_data.get('library_modus')
                tast.casaver = form.cleaned_data.get('casaver')
                tast.data_amount = form.cleaned_data.get('data_amount')
                supporter = form.cleaned_data.get('supporter')
                tast.raw_data = form.cleaned_data.get('raw_data')
                tast.external = form.cleaned_data.get('external')
                tast.internal = form.cleaned_data.get('internal')
                tast.internal_time = form.cleaned_data.get('internal_time')
                tast.external_time = form.cleaned_data.get('external_time')
                tast.priority = form.cleaned_data.get('priority')
                tast.error_reason = form.cleaned_data.get('error_reason')
                for analyst in analysts_name:
                    tast.analysts_name.add(analyst)
                tast.salesman.add(salesman_name)
                tast.supporter.add(supporter)
                tast.save()
                return HttpResponseRedirect('/all')
        else:
            if len(tast.salesman.all()) == 0:
                salesman_name = ""
            else:
                salesman_name = tast.salesman.all()[0]
            if len(tast.supporter.all()) == 0:
                supporter_name = ""
            else:
                supporter_name = tast.supporter.all()[0]
            form = EditForm(initial={
                'name': tast.name,
                'platform': tast.platform,
                'analysts_name': tast.analysts_name.all(),
                'start_time': tast.start_time,
                'analysts_end_time': tast.analysts_end_time,
                'project_infomation': tast.project_infomation,
                'sample_num': tast.sample_num,
                'transmission_mode': tast.transmission_mode,
                'working_hour': tast.working_hour,
                'salesman': salesman_name,
                'inspection': tast.inspection,
                'qualitycontrl': tast.qualitycontrl,
                'habitude': tast.habitude,
                'detection_type': tast.detection_type,
                'analysts_demand': tast.analysts_demand,
                'external_extension': tast.external_extension,
                'internal_extension': tast.internal_extension,
                'sequenom': tast.sequenom,
                'species': tast.species,
                'machine_hour': tast.machine_hour,
                'tastinfo': tast.tastinfo,
                'batch': tast.batch,
                'additional_analysis': tast.additional_analysis,
                'order_number': tast.order_number,
                'reads': tast.reads,
                'reads_length': tast.reads_length,
                'library_modus': tast.library_modus,
                'casaver': tast.casaver,
                'data_amount': tast.data_amount,
                'supporter': supporter_name,
                'raw_data': tast.raw_data,
                'external': tast.external,
                'internal': tast.internal,
                'internal_time': tast.internal_time,
                'external_time': tast.external_time,
                'priority': tast.priority,
                'error_reason': tast.error_reason,
            })
    return render_to_response('reedit.html', locals())


@login_required(login_url='/login')
def search(request):
    user = request.user
    s = request.GET.get('s', '')
    tasts = Tast.objects.filter(name__icontains=s)
    platforms = Platform.objects.all()
    paginator = Paginator(tasts, 30)
    page_num = request.GET.get('page')
    try:
        tasts = paginator.page(page_num)
    except PageNotAnInteger:
        tasts = paginator.page(1)
    except EmptyPage:
        tasts = paginator.page(paginator.num_pages)
    return render_to_response('search.html', locals())


@login_required(login_url='/login')
def detail(request, id):
    user = request.user
    tast = Tast.objects.get(id=id)
    platforms = Platform.objects.all()
    return render_to_response('detail.html', locals())


@login_required(login_url='/login')
def histogram(request):
    post_date = Tast.objects.dates('start_time', 'month')
    post_year = Tast.objects.dates('start_time', 'year')
    month_list = []
    year_list = []
    num_list = []
    for i in range(len(post_year)):
        year_list.append([])
    for x in range(len(post_year)):
        curyear = post_year[x].year
        for y in range(1, 13):
            curmonth = y
            temTasts = Tast.objects.filter(start_time__year=curyear).filter(start_time__month=curmonth)
            temTastsNum = len(temTasts)
            month_list.append(curmonth)
            num_list.append(temTastsNum)
        year_list[x].append(month_list)
        year_list[x].append(num_list)
        year_list[x].append(curyear)
        month_list = []
        num_list = []
    return render_to_response('tast_histogram.html', locals())


quarter_dict = {'1': [1, 2, 3], '2': [4, 5, 6], '3': [7, 8, 9], '4': [10, 11, 11]}


@login_required(login_url='/login')
def stacked_bar_chart(request):
    user = request.user
    platforms = Platform.objects.all()
    if request.method == 'POST':
        normal_list = []
        subsequent_list = []
        test_list = []
        leaguer_list = []
        quarter = request.POST.get('quarter')
        paas = request.POST.get('sequence')
        year = request.POST.get('year')
        quarters = Tast.QuarterObjects.get_quarter(quarter, paas, year)
        for month in quarter_dict[quarter]:
            normal = quarters.filter(start_time__month=month).filter(habitude=1).count()
            subsequent = quarters.filter(start_time__month=month).filter(habitude=2).count()
            test = quarters.filter(start_time__month=month).filter(habitude=3).count()
            leaguer = quarters.filter(start_time__month=month).filter(habitude=4).count()
            normal_list.append(normal)
            subsequent_list.append(subsequent)
            test_list.append(test)
            leaguer_list.append(leaguer)
        normal_list.append(quarters.filter(habitude=1).count())
        subsequent_list.append(quarters.filter(habitude=2).count())
        test_list.append(quarters.filter(habitude=3).count())
        leaguer_list.append(quarters.filter(habitude=4).count())
        return render_to_response('stacked_bar_chart.html', locals())
    return render_to_response('stacked_bar_chart.html', locals())


@login_required(login_url='/login')
def send_file(request, dirname, filename):
    filename = os.path.join(dirname, filename)
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='application/doc+xlsx')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


@login_required(login_url='/login')
def statistical_work_hours(request):
    user = request.user
    platforms = Platform.objects.all()
    # if request.method == 'POST':
    #     starttime = request.POST.get('starttime')
    #     endtime = request.POST.get('endtime')
    #     tasts = Tast.objects.filter(start_time__range=(starttime, endtime))
    #     response = HttpResponse(content_type='text/csv; charset=UTF-8')
    #     filename = str(starttime) + '_' + str(endtime) + '.csv'
    #     response['Content-Disposition'] = 'attachment; filename=%s' % filename
    #     write = csv.writer(response)
    #     write.writerow([u'合同号'.encode("gb2312"), u'k3订单'.encode("gb2312"), u'工时'.encode("gb2312")])
    #     for tast in tasts:
    #         write.writerow([tast.name, tast.order_number, tast.working_hour])
    #     return response
    if request.method == "POST":
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        tasts = Tast.objects.filter(start_time__range=(starttime, endtime))
        return render_to_response('working_hourtime.html', locals())
    return render_to_response('working_hourtime.html', locals())
