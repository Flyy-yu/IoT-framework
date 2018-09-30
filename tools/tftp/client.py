# -*- coding: utf-8 -*-
# Create by zli on 9/30/18

import tftpy

client = tftpy.TftpClient('127.0.0.1', 6969)
client.download('install.txt', 'down')