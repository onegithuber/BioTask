#!/usr/bin/env python
# encoding: utf-8
import xadmin

from tast.models import Tast, Platform, Habitude, Sequenom, Chipbackup, Detection


class TastAdmin(object):
    search_fields = ('name',)
    serch_filter = ('')
    list_display = (
    'name', 'tastinfo','analysts_name', 'platform', 'start_time', 'analysts_end_time','working_hour', 'project_infomation',
    )

    def get_analyst(self, obj):
        return ",".join([p.name for p in obj.analysts_name.all()])


xadmin.site.register(Tast, TastAdmin)


class PlatformAdmin(object):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)


xadmin.site.register(Platform, PlatformAdmin)


class HabitudeAdmin(object):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)


xadmin.site.register(Habitude, HabitudeAdmin)


class SequenomAdmin(object):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)


xadmin.site.register(Sequenom, SequenomAdmin)


# class DeadlineAdmin(object):
#     search_fields = ('internal',)
#     list_filter = ('internal',)
#     list_display = ('internal',)
#
#
# xadmin.site.register(Deadline, DeadlineAdmin)


class ChipbackupAdmin(object):
    search_fields = ('tast',)
    list_filter = ('tast',)
    list_display = ('tast',)


xadmin.site.register(Chipbackup, ChipbackupAdmin)


class DetectionAdmin(object):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)


xadmin.site.register(Detection, DetectionAdmin)
