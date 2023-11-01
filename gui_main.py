# -*- coding: utf-8 -*-

import sys
import json

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator, QIntValidator

from mainwindow_ui import Ui_MainWindow
from gui_threads import PreprocessThread, TrainThread, TestThread

import argparse

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, args_path, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        ### Args part ###
        self.setupUi(self) # qt designer로 만든 UI 적용
        self.set_validator() # 각 parameter 입력 값 type에 관한 validation 설정
        self.args = self.read_arguments(args_path) # 저장된 argument 값을 불러온다.
        self.set_args_edit() # 불러온 값을 UI에 적용시킨다.

        ### Log part ###
        self.scroll_bottom = True
        self.pushButton_clear_log.clicked.connect(self.click_clear_log) 
        # Clear log 버튼 클릭 시 brwoser 내용 다 지움.
        self.textBrowser_log.verticalScrollBar().valueChanged.connect(self.on_scrollbar_value_changed)

        ### Preprocess Tab ###
        self.preprocess_pushButton_save_arg.clicked.connect(self.click_save_arg)
        self.preprocess_pushButton_run.clicked.connect(self.click_preprocess_run)
        self.preprocess_thraed = PreprocessThread(self.args['preprocess'])
        self.preprocess_thraed.run_signal.connect(self.update_run_log)
        self.preprocess_thraed.finished_signal.connect(self.enable_preprocess_run_button)

        ### Train Tab ###
        self.train_pushButton_save_arg.clicked.connect(self.click_save_arg)
        self.train_pushButton_run.clicked.connect(self.click_train_run)
        self.train_thread = TrainThread(self.args['train'])
        self.train_thread.run_signal.connect(self.update_run_log)
        self.train_thread.finished_signal.connect(self.enable_train_run_button)

        ### Test Tab ###
        self.test_pushButton_save_arg.clicked.connect(self.click_save_arg)
        self.test_pushButton_run.clicked.connect(self.click_test_run)
        self.test_thread = TestThread(self.args['test'])
        self.test_thread.run_signal.connect(self.update_run_log)
        self.test_thread.finished_signal.connect(self.enable_test_run_button)

    ### Preprocess function ####
    def click_preprocess_run(self):
        self.preprocess_pushButton_run.setEnabled(False)
        self.update_preprocess_args()
        self.preprocess_thraed.args = self.args['preprocess']
        self.preprocess_thraed.start()

    def enable_preprocess_run_button(self):
        self.preprocess_pushButton_run.setEnabled(True)
    
    def update_preprocess_args(self):
        # save argument와 run을 눌렀을 때, 먼저 args 값들을 update해준다.
        self.args['preprocess'].filename = self.preprocess_lineEdit_filename.text()
        self.args['preprocess'].outlier_detector = self.preprocess_comboBox_outlier_detector.currentText()
        self.args['preprocess'].outlier_detector_param = float(self.preprocess_lineEdit_outlier_detector_param.text())
        self.args['preprocess'].train_size = float(self.preprocess_lineEdit_train_size.text())
        self.args['preprocess'].num_splits = int(self.preprocess_lineEdit_num_splits.text())
    ############################

    ### Train function ###
    def click_train_run(self):
        self.train_pushButton_run.setEnabled(False)
        self.update_train_args()
        self.train_thread.args = self.args['train']
        self.train_thread.start()

    def enable_train_run_button(self):
        self.train_pushButton_run.setEnabled(True)

    def update_train_args(self):
        if self.train_checkbox_quiet.isChecked(): self.args['train'].quiet = True
        else: self.args['train'].quiet = False
        self.args['train'].cuda = int(self.train_lineEdit_cuda.text())
        self.args['train'].dataset = self.train_lineEdit_dataset.text()
        self.args['train'].split_id = int(self.train_lineEdit_split_id.text())
        self.args['train'].train_size = float(self.train_lineEdit_train_size.text())
        self.args['train'].batch_size = int(self.train_lineEdit_batch_size.text())
        self.args['train'].model = self.train_comboBox_model.currentText()
        self.args['train'].num_hidden_layers = int(self.train_lineEdit_num_hidden_layers.text())
        self.args['train'].hidden_size = int(self.train_lineEdit_hidden_size.text())
        self.args['train'].dropout = float(self.train_lineEdit_dropout.text())
        self.args['train'].learning_rate = float(self.train_lineEdit_learning_rate.text())
        self.args['train'].weight_decay = float(self.train_lineEdit_weight_decay.text())
        self.args['train'].num_epochs = int(self.train_lineEdit_num_epochs.text())
    ######################

    ### Test function ###
    def click_test_run(self):
        self.test_pushButton_run.setEnabled(False)
        self.update_test_args()
        self.test_thread.args = self.args['test']
        self.test_thread.start()

    def enable_test_run_button(self):
        self.test_pushButton_run.setEnabled(True)

    def update_test_args(self):
        self.args['test'].cuda = int(self.test_lineEdit_cuda.text())
        self.args['test'].dataset = self.test_lineEdit_dataset.text()
        self.args['test'].split_id = int(self.test_lineEdit_split_id.text())
        self.args['test'].model = self.test_comboBox_model.currentText()
    #####################

    
    ### Log part ###
    def on_scrollbar_value_changed(self, value):
        # 스크롤바가 항상 제일 아래에 가 있도록 되는데, 잠깐 위를 보기 위해 스크롤을 움직이면 제일 아래에 가도록하는 게 멈춘다.
        # 그리고 다시 스크롤바를 제일 아래로 내리면, 계속 해서 제일 아래에 가 있도록 만든다.
        if value == self.textBrowser_log.verticalScrollBar().maximum(): self.scroll_bottom = True
        else: self.scroll_bottom = False

    def update_run_log(self, text, color):
        self.textBrowser_log.setTextColor(color)
        self.textBrowser_log.insertPlainText(text)
        if self.scroll_bottom is True: # 스크롤바가 항상 제일 아래에 가 있도록 한다.
            self.textBrowser_log.verticalScrollBar().setValue(self.textBrowser_log.verticalScrollBar().maximum())
    
    def click_clear_log(self):
        self.textBrowser_log.clear()
    ################

    ### Args part ###
    def click_save_arg(self):
        # 전처리에 사용한 인자들을 저장한다.

        # 저장하기 전, lineEdit에 적혀 있는 값으로 arg 값을 update 한다.
        self.update_preprocess_args()
        self.update_train_args()
        self.update_test_args()
        args = {
            'preprocess': vars(self.args['preprocess']),
            'train': vars(self.args['train']),
            'test': vars(self.args['test']),
        }
        with open(f'../saved_args.json', 'w') as f:
            json.dump(args, f, indent=4)

    def set_args_edit(self):
        # 저장된 args의 값을 바탕으로 초기 preprocess의 args 값을 설정한다.

        # preprocess
        self.preprocess_lineEdit_filename.setText(str(self.args['preprocess'].filename))
        self.preprocess_comboBox_outlier_detector.setCurrentText(str(self.args['preprocess'].outlier_detector))
        self.preprocess_lineEdit_outlier_detector_param.setText(str(self.args['preprocess'].outlier_detector_param))
        self.preprocess_lineEdit_train_size.setText(str(self.args['preprocess'].train_size))
        self.preprocess_lineEdit_num_splits.setText(str(self.args['preprocess'].num_splits))

        # train
        if self.args['train'].quiet == 'True': self.train_checkbox_quiet.setCheckState(Qt.Checked)
        self.train_lineEdit_cuda.setText(str(self.args['train'].cuda))
        self.train_lineEdit_dataset.setText(str(self.args['train'].dataset))
        self.train_lineEdit_split_id.setText(str(self.args['train'].split_id))
        self.train_lineEdit_train_size.setText(str(self.args['train'].train_size))
        self.train_lineEdit_batch_size.setText(str(self.args['train'].batch_size))
        self.train_comboBox_model.setCurrentText(str(self.args['train'].model))
        self.train_lineEdit_num_hidden_layers.setText(str(self.args['train'].num_hidden_layers))
        self.train_lineEdit_hidden_size.setText(str(self.args['train'].hidden_size))
        self.train_lineEdit_dropout.setText(str(self.args['train'].dropout))
        self.train_lineEdit_learning_rate.setText(str(self.args['train'].learning_rate))
        self.train_lineEdit_weight_decay.setText(str(self.args['train'].weight_decay))
        self.train_lineEdit_num_epochs.setText(str(self.args['train'].num_epochs))

        # test
        self.test_lineEdit_cuda.setText(str(self.args['test'].cuda))
        self.test_lineEdit_dataset.setText(str(self.args['test'].dataset))
        self.test_lineEdit_split_id.setText(str(self.args['test'].split_id))
        self.test_comboBox_model.setCurrentText(str(self.args['test'].model))

    def read_arguments(self, args_path):
        # args.json에 저장된 args 값들을 불러 온다.
        with open(args_path, 'r') as f:
            saved_args = json.load(f)

        args = {
            'preprocess': argparse.ArgumentParser(),
            'train': argparse.ArgumentParser(),
            'test': argparse.ArgumentParser(),
        }

        for key, item in saved_args['preprocess'].items():
            args['preprocess'].add_argument(f'--{key}', type=str, default=item)

        for key, item in saved_args['train'].items():
            args['train'].add_argument(f'--{key}', type=str, default=item)

        for key, item in saved_args['test'].items():
            args['test'].add_argument(f'--{key}', type=str, default=item)

        args['preprocess'] = args['preprocess'].parse_args()
        args['train'] = args['train'].parse_args()
        args['test'] = args['test'].parse_args()
        
        return args
    
    def set_validator(self):
        # UI에 입력한 값이 유효하도록 만든다.
        double_validator = QDoubleValidator()
        int_validator = QIntValidator()

        self.preprocess_lineEdit_outlier_detector_param.setValidator(double_validator)
        self.preprocess_lineEdit_train_size.setValidator(double_validator)
        self.preprocess_lineEdit_num_splits.setValidator(int_validator)

        self.train_lineEdit_cuda.setValidator(int_validator)
        self.train_lineEdit_split_id.setValidator(int_validator)
        self.train_lineEdit_train_size.setValidator(double_validator)
        self.train_lineEdit_batch_size.setValidator(int_validator)
        self.train_lineEdit_num_hidden_layers.setValidator(int_validator)
        self.train_lineEdit_hidden_size.setValidator(int_validator)
        self.train_lineEdit_dropout.setValidator(double_validator)
        self.train_lineEdit_learning_rate.setValidator(double_validator)
        self.train_lineEdit_weight_decay.setValidator(double_validator)
        self.train_lineEdit_num_epochs.setValidator(int_validator)

        self.test_lineEdit_cuda.setValidator(int_validator)
        self.test_lineEdit_split_id.setValidator(int_validator)
    #################

def main():
    import os
    app = QApplication()
    file_path_args = '../saved_args.json'
    window = MainWindow(args_path=file_path_args)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()