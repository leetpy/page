#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64

img = 'conf_mx_norm.png'

with open(img, "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    print(str)
