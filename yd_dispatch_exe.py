# -*-coding:utf-8-*-

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox, QLabel
from PySide2 import QtCore
import time
import os
import shutil
import glob


class exe:

    def __init__(self):

        # 主程序
        self.window = QMainWindow()
        self.window.resize(500, 600)
        self.window.move(300, 300)
        self.window.setWindowTitle('影刀调度神器')
        self.window.setFixedSize(500, 600)

        # 影刀账号
        self.account = QLabel(self.window)
        self.account.setGeometry(QtCore.QRect(40, 40, 100, 41))
        self.account.setText('影刀账号:')

        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText("例如xxx@xxx")
        self.textEdit.setGeometry(QtCore.QRect(170, 40, 170, 35))

        # id
        self.id = QLabel(self.window)
        self.id.setGeometry(QtCore.QRect(40, 90, 100, 41))
        self.id.setText('access id:')

        self.textEdit2 = QPlainTextEdit(self.window)
        self.textEdit2.setPlaceholderText("在控制台获取")
        self.textEdit2.setGeometry(QtCore.QRect(170, 90, 170, 35))

        # secret
        self.id = QLabel(self.window)
        self.id.setGeometry(QtCore.QRect(40, 140, 100, 41))
        self.id.setText('access secret:')

        self.textEdit2 = QPlainTextEdit(self.window)
        self.textEdit2.setPlaceholderText("在控制台获取")
        self.textEdit2.setGeometry(QtCore.QRect(170, 140, 170, 35))

        # 选择应用
        self.id = QLabel(self.window)
        self.id.setGeometry(QtCore.QRect(40, 190, 100, 41))
        self.id.setText('选择应用:')

        self.textEdit2 = QPlainTextEdit(self.window)
        self.textEdit2.setPlaceholderText("自动获取，请选择")
        self.textEdit2.setGeometry(QtCore.QRect(170, 190, 170, 35))

        # 停止应用、启动应用、重试应用
        self.button = QPushButton('停止应用', self.window)
        self.button.move(40, 260)

        self.button.clicked.connect(self.dispatch)

        self.button = QPushButton('启动应用', self.window)
        self.button.move(150, 260)

        self.button.clicked.connect(self.dispatch)
        self.button = QPushButton('重试应用', self.window)
        self.button.move(260, 260)

        self.button.clicked.connect(self.dispatch)

        # 运行状态
        self.account = QLabel(self.window)
        self.account.setGeometry(QtCore.QRect(40, 320, 100, 41))
        self.account.setText('运行状态:')

        self.state = QPlainTextEdit(self.window)
        self.state.setPlaceholderText("接口返回数据")
        self.state.setGeometry(QtCore.QRect(40, 370, 400, 200))

    def dispatch(self):
        info = self.textEdit.toPlainText()
        mkdir_path = os.path.join(info, '文件分类')

        start_time = time.time()

        if not os.path.exists(mkdir_path):
            os.mkdir(mkdir_path)

        file_num = 0
        dir_num = 0

        for file in glob.glob(f'{info}\*'):
            print(file)
            if os.path.isfile(file):
                filename = os.path.basename(file)
                if '.' in filename:
                    suffix = filename.split('.')[-1]
                else:
                    suffix = 'others'
                if not os.path.exists(f'{mkdir_path}/{suffix}'):
                    os.mkdir(f'{mkdir_path}/{suffix}')
                    dir_num += 1
                shutil.copy(file, f'{mkdir_path}/{suffix}')
                os.remove(file)
                file_num += 1

        end_time = time.time()
        duaration_time = end_time - start_time

        if dir_num == 0:
            QMessageBox.about(self.window,
                              '整理结果',
                              f'''无需整理，闲的没事？'''
                              )

        else:
            QMessageBox.about(self.window,
                              '整理结果',
                              f'哔哩哔哩噼里啪啦，整理完成啦！\n'
                              f'共有{file_num}个文件分类到了{dir_num}个文件夹中\n'
                              f'整理时间为{duaration_time}秒'
                              )


if __name__ == "__main__":
    app = QApplication([])
    file_tidy = exe()
    file_tidy.window.show()
    app.exec_()
