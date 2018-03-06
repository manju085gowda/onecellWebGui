try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django import forms
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.forms.formsets import BaseFormSet
from django.views.generic.edit import BaseFormView
from django.views.generic.edit import BaseCreateView
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.views.generic import View
from django.views.generic.edit import TemplateResponseMixin
from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import SingleObjectMixin

from ajax_forms.utils import LazyEncoder

FORM_SUBMITTED = "valid_submit"

class JSONResponseMixin(object):
    def render_to_json_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)

class RealSubmitMixin(object):
    def is_actual_submit(self):
        return True
        # if self.request.POST.get('submit') == 'true':
        #     return True
        # return False

class AjaxValidFormMixin(RealSubmitMixin):
    def form_valid(self, form):
        response = None
        if self.is_actual_submit():
            response = self.render_to_json_response({ 'valid': True, 'submitted': True })
        if self.is_actual_submit() and getattr(self, FORM_SUBMITTED, False):
            self.valid_submit(form)

        if not response:
            return self.render_to_json_response({ 'valid': True })
        return response


class AjaxInvalidFormMixin(JSONResponseMixin, TemplateResponseMixin):
    def get_form_class(self):
        """
        A form_class can either be defined by inheriting from AjaxValidatingForm and setting the
        form_class property or by adding the form_class in the url definition.
        """
        form_class = getattr(self, "form_class", False)
        if not form_class:
            form_class = self.kwargs["form_class"]
        return form_class


    def form_invalid(self, form):
        # Get the BoundFields which contains the errors attribute
        if isinstance(form, BaseFormSet):
            errors = {}
            formfields = {}
            for f in form.forms:
                for field in f.fields.keys():
                    formfields[f.add_prefix(field)] = f[field]
                for field, error in f.errors.iteritems():
                    errors[f.add_prefix(field)] = error
            if form.non_form_errors():
                errors['__all__'] = form.non_form_errors()
        else:
            formfields = dict([(fieldname, form[fieldname]) for fieldname in form.fields.keys()])
            errors = form.errors

        if self.request.POST.has_key('fields'):
            fields = self.request.POST.getlist('fields') + ['__all__']
            errors = dict([(key, val) for key, val in errors.iteritems() if key in fields])

        final_errors = {}
        for key, val in errors.iteritems():
            if '__all__' in key:
                final_errors[key] = val
            elif not isinstance(formfields[key].field, forms.FileField):
                html_id = formfields[key].field.widget.attrs.get('id') or formfields[key].auto_id
                html_id = formfields[key].field.widget.id_for_label(html_id)
                final_errors[html_id] = val
        data = {
            'valid': False or not final_errors,
            'errors': final_errors,
        }
        return self.render_to_json_response(data)

class AjaxFormView(AjaxValidFormMixin, AjaxInvalidFormMixin, FormView):
    pass

