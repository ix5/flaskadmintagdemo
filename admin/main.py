#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView

from app import app, db
from models import *

from .fields import AdvancedTagField

class PostView(ModelView):

    page_size = 100

    column_auto_select_related = True

    column_list = (
                    'title',
                    'tags',
    )
    column_searchable_list = [
            'title',
            'tags.name',
    ]


    form_columns = (
            'title',
            'tags',
    )

    # Use form_extra_fields instead of form_overrides
    form_extra_fields = {
            'tags': AdvancedTagField(
                'Tags',
            ),
    }

    def __init__(self, model, session, *args, **kwargs):
        super(PostView, self).__init__(model, session, *args, **kwargs)
        self.static_folder = 'static'
        self.endpoint = 'admin'
        self.name = 'Posts'

class TagView(ModelView):
    page_size = 100
    def get_query(self):
        return self.session.query(self.model)\
                .order_by(self.model.id.desc())

admin = Admin(
    app,
    name='Tagging demo',
    template_mode='bootstrap3',
    index_view=PostView(
        Post, db.session,
        url='/admin'
    ),
)

admin.add_view(TagView(Tag, db.session))
