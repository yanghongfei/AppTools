#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/22 18:16
# @Author  : Fred Yang
# @File    : itsm_upload_file.py
# @Role    : 简单文件上传功能


import os
import tornado.web

Base_DIR = os.path.dirname((os.path.abspath('__file__')))


class UpFileHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.write('<!DOCTYPE html>\
                    <html lang="en">\
                    <head>\
                        <meta charset="UTF-8">\
                        <title>Title</title>\
                    </head>\
                    <body>\
                        <form action="upload_file" method="post" enctype="multipart/form-data">\
                            <input type="file" name="file">\
                            <input type="submit" value="点我上传">\
                        </form>\
                    </body>\
                    </html>')

    def post(self, *args, **kwargs):
        file_metas = self.request.files['file']
        for meta in file_metas:
            filename = meta['filename']
            filepath = os.path.join(Base_DIR + '/static/files', filename)
            with open(filepath, 'wb') as f:
                f.write(meta['body'])
                return self.write('finished!')
