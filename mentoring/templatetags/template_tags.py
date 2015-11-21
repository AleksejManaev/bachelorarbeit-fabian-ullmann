#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'preuss'
# http://stackoverflow.com/questions/6451304/django-simple-custom-template-tag-example

from django import template
from tag_parser import template_tag
from tag_parser.basetags import BaseNode

register = template.Library()


@template_tag(register, "sort_th")
class SortTableHeader(BaseNode):
    # Todo: order_by muss ausgetauscht und nicht zusätzlich angehängt werden
    min_args = max_args = 2

    def render_tag(self, context, *tag_args, **tag_kwargs):
        field = tag_args[1]
        ctx = {'name': tag_args[0], }
        request = context['request']
        new_query_dict = request.GET.copy()
        order_by = request.GET.get('order_by', 'id')
        if order_by == field:
            ctx['order'] = '▲'
            new_query_dict['order_by'] = '-' + order_by
        elif order_by[0] == '-' and order_by[1:] == field:
            ctx['order'] = '▼'
            new_query_dict['order_by'] = order_by[1:]
        else:
            ctx['order'] = ''
            new_query_dict['order_by'] = field

        return '<th><a href="{path}?{query_string}">{name} {order}</a></th>'.format(path=request.path, query_string=new_query_dict.urlencode(), **ctx)
