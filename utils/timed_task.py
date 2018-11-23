#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 10:12
# @Author  : Fred Yang
# @File    : timed_task.py
# @Role    : 定时任务


import datetime
from database import db_session
from models import EventReminder
from utils import const
from apscheduler.schedulers.blocking import BlockingScheduler
from utils.send_mail import MailAPI


def check_reminder_event():
    """
    用途：
        检查哪些事件需要进行邮件提醒
    逻辑：
        这里逻辑简单说明下如下：
        01. 先获取到所有事件的到期时间
        02. 获取所有事件中每条事件都需要提前多少天进行提醒
        03. 计算从哪天开始进行提醒（过期时间 - 提前提醒天数 = 开始提醒的日期）
        04. 计算出来的·开始提醒日期· <= 现在时间 都进行报警
    :return:
    """
    for event in db_session.query(EventReminder).all():
        print(event.name)
        now_time = datetime.datetime.now()  # 现在时间
        # 获取当天时间进行对比，是否触发报警机制（过期时间---提前时间 <= 现在时间  报警）
        start_reminder_time = event.expire_at - datetime.timedelta(days=int(event.advance_at))
        if start_reminder_time <= now_time:
            content = """
                    <!DOCTYPE html><html>
                    <head lang="en">
                    <meta charset="UTF-8">
                    <title></title>
                    <style type="text/css">
                        p {
                            width: 100%;
                            margin: 30px 0 30px 0;
                            height: 30px;
                            line-height: 30px;
                            text-align: center;

                        }
                        table {
                            width: 100%;
                            text-align: center;
                            border-collapse: collapse;
                        }

                        tr.desc {
                            background-color: gray;
                            height: 30px;
                        }
                        tr.desc td {
                            border-color: #ffffff;
                        }
                        td {
                            height: 30px;
                            border: 1px solid gray;
                        }
                    </style>
                    </head>
                    <body>"""

            content += """
                    <table>
                    <p>OpenDevOps事件提醒 </p>
                    <tr class='desc'>
                    <td>事件名称</td>
                    <td>事件内容</td>
                    <td>过期时间</td>

                    </tr>"""

            content += """
                    <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                     </tr>""".format(event.name, event.content, event.expire_at)
            content += """
                     </table>
                     </body>
                     </html>"""
            try:
                obj = MailAPI(mail_host=const.EMAIL_HOST, mail_port=const.EMAIL_PORT,
                              mail_user=const.EMAIL_HOST_USER,
                              mail_passwd=const.EMAIL_HOST_PASSWORD,
                              mail_ssl=const.EMAIL_USE_SSL)

                obj.send_mail(event.email, 'OpenDevOps', content, subtype='html', att='None')
            except Exception as e:
                print(e)


def exec_task():
    sched = BlockingScheduler()
    sched.add_job(check_reminder_event, 'interval', seconds=30)  # 每30s
    # sched.add_job(check_reminder_event, 'interval', hours=1)  # 每小时
    sched.start()


if __name__ == '__main__':
    exec_task()
