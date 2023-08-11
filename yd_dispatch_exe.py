# -*-coding:utf-8-*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox, QLabel, QComboBox, \
    QTextBrowser, QDesktopWidget, QVBoxLayout, QHBoxLayout
from PyQt5 import QtCore
import os
import shutil
import glob
from PyQt5.QtGui import QFont
# from qt_material import apply_stylesheet
import requests
import json
import time
import requests

# 请求方法
method = ['GET', 'POST']


def callApi(url, data, headers=None, method=None):
    """
    调用接口返回json数据(字典)
    """
    if method == 'GET':
        result = requests.get(url=url, data=data, headers=headers).json()
        return result
    elif method == 'POST':
        result = requests.post(url=url, data=data, headers=headers).json()
        return result


def getAccessToken():
    """
    获取accessToken
    :return:accessToken
    """
    accessToken = callApi(
        urls['getAccessToken'].format(informationOfDispatch['accessKeyId'], informationOfDispatch['accessKeySecret']),
        None, {'Content-Type': 'application/x-www-form-urlencoded'}, method[0])['data']['accessToken']
    print('已获取accessToken：{}'.format(accessToken))
    print('-----------------------帅气的分割线-------------------------')
    return accessToken


def query_application(accessToken):  # 获取应用列表
    url = "https://api.yingdao.com/oapi/robot/v2/query"
    headers = {
        "Authorization": f"Bearer {accessToken}"
    }
    data = callApi(url, None, headers, method[0])
    data_list = [{"账号名称": i["ownerName"], "应用名称": i["robotName"], "robotUuid": i["robotUuid"]} for i in data["data"]]
    yy_list = [x['应用名称'] for x in data_list]
    return {'完整信息': data_list, '应用列表': yy_list}


def startJob(accessToken):
    """
    启动任务，并返回jobUuid
    :return:jobUuid
    """
    data = json.dumps({
        "accountName": informationOfDispatch["accountName"],
        "robotUuid": informationOfDispatch["robotUuid"],
        "params": informationOfrobot
    })
    headers = {'Content-Type': 'application/json', 'authorization': 'Bearer {}'.format(accessToken)}
    jobUuid = callApi(urls['startJob'], data, headers, method[1])['data']['jobUuid']
    print('已获取jobUuid：' + jobUuid)
    print('-----------------------帅气的分割线-------------------------')
    return jobUuid


def job_stop(accessToken, jobUuid):
    url = "https://api.yingdao.com/oapi/dispatch/v2/job/stop"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "jobUuid": jobUuid
    })
    re_data = callApi(url, data, headers, method[1])
    return re_data


def query(accessToken, jobUuid):
    """
    查询应用启动结果
    :return:
    """
    data = json.dumps({
        "jobUuid": jobUuid,
    })
    headers = {'Content-Type': 'application/json', 'authorization': 'Bearer {}'.format(accessToken)}
    return callApi(
        urls['query'],
        data,
        headers,
        method[1])['data']['status']


# 调用的接口网址
urls = {
    'getAccessToken': 'https://api.yingdao.com/oapi/token/v2/token/create?accessKeyId={}&accessKeySecret={}',
    'startJob': 'https://api.yingdao.com/oapi/dispatch/v2/job/start',
    'query': 'https://api.yingdao.com/oapi/dispatch/v2/job/query'
}

# todo -------------------------改变调度相关信息和应用入参即可------------------------------------------
# 调度相关信息
informationOfDispatch = {
    'accessKeyId': 'SNf63XdyraPDxUZc@platform',
    'accessKeySecret': 'fmd91tTMSp5Y4RNkC2yuEcW0r8vVqAzn',
    "accountName": "admin@fckjgz",
    "robotUuid": "13842197-a729-46a8-973e-abef125e837c",
    'comment': '伯符的调度相关信息',
}

# 应用入参
informationOfrobot = [
    {"name": "parameter1",
     "value": '啊杰连锁火锅店',
     "type": "str"
     },
    {"name": "parameter2",
     "value": '直播卖拖鞋',
     "type": "str"
     }]


class exe:

    def __init__(self):

        self.accessToken = None
        self.jobUuid = None
        self.appliction_list = None

        # 主程序
        self.window = QMainWindow()
        self.window.resize(500, 600)
        self.window.move(300, 300)
        self.window.setWindowTitle('影刀调度神器')
        # self.window.setFixedSize(500, 600)
        # 将窗口移动到屏幕中央
        self.center_window()

    def center_window(self):
        # 获取屏幕大小
        screen = QDesktopWidget().screenGeometry()
        # 计算窗口居中时的左上角坐标
        x = int((screen.width() - self.window.width()) / 2)
        y = int((screen.height() - self.window.height()) / 2)
        # 移动窗口
        self.window.move(x, y)
        # 文字：影刀账号
        self.account = QLabel(self.window)
        self.account.setGeometry(QtCore.QRect(40, 40, 100, 41))
        self.account.setText('机器人账号:')
        # id
        self.id = QLabel(self.window)
        self.id.setGeometry(QtCore.QRect(40, 90, 100, 41))
        self.id.setText('access id:')
        # secret
        self.access_secret = QLabel(self.window)
        self.access_secret.setGeometry(QtCore.QRect(40, 140, 130, 41))
        self.access_secret.setText('access_secret:')
        # 选择应用
        self.id1 = QLabel(self.window)
        self.id1.setGeometry(QtCore.QRect(40, 190, 100, 41))
        self.id1.setText('选择应用:')
        # 框
        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText("例如xxx@xxx")
        self.textEdit.setGeometry(QtCore.QRect(180, 40, 260, 35))
        self.textEdit2 = QPlainTextEdit(self.window)
        self.textEdit2.setPlaceholderText("在控制台获取")
        self.textEdit2.setGeometry(QtCore.QRect(180, 90, 260, 35))
        self.textEdit3 = QPlainTextEdit(self.window)
        self.textEdit3.setPlaceholderText("在控制台获取")
        self.textEdit3.setGeometry(QtCore.QRect(180, 140, 260, 35))
        self.xz = QComboBox(self.window)
        self.xz.setPlaceholderText("请选择")
        self.xz.setGeometry(QtCore.QRect(180, 190, 260, 35))
        # 停止应用、启动应用、重试应用
        self.button_stop = QPushButton('停止应用', self.window)
        self.button_stop.move(40, 260)
        self.button_stop.clicked.connect(self.stop)
        self.button_start = QPushButton('启动应用', self.window)
        self.button_start.move(150, 260)
        # self.button_retry = QPushButton('重试应用', self.window)
        # self.button_retry.move(260, 260)
        self.button_flesh = QPushButton('刷新应用', self.window)
        # self.button_flesh.move(370, 260)
        self.button_flesh.move(260, 260)
        self.button_flesh.clicked.connect(self.flesh)
        # 运行状态
        self.account1 = QLabel(self.window)
        self.account1.setGeometry(QtCore.QRect(40, 320, 100, 41))
        self.account1.setText('运行状态:')
        self.state = QTextBrowser(self.window)
        self.state.setPlaceholderText("接口返回数据")
        self.state.setGeometry(QtCore.QRect(40, 370, 400, 200))
        # 创建定时器对象
        self.timer = QtCore.QTimer()
        # 将定时器的timeout信号连接到self.button_start方法
        self.timer.timeout.connect(self.button_start_handler)
        # 将按钮的clicked信号连接到self.start方法
        self.button_start.clicked.connect(self.start)
        # 设置主窗口的布局
        layout = QVBoxLayout()
        self.window.setLayout(layout)
        # 添加标签和按钮到水平布局中
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.account)
        hlayout.addWidget(self.id)
        hlayout.addWidget(self.access_secret)
        hlayout.addWidget(self.id1)
        hlayout.addWidget(self.textEdit)
        hlayout.addWidget(self.textEdit2)
        hlayout.addWidget(self.textEdit3)
        hlayout.addWidget(self.xz)
        hlayout.addWidget(self.button_start)
        hlayout.addWidget(self.button_flesh)
        hlayout.addWidget(self.button_stop)
        hlayout.addWidget(self.account1)
        hlayout.addWidget(self.state)

        # 将水平布局添加到垂直布局中
        layout.addLayout(hlayout)

    def start(self):
        # 启动定时器
        self.timer.start(2000)

    def button_start_handler(self):
        # 定时器的timeout信号处理函数
        self.accessToken = getAccessToken()
        self.jobUuid = startJob(self.accessToken)
        response = query(self.accessToken, self.jobUuid)
        print("状态：" + response)
        if response == 'error':
            print('应用运行异常！请检查入参或者指令！')
            self.state.append('应用运行异常！请检查入参或者指令！')
            self.state.ensureCursorVisible()
        elif response == 'finish':
            print('应用运行完成，调度结束！')
            self.state.append('应用运行完成，调度结束！')
            self.state.ensureCursorVisible()
            # 停止定时器
            self.timer.stop()
        else:
            print('应用还在运行中.......')
            self.state.append('应用还在运行中.......')
            self.state.ensureCursorVisible()

    def flesh(self):
        self.accessToken = getAccessToken()
        appliction_list = query_application(self.accessToken)['应用列表']
        self.xz.addItems(appliction_list)

    def stop(self):
        self.timer.stop()
        print(self.accessToken)
        print(self.jobUuid)
        data = job_stop(self.accessToken, self.jobUuid)['success']
        print(data, type(str(data)))
        if data == True:
            self.state.append('应用已停止运行！')
            self.state.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication([])
    file_tidy = exe()
    # apply_stylesheet(app, theme='dark_blue.xml')
    file_tidy.window.show()

    app.exec_()
