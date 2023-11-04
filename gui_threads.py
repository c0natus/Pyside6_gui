# -*- coding: utf-8 -*-

import os
import sys
import main_preprocess, main_train, main_test
from PySide6.QtCore import QThread, Signal


class PreprocessThread(QThread):
    run_signal = Signal(str, str) # msg, color 값을 signal과 함께 보낸다.
    finished_signal = Signal()

    def __init__(self, args, cur_path):
        super(PreprocessThread, self).__init__()
        self.args = args
        self.cur_path = cur_path

    def run(self):
        self.args.filename = os.path.join(self.cur_path, self.args.filename)        
        self.args.dataset = os.path.join(self.cur_path, self.args.dataset)

        sys.stdout.write = self.write # standard output을 self.write로 redirect한다.

        try: # Preprocess를 실행한다.
            print('*'*5, 'Start preprocess', '*'*5)
            main_preprocess.preprocess(self.args)
            print('*'*5, 'Done preprocess', '*'*5)
        except Exception as e: # error가 났을 때.
            self.write(str(e)+"\n", color="red")
            print('*'*5, 'Fail preprocess', '*'*5)

        
        sys.stdout.write = sys.__stdout__ # redirection 복원

        self.finished_signal.emit() # 종료되었다는 signal을 보낸다.

    def write(self, text, color="black"):
        sys.stdout.flush()
        sys.stderr.flush()
        self.run_signal.emit(text, color)


class TrainThread(QThread):
    run_signal = Signal(str, str) # msg, color
    finished_signal = Signal()

    def __init__(self, args, cur_path):
        super(TrainThread, self).__init__()
        self.args = args
        self.cur_path = cur_path

    def run(self):
        self.args.dataset = os.path.join(self.cur_path, self.args.dataset)

        sys.stdout.write = self.write

        try:
            print('*'*5, 'Start train', '*'*5)
            main_train.train(self.args)
            print('*'*5, 'Done train', '*'*5)
        except Exception as e:
            self.write(str(e)+"\n", color="red")
            print('*'*5, 'Fail train', '*'*5)
        
        sys.stdout.write = sys.__stdout__ # redirection 복원

        self.finished_signal.emit()

    def write(self, text, color="black"):
        sys.stdout.flush()
        sys.stderr.flush()
        self.run_signal.emit(text, color)


class TestThread(QThread):
    run_signal = Signal(str, str) # msg, color
    finished_signal = Signal()

    def __init__(self, args, cur_path):
        super(TestThread, self).__init__()
        self.args = args
        self.cur_path = cur_path

    def run(self):
        self.args.dataset = os.path.join(self.cur_path, self.args.dataset)

        sys.stdout.write = self.write

        try:
            print('*'*5, 'Start test', '*'*5)
            main_test.test(self.args)
            print('*'*5, 'Done test', '*'*5)
        except Exception as e:
            self.write(str(e)+"\n", color="red")
            print('*'*5, 'Fail test', '*'*5)
        
        sys.stdout.write = sys.__stdout__ # redirection 복원

        self.finished_signal.emit()

    def write(self, text, color="black"):
        sys.stdout.flush()
        sys.stderr.flush()
        self.run_signal.emit(text, color)