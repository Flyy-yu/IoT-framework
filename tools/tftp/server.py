# -*- coding: utf-8 -*-
# Create by zli on 9/30/18

import tftpy

server = tftpy.TftpServer('./')
server.listen('0.0.0.0', 6969)