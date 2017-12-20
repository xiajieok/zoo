from django.test import TestCase

# Create your tests here.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
i = 1
while i < 10:
    i += 1
    if i % 2 > 0:
        continue
    print(i)

print(i)
