#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 18:20
# @Author  : hardyxia
# @File    : pagination.py

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def page(request, queryset):
    '''分页'''
    list_per_page = 10  # 设置每页的数量
    paginator = Paginator(queryset, list_per_page)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        query_sets = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)  # 取第一页的记录
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        # 如果页码太大，没有相应的记录,取最后一页的记录
        query_sets = paginator.page(paginator.num_pages)
    return query_sets
