import xadmin
from django.contrib import admin
from models import Platform, Tast, MyProfile
from django.contrib.auth.models import User
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class PlatformAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)


class ChiptastAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)


class NgstastAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)


class ChipbackAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)


# class AnalystsAdmin(admin.ModelAdmin):
#     search_fields = ('name',)
#     list_filter = ('name',)
#     list_display = ('name', 'email',)


class TastAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    serch_filter = ('')
    list_display = ('name', 'get_analyst', 'platform')

    def get_analyst(self, obj):
        return ",".join([p.name for p in obj.analysts_name.all()])


admin.site.register(Platform, PlatformAdmin)
# admin.site.register(MyProfile, AnalystsAdmin)
admin.site.register(Tast, TastAdmin)


# admin.site.register()
# admin.site.register()
# admin.site.register()
# admin.site.register()
# admin.site.register()
# admin.site.register()



