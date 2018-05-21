#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/17 10:02
# @Author  : hardyxia
# @File    : maopao.py


def maopao(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


def bubble_sort(lists):
    # 冒泡排序
    count = len(lists)
    for i in range(0, count):
        for j in range(i + 1, count):
            if lists[i] > lists[j]:
                lists[i], lists[j] = lists[j], lists[i]
    return lists


print(maopao(nums=[1, 4, 7, 13, 2, 90]))
print(bubble_sort([1, 4, 7, 13, 2, 90]))
