import os

from django.shortcuts import render, render_to_response
# Create your views here.
from django.views.generic.edit import CreateView
from xadmin.util import User
import tempfile
import zipfile
from primer_design.models import Primer
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext


class PrimerView(CreateView):
    template_name = 'primerDesign.html'
    model = Primer
    fields = ['name', 'sequen', 'rangelength', 'maxnumber']
    success_url = '/hla/success'

    def form_valid(self, form):
        # if fastaformat(form.cleaned_data['sequen'].name) == ".fasta":
        # os.mkdir("media/hla/" + form.cleaned_data['name'])
        form.save()
        if Primer.objects.all().count() != 0:
            script = 'perl extra_script/primers_specific_worksh_v3.pl -dir ' + 'media/hla/' + form.cleaned_data[
                'name'] + ' -fa ' + Primer.objects.all()[
                         Primer.objects.all().count() - 1].sequen.name + ' -range ' + str(form.cleaned_data[
                                                                                              'rangelength']) + ' -max ' + str(
                form.cleaned_data['maxnumber'])
        else:
            script = 'perl extra_script/primers_specific_worksh_v3.pl -dir ' + 'media/hla/' + form.cleaned_data[
                'name'] + ' -fa ' + Primer.objects.all()[
                         Primer.objects.all().count() - 1].sequen.name + ' -range ' + str(form.cleaned_data[
                                                                                              'rangelength']) + ' -max ' + str(
                form.cleaned_data['maxnumber'])
        print script
        os.system(script)
        return super(PrimerView, self).form_valid(form)


def fastaformat(filename):
    return os.path.splitext(filename)[1]


def successview(request):
    dirname = Primer.objects.all()
    # template = loader.get_template('down.html')
    # context = RequestContext(request, {'dirname': dirname})
    # return HttpResponse(template.render(context))
    return render_to_response('down.html', {'dirname': dirname})


def send_zipfile(request, dirname):
    path = "media/hla/" + dirname
    filename = os.path.join(path, "primer.zip")
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

# def send_zipfile(request):
#     """
#   Create a ZIP file on disk and transmit it in chunks of 8KB,
#   without loading the whole file into memory. A similar approach can
#   be used for large dynamic PDF files.
#   """
#     # temp = tempfile.TemporaryFile()
#     path = "media/hla/" + Primer.objects.all()[Primer.objects.all().count() - 1].name
#     archive = zipfile.ZipFile(os.path.join(path, "primer.zip"), 'w', zipfile.ZIP_DEFLATED)
#     filenamelist = ["poly.detail.txt"]
#     for index, filename in enumerate(filenamelist):
#         archive.write(os.path.join(path, filename), filename)
#     archive.close()
#     wrapper = FileWrapper(file(os.path.join(path, "primer.zip")), "rb")
#     response = StreamingHttpResponse(wrapper, content_type='application/zip')
#     response['Content-Disposition'] = 'attachment; filename=primer.zip'
#     print os.path.join(path, 'primer.zip'), os.path.getsize(os.path.join(path, 'primer.zip'))
#     response['Content-Length'] = os.path.getsize(os.path.join(path, 'primer.zip'))
#     # response['X-Accel-Redirect'] = "/hla/primerdown/{0}".format(
#     #     os.path.join(Primer.objects.all()[Primer.objects.all().count() - 1].name), "primer.zip")
#     return response
