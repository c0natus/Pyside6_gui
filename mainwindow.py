# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowKtVqJB.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(847, 520)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 821, 501))
        self.preprocess = QWidget()
        self.preprocess.setObjectName(u"preprocess")
        self.preprocess.setEnabled(True)
        self.preprocess.setLayoutDirection(Qt.LeftToRight)
        self.label_start_column_output = QLabel(self.preprocess)
        self.label_start_column_output.setObjectName(u"label_start_column_output")
        self.label_start_column_output.setGeometry(QRect(40, 180, 151, 21))
        self.label_sheet_output = QLabel(self.preprocess)
        self.label_sheet_output.setObjectName(u"label_sheet_output")
        self.label_sheet_output.setGeometry(QRect(40, 100, 151, 21))
        self.label_start_column_input = QLabel(self.preprocess)
        self.label_start_column_input.setObjectName(u"label_start_column_input")
        self.label_start_column_input.setGeometry(QRect(40, 140, 151, 21))
        self.label_filename = QLabel(self.preprocess)
        self.label_filename.setObjectName(u"label_filename")
        self.label_filename.setGeometry(QRect(40, 20, 151, 21))
        self.label_sheet_input = QLabel(self.preprocess)
        self.label_sheet_input.setObjectName(u"label_sheet_input")
        self.label_sheet_input.setGeometry(QRect(40, 60, 151, 21))
        self.pushButton_save_arg = QPushButton(self.preprocess)
        self.pushButton_save_arg.setObjectName(u"pushButton_save_arg")
        self.pushButton_save_arg.setGeometry(QRect(320, 430, 101, 24))
        self.lineEdit_filename = QLineEdit(self.preprocess)
        self.lineEdit_filename.setObjectName(u"lineEdit_filename")
        self.lineEdit_filename.setGeometry(QRect(210, 20, 113, 21))
        self.lineEdit_sheet_input = QLineEdit(self.preprocess)
        self.lineEdit_sheet_input.setObjectName(u"lineEdit_sheet_input")
        self.lineEdit_sheet_input.setGeometry(QRect(210, 60, 113, 21))
        self.lineEdit_sheet_output = QLineEdit(self.preprocess)
        self.lineEdit_sheet_output.setObjectName(u"lineEdit_sheet_output")
        self.lineEdit_sheet_output.setGeometry(QRect(210, 100, 113, 21))
        self.lineEdit_start_column_input = QLineEdit(self.preprocess)
        self.lineEdit_start_column_input.setObjectName(u"lineEdit_start_column_input")
        self.lineEdit_start_column_input.setGeometry(QRect(210, 140, 113, 21))
        self.lineEdit_start_column_output = QLineEdit(self.preprocess)
        self.lineEdit_start_column_output.setObjectName(u"lineEdit_start_column_output")
        self.lineEdit_start_column_output.setGeometry(QRect(210, 180, 113, 21))
        self.pushButton_browse_file = QPushButton(self.preprocess)
        self.pushButton_browse_file.setObjectName(u"pushButton_browse_file")
        self.pushButton_browse_file.setGeometry(QRect(340, 20, 81, 24))
        self.pushButton_browse_file.setAutoRepeatDelay(301)
        self.textBrowser_results = QTextBrowser(self.preprocess)
        self.textBrowser_results.setObjectName(u"textBrowser_results")
        self.textBrowser_results.setGeometry(QRect(460, 20, 331, 371))
        self.pushButton_run = QPushButton(self.preprocess)
        self.pushButton_run.setObjectName(u"pushButton_run")
        self.pushButton_run.setGeometry(QRect(690, 430, 101, 24))
        self.lineEdit_outlier_detector = QLineEdit(self.preprocess)
        self.lineEdit_outlier_detector.setObjectName(u"lineEdit_outlier_detector")
        self.lineEdit_outlier_detector.setGeometry(QRect(210, 220, 113, 21))
        self.label_outlier_detector = QLabel(self.preprocess)
        self.label_outlier_detector.setObjectName(u"label_outlier_detector")
        self.label_outlier_detector.setGeometry(QRect(40, 220, 151, 21))
        self.lineEdit_outlier_detector_param = QLineEdit(self.preprocess)
        self.lineEdit_outlier_detector_param.setObjectName(u"lineEdit_outlier_detector_param")
        self.lineEdit_outlier_detector_param.setGeometry(QRect(210, 260, 113, 21))
        self.label_outlier_detector_param = QLabel(self.preprocess)
        self.label_outlier_detector_param.setObjectName(u"label_outlier_detector_param")
        self.label_outlier_detector_param.setGeometry(QRect(40, 260, 151, 21))
        self.lineEdit_train_size = QLineEdit(self.preprocess)
        self.lineEdit_train_size.setObjectName(u"lineEdit_train_size")
        self.lineEdit_train_size.setGeometry(QRect(210, 300, 113, 21))
        self.label_train_size = QLabel(self.preprocess)
        self.label_train_size.setObjectName(u"label_train_size")
        self.label_train_size.setGeometry(QRect(40, 300, 151, 21))
        self.label_num_splits = QLabel(self.preprocess)
        self.label_num_splits.setObjectName(u"label_num_splits")
        self.label_num_splits.setGeometry(QRect(40, 340, 151, 21))
        self.lineEdit_num_splits = QLineEdit(self.preprocess)
        self.lineEdit_num_splits.setObjectName(u"lineEdit_num_splits")
        self.lineEdit_num_splits.setGeometry(QRect(210, 340, 113, 21))
        self.label_dataset = QLabel(self.preprocess)
        self.label_dataset.setObjectName(u"label_dataset")
        self.label_dataset.setGeometry(QRect(40, 380, 151, 21))
        self.lineEdit_dataset = QLineEdit(self.preprocess)
        self.lineEdit_dataset.setObjectName(u"lineEdit_dataset")
        self.lineEdit_dataset.setGeometry(QRect(210, 380, 113, 21))
        self.tabWidget.addTab(self.preprocess, "")
        self.menu2 = QWidget()
        self.menu2.setObjectName(u"menu2")
        self.tabWidget.addTab(self.menu2, "")
        self.menu3 = QWidget()
        self.menu3.setObjectName(u"menu3")
        self.tabWidget.addTab(self.menu3, "")
        self.menu4 = QWidget()
        self.menu4.setObjectName(u"menu4")
        self.tabWidget.addTab(self.menu4, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_start_column_output.setText(QCoreApplication.translate("MainWindow", u"start_column_output", None))
        self.label_sheet_output.setText(QCoreApplication.translate("MainWindow", u"sheet_output", None))
        self.label_start_column_input.setText(QCoreApplication.translate("MainWindow", u"start_column_input", None))
        self.label_filename.setText(QCoreApplication.translate("MainWindow", u"Filename", None))
        self.label_sheet_input.setText(QCoreApplication.translate("MainWindow", u"sheet_input", None))
        self.pushButton_save_arg.setText(QCoreApplication.translate("MainWindow", u"Save arguments", None))
        self.pushButton_browse_file.setText(QCoreApplication.translate("MainWindow", u"Browse file", None))
        self.pushButton_run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_outlier_detector.setText(QCoreApplication.translate("MainWindow", u"outlier_detector", None))
        self.label_outlier_detector_param.setText(QCoreApplication.translate("MainWindow", u"outlier_detector_param", None))
        self.label_train_size.setText(QCoreApplication.translate("MainWindow", u"train_size", None))
        self.label_num_splits.setText(QCoreApplication.translate("MainWindow", u"num_splits", None))
        self.label_dataset.setText(QCoreApplication.translate("MainWindow", u"dataset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.preprocess), QCoreApplication.translate("MainWindow", u"Preprocess", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.menu2), QCoreApplication.translate("MainWindow", u"Menu2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.menu3), QCoreApplication.translate("MainWindow", u"Menu3", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.menu4), QCoreApplication.translate("MainWindow", u"Menu4", None))
    # retranslateUi

