# -*- coding: utf-8 -*-

import sys
import main_preprocess, main_train, main_test
from PySide6.QtCore import QThread, Signal


class PreprocessThread(QThread):
    run_signal = Signal(str, str) # msg, color
    finished_signal = Signal()

    def __init__(self, args):
        super(PreprocessThread, self).__init__()
        self.args = args

    def run(self):
        self.args.filename = '../' + self.args.filename
        self.args.dataset = '../' + self.args.dataset

        sys.stdout.write = self.write

        try:
            print('*'*5, 'Start preprocess', '*'*5)
            main_preprocess.preprocess(self.args)
            print('*'*5, 'Done preprocess', '*'*5)
        except Exception as e:
            self.write(str(e)+"\n", color="red")
            print('*'*5, 'Fail preprocess', '*'*5)

        
        sys.stdout.write = sys.__stdout__ # redirection 복원

        self.finished_signal.emit()

    def write(self, text, color="black"):
        sys.stdout.flush()
        sys.stderr.flush()
        self.run_signal.emit(text, color)


class TrainThread(QThread):
    run_signal = Signal(str, str) # msg, color
    finished_signal = Signal()

    def __init__(self, args):
        super(TrainThread, self).__init__()
        self.args = args

    def run(self):
        self.args.dataset = '../' + self.args.dataset

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

    def __init__(self, args):
        super(TestThread, self).__init__()
        self.args = args

    def run(self):
        self.args.dataset = '../' + self.args.dataset

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