# -*- coding: utf-8 -*-

import os
import sys
import json

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QDoubleValidator, QIntValidator

from mainwindow import Ui_MainWindow
from preprocess import PreprocessThread


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, args_path, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self) # qt designer로 만든 UI 적용
        self.set_validator()

        self.args = self.read_arguments(args_path)
        self.set_args_edit()

        self.pushButton_save_arg.clicked.connect(self.click_save_arg)

        self.pushButton_browse_file.clicked.connect(self.click_browse_file)

        self.pushButton_run.clicked.connect(self.click_run)
        self.preprocess_thraed = PreprocessThread(self.args)
        self.preprocess_thraed.progress_signal.connect(self.update_run_log)
        self.preprocess_thraed.finished_signal.connect(self.enable_run_button)
    
    def click_save_arg(self):
        # 전처리에 사용한 인자들을 저장한다.
        self.update_args()
        with open(f'args.json', 'w') as f:
            json.dump(self.args, f)

    def click_browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 불러오기", "", "모든 파일 (*)", options=options)
        
        if file_path:
            self.args['dataset_path'] = file_path
            file_name = file_path.split('/')[-1]
            extention_index = file_name.rfind('.')
            file_name_without_extention = file_name[:extention_index]
            self.lineEdit_filename.setText(f"{file_name_without_extention}")

    def click_run(self):
        self.textBrowser_results.clear()
        self.pushButton_run.setEnabled(False)
        self.update_args()
        self.preprocess_thraed.args = self.args
        self.preprocess_thraed.start()

    def update_run_log(self, msg):
        self.textBrowser_results.append(msg)

    def enable_run_button(self):
        self.pushButton_run.setEnabled(True)
    
    def set_args_edit(self):
        self.lineEdit_filename.setText(str(self.args['filename']))
        self.lineEdit_sheet_input.setText(str(self.args['sheet_input']))
        self.lineEdit_sheet_output.setText(str(self.args['sheet_output']))
        self.lineEdit_start_column_input.setText(str(self.args['start_column_input']))
        self.lineEdit_start_column_output.setText(str(self.args['start_column_output']))
        self.lineEdit_outlier_detector.setText(str(self.args['outlier_detector']))
        self.lineEdit_outlier_detector_param.setText(str(self.args['outlier_detector_param']))
        self.lineEdit_train_size.setText(str(self.args['train_size']))
        self.lineEdit_num_splits.setText(str(self.args['num_splits']))
        self.lineEdit_dataset.setText(str(self.args['dataset']))
    
    def update_args(self):
        self.args['filename'] = self.lineEdit_filename.text()
        self.args['sheet_input'] = self.lineEdit_sheet_input.text()
        self.args['sheet_output'] = self.lineEdit_sheet_output.text()
        self.args['start_column_input'] = self.lineEdit_start_column_input.text()
        self.args['start_column_output'] = self.lineEdit_start_column_output.text()
        self.args['outlier_detector'] = self.lineEdit_outlier_detector.text()
        self.args['outlier_detector_param'] = float(self.lineEdit_outlier_detector_param.text())
        self.args['train_size'] = float(self.lineEdit_train_size.text())
        self.args['num_splits'] = int(self.lineEdit_num_splits.text())
        self.args['dataset'] = self.lineEdit_dataset.text()

    def read_arguments(self, args_path):
        with open(args_path, 'r') as f:
            args = json.load(f)
        return args
    
    def set_validator(self):
        double_validator = QDoubleValidator()
        int_validator = QIntValidator()

        self.lineEdit_outlier_detector_param.setValidator(double_validator)
        self.lineEdit_train_size.setValidator(double_validator)
        self.lineEdit_num_splits.setValidator(int_validator)


def main():
    app = QApplication()
    file_path_args = 'args.json'
    window = MainWindow(args_path=file_path_args)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()