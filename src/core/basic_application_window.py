# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basic_application_window.ui'
#
# Created: Thu Mar 31 19:20:01 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from external_modules.matplotlibwidget import MatplotlibWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1144, 718)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.list_records = QtGui.QListView(self.centralwidget)
        self.list_records.setGeometry(QtCore.QRect(740, 220, 391, 141))
        self.list_records.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.list_records.setModelColumn(0)
        self.list_records.setObjectName(_fromUtf8("list_records"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(740, 370, 391, 25))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.txt_tag = QtGui.QLineEdit(self.layoutWidget)
        self.txt_tag.setObjectName(_fromUtf8("txt_tag"))
        self.horizontalLayout_2.addWidget(self.txt_tag)
        self.btn_clear_record = QtGui.QPushButton(self.layoutWidget)
        self.btn_clear_record.setObjectName(_fromUtf8("btn_clear_record"))
        self.horizontalLayout_2.addWidget(self.btn_clear_record)
        self.btn_save_record_to_disk = QtGui.QPushButton(self.layoutWidget)
        self.btn_save_record_to_disk.setObjectName(_fromUtf8("btn_save_record_to_disk"))
        self.horizontalLayout_2.addWidget(self.btn_save_record_to_disk)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 200, 721, 471))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_scripts = QtGui.QWidget()
        self.tab_scripts.setObjectName(_fromUtf8("tab_scripts"))
        self.tree_scripts = QtGui.QTreeWidget(self.tab_scripts)
        self.tree_scripts.setEnabled(True)
        self.tree_scripts.setGeometry(QtCore.QRect(0, 30, 711, 311))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_scripts.sizePolicy().hasHeightForWidth())
        self.tree_scripts.setSizePolicy(sizePolicy)
        self.tree_scripts.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.tree_scripts.setHeaderHidden(False)
        self.tree_scripts.setObjectName(_fromUtf8("tree_scripts"))
        self.tree_scripts.header().setDefaultSectionSize(150)
        self.tree_scripts.header().setHighlightSections(True)
        self.progressBar = QtGui.QProgressBar(self.tab_scripts)
        self.progressBar.setGeometry(QtCore.QRect(230, 420, 471, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.btn_stop_script = QtGui.QPushButton(self.tab_scripts)
        self.btn_stop_script.setGeometry(QtCore.QRect(120, 420, 101, 23))
        self.btn_stop_script.setObjectName(_fromUtf8("btn_stop_script"))
        self.btn_start_script = QtGui.QPushButton(self.tab_scripts)
        self.btn_start_script.setGeometry(QtCore.QRect(20, 420, 101, 23))
        self.btn_start_script.setObjectName(_fromUtf8("btn_start_script"))
        self.list_scripts = QtGui.QListView(self.tab_scripts)
        self.list_scripts.setGeometry(QtCore.QRect(0, 350, 711, 61))
        self.list_scripts.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.list_scripts.setModelColumn(0)
        self.list_scripts.setObjectName(_fromUtf8("list_scripts"))
        self.btn_plot_script = QtGui.QPushButton(self.tab_scripts)
        self.btn_plot_script.setGeometry(QtCore.QRect(0, 2, 101, 23))
        self.btn_plot_script.setObjectName(_fromUtf8("btn_plot_script"))
        self.tabWidget.addTab(self.tab_scripts, _fromUtf8(""))
        self.tab_monitor = QtGui.QWidget()
        self.tab_monitor.setObjectName(_fromUtf8("tab_monitor"))
        self.tree_monitor = QtGui.QTreeWidget(self.tab_monitor)
        self.tree_monitor.setEnabled(True)
        self.tree_monitor.setGeometry(QtCore.QRect(0, 30, 711, 431))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_monitor.sizePolicy().hasHeightForWidth())
        self.tree_monitor.setSizePolicy(sizePolicy)
        self.tree_monitor.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.tree_monitor.setHeaderHidden(False)
        self.tree_monitor.setObjectName(_fromUtf8("tree_monitor"))
        self.tree_monitor.header().setDefaultSectionSize(150)
        self.tree_monitor.header().setHighlightSections(True)
        self.btn_plot_probe = QtGui.QPushButton(self.tab_monitor)
        self.btn_plot_probe.setGeometry(QtCore.QRect(0, 2, 101, 23))
        self.btn_plot_probe.setObjectName(_fromUtf8("btn_plot_probe"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.tab_monitor)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(110, 0, 591, 31))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_probe_log_path = QtGui.QLabel(self.horizontalLayoutWidget)
        self.lbl_probe_log_path.setObjectName(_fromUtf8("lbl_probe_log_path"))
        self.horizontalLayout.addWidget(self.lbl_probe_log_path)
        self.txt_probe_log_path = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.txt_probe_log_path.setObjectName(_fromUtf8("txt_probe_log_path"))
        self.horizontalLayout.addWidget(self.txt_probe_log_path)
        self.chk_probe_log = QtGui.QCheckBox(self.horizontalLayoutWidget)
        self.chk_probe_log.setObjectName(_fromUtf8("chk_probe_log"))
        self.horizontalLayout.addWidget(self.chk_probe_log)
        self.tabWidget.addTab(self.tab_monitor, _fromUtf8(""))
        self.tab_settings = QtGui.QWidget()
        self.tab_settings.setObjectName(_fromUtf8("tab_settings"))
        self.tree_settings = QtGui.QTreeWidget(self.tab_settings)
        self.tree_settings.setEnabled(True)
        self.tree_settings.setGeometry(QtCore.QRect(0, 10, 711, 431))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_settings.sizePolicy().hasHeightForWidth())
        self.tree_settings.setSizePolicy(sizePolicy)
        self.tree_settings.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.tree_settings.setHeaderHidden(False)
        self.tree_settings.setObjectName(_fromUtf8("tree_settings"))
        self.tree_settings.header().setDefaultSectionSize(150)
        self.tree_settings.header().setHighlightSections(True)
        self.tabWidget.addTab(self.tab_settings, _fromUtf8(""))
        self.tab_history = QtGui.QWidget()
        self.tab_history.setObjectName(_fromUtf8("tab_history"))
        self.list_history = QtGui.QListView(self.tab_history)
        self.list_history.setGeometry(QtCore.QRect(0, 10, 711, 421))
        self.list_history.setObjectName(_fromUtf8("list_history"))
        self.tabWidget.addTab(self.tab_history, _fromUtf8(""))
        self.matplotlibwidget = MatplotlibWidget(self.centralwidget)
        self.matplotlibwidget.setGeometry(QtCore.QRect(10, 0, 321, 191))
        self.matplotlibwidget.setObjectName(_fromUtf8("matplotlibwidget"))
        self.matplotlibwidget_2 = MatplotlibWidget(self.centralwidget)
        self.matplotlibwidget_2.setGeometry(QtCore.QRect(740, 0, 391, 211))
        self.matplotlibwidget_2.setObjectName(_fromUtf8("matplotlibwidget_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1144, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.txt_tag.setText(_translate("MainWindow", "some tag", None))
        self.btn_clear_record.setText(_translate("MainWindow", "Delete", None))
        self.btn_save_record_to_disk.setText(_translate("MainWindow", "Save to disk", None))
        self.tree_scripts.headerItem().setText(0, _translate("MainWindow", "Parameter/Script", None))
        self.tree_scripts.headerItem().setText(1, _translate("MainWindow", "Value", None))
        self.btn_stop_script.setText(_translate("MainWindow", "stop", None))
        self.btn_start_script.setText(_translate("MainWindow", "start", None))
        self.btn_plot_script.setText(_translate("MainWindow", "plot script  ↑", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_scripts), _translate("MainWindow", "Scripts", None))
        self.tree_monitor.headerItem().setText(0, _translate("MainWindow", "Parameter", None))
        self.tree_monitor.headerItem().setText(1, _translate("MainWindow", "Value", None))
        self.btn_plot_probe.setText(_translate("MainWindow", "plot probe  ↑", None))
        self.lbl_probe_log_path.setText(_translate("MainWindow", "Path", None))
        self.chk_probe_log.setText(_translate("MainWindow", "logging on", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_monitor), _translate("MainWindow", "Monitor", None))
        self.tree_settings.headerItem().setText(0, _translate("MainWindow", "Instrument", None))
        self.tree_settings.headerItem().setText(1, _translate("MainWindow", "Value", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings), _translate("MainWindow", "Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_history), _translate("MainWindow", "History", None))

