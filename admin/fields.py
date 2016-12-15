from wtforms import widgets
from flask_admin.form import Select2TagsField

from app import app, db
from models import *

class AdvancedTagWidget(widgets.Select):
    """
        `Select2 <https://github.com/select2/select2>`_ styled select widget.

        You must include select2.js, form-x.x.x.js and select2 stylesheet for it to
        work.
    """
    def __call__(self, field, **kwargs):
        # For select2 v4:
        kwargs.setdefault('data-tags', '1')
        # For select2 v3.x and vanilla flask-admin form.js:
        #  kwargs.setdefault('data-role', u'select2-tags')

        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super(AdvancedTagWidget, self).__call__(field, **kwargs)


class AdvancedTagField(Select2TagsField):
    """
    Custom tag field. Supports tags that do not exist yet.
    """

    widget = AdvancedTagWidget(multiple=True)


    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):

        if valuelist:
            self.data = []
            for tagname in valuelist:
                rv = Tag.query.filter_by(name=tagname).first()
                if rv:
                    self.data.append(rv)
                else:
                    self.data.append(Tag(name=tagname))
        else:
            #  self.data = u''
            #  self.data = None
            # You can use whatever empty type you want, just be consistent
            self.data = []

    def iter_choices(self):

        self.blank_text = ""

        tags = list(set([str(tag.name) for tag in Tag.query.all()]))
        model_tags = [tag.name for tag in self.object_data]

        self.choices = [[tag, tag] for tag in tags]

        # Yield empty object in order to have an empty placeholder
        yield (u'__None', self.blank_text, self.data is None)

        for value, label in self.choices:
            yield (value, label, value in model_tags)
