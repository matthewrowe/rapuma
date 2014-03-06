# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dennis/Projects/rapuma/lib/rapuma/dialog/menu_project_backup_dlg.ui'
#
# Created: Thu Mar  6 16:50:56 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MenuProjectBackup(object):
    def setupUi(self, MenuProjectBackup):
        MenuProjectBackup.setObjectName("MenuProjectBackup")
        MenuProjectBackup.resize(370, 473)
        self.gridLayout_2 = QtGui.QGridLayout(MenuProjectBackup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelSelectProject = QtGui.QLabel(MenuProjectBackup)
        self.labelSelectProject.setObjectName("labelSelectProject")
        self.gridLayout_2.addWidget(self.labelSelectProject, 0, 0, 1, 1)
        self.groupBoxBackupAction = QtGui.QGroupBox(MenuProjectBackup)
        self.groupBoxBackupAction.setObjectName("groupBoxBackupAction")
        self.gridLayout = QtGui.QGridLayout(self.groupBoxBackupAction)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButtonBackup = QtGui.QRadioButton(self.groupBoxBackupAction)
        self.radioButtonBackup.setChecked(True)
        self.radioButtonBackup.setObjectName("radioButtonBackup")
        self.gridLayout.addWidget(self.radioButtonBackup, 0, 0, 1, 2)
        self.radioButtonRestore = QtGui.QRadioButton(self.groupBoxBackupAction)
        self.radioButtonRestore.setChecked(False)
        self.radioButtonRestore.setObjectName("radioButtonRestore")
        self.gridLayout.addWidget(self.radioButtonRestore, 1, 0, 1, 2)
        self.radioButtonRemove = QtGui.QRadioButton(self.groupBoxBackupAction)
        self.radioButtonRemove.setObjectName("radioButtonRemove")
        self.gridLayout.addWidget(self.radioButtonRemove, 2, 0, 1, 2)
        self.radioButtonRestoreAlternate = QtGui.QRadioButton(self.groupBoxBackupAction)
        self.radioButtonRestoreAlternate.setObjectName("radioButtonRestoreAlternate")
        self.gridLayout.addWidget(self.radioButtonRestoreAlternate, 3, 0, 1, 2)
        self.radioButtonNewProject = QtGui.QRadioButton(self.groupBoxBackupAction)
        self.radioButtonNewProject.setObjectName("radioButtonNewProject")
        self.gridLayout.addWidget(self.radioButtonNewProject, 4, 0, 2, 2)
        self.radioButtonFlushBackups = QtGui.QRadioButton(self.groupBoxBackupAction)
        self.radioButtonFlushBackups.setObjectName("radioButtonFlushBackups")
        self.gridLayout.addWidget(self.radioButtonFlushBackups, 6, 0, 1, 2)
        self.labelBackupFile = QtGui.QLabel(self.groupBoxBackupAction)
        self.labelBackupFile.setEnabled(False)
        self.labelBackupFile.setObjectName("labelBackupFile")
        self.gridLayout.addWidget(self.labelBackupFile, 9, 0, 1, 2)
        self.lineEditAlternateBackup = QtGui.QLineEdit(self.groupBoxBackupAction)
        self.lineEditAlternateBackup.setEnabled(False)
        self.lineEditAlternateBackup.setObjectName("lineEditAlternateBackup")
        self.gridLayout.addWidget(self.lineEditAlternateBackup, 10, 0, 1, 2)
        self.pushButtonBrowseAlternateBackupFile = QtGui.QPushButton(self.groupBoxBackupAction)
        self.pushButtonBrowseAlternateBackupFile.setEnabled(False)
        self.pushButtonBrowseAlternateBackupFile.setObjectName("pushButtonBrowseAlternateBackupFile")
        self.gridLayout.addWidget(self.pushButtonBrowseAlternateBackupFile, 10, 2, 1, 1)
        self.labelNeLocation = QtGui.QLabel(self.groupBoxBackupAction)
        self.labelNeLocation.setEnabled(False)
        self.labelNeLocation.setObjectName("labelNeLocation")
        self.gridLayout.addWidget(self.labelNeLocation, 11, 0, 1, 2)
        self.lineEditNewProjectLocation = QtGui.QLineEdit(self.groupBoxBackupAction)
        self.lineEditNewProjectLocation.setEnabled(False)
        self.lineEditNewProjectLocation.setObjectName("lineEditNewProjectLocation")
        self.gridLayout.addWidget(self.lineEditNewProjectLocation, 12, 0, 1, 2)
        self.labelSelectBackup = QtGui.QLabel(self.groupBoxBackupAction)
        self.labelSelectBackup.setEnabled(False)
        self.labelSelectBackup.setObjectName("labelSelectBackup")
        self.gridLayout.addWidget(self.labelSelectBackup, 7, 0, 1, 1)
        self.pushButtonBrowseProjectLocation = QtGui.QPushButton(self.groupBoxBackupAction)
        self.pushButtonBrowseProjectLocation.setEnabled(False)
        self.pushButtonBrowseProjectLocation.setObjectName("pushButtonBrowseProjectLocation")
        self.gridLayout.addWidget(self.pushButtonBrowseProjectLocation, 12, 2, 1, 1)
        self.comboBoxSelectBackup = QtGui.QComboBox(self.groupBoxBackupAction)
        self.comboBoxSelectBackup.setEnabled(False)
        self.comboBoxSelectBackup.setObjectName("comboBoxSelectBackup")
        self.gridLayout.addWidget(self.comboBoxSelectBackup, 8, 0, 1, 3)
        self.gridLayout_2.addWidget(self.groupBoxBackupAction, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.pushButtonOk = QtGui.QPushButton(MenuProjectBackup)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.gridLayout_2.addWidget(self.pushButtonOk, 3, 1, 1, 1)
        self.pushButtonCancel = QtGui.QPushButton(MenuProjectBackup)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayout_2.addWidget(self.pushButtonCancel, 3, 2, 1, 1)
        self.comboBoxSelectProject = QtGui.QComboBox(MenuProjectBackup)
        self.comboBoxSelectProject.setObjectName("comboBoxSelectProject")
        self.gridLayout_2.addWidget(self.comboBoxSelectProject, 1, 0, 1, 3)

        self.retranslateUi(MenuProjectBackup)
        self.comboBoxSelectProject.setCurrentIndex(-1)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL("clicked()"), MenuProjectBackup.close)
        QtCore.QObject.connect(self.pushButtonOk, QtCore.SIGNAL("clicked()"), MenuProjectBackup.update)
        QtCore.QObject.connect(self.radioButtonRestore, QtCore.SIGNAL("toggled(bool)"), self.comboBoxSelectBackup.setEnabled)
        QtCore.QObject.connect(self.radioButtonRestore, QtCore.SIGNAL("toggled(bool)"), self.labelSelectBackup.setEnabled)
        QtCore.QObject.connect(self.radioButtonRemove, QtCore.SIGNAL("toggled(bool)"), self.labelSelectBackup.setEnabled)
        QtCore.QObject.connect(self.radioButtonRemove, QtCore.SIGNAL("toggled(bool)"), self.comboBoxSelectBackup.setEnabled)
        QtCore.QObject.connect(self.radioButtonRestoreAlternate, QtCore.SIGNAL("toggled(bool)"), self.labelBackupFile.setEnabled)
        QtCore.QObject.connect(self.radioButtonRestoreAlternate, QtCore.SIGNAL("toggled(bool)"), self.lineEditAlternateBackup.setEnabled)
        QtCore.QObject.connect(self.radioButtonRestoreAlternate, QtCore.SIGNAL("toggled(bool)"), self.pushButtonBrowseAlternateBackupFile.setEnabled)
        QtCore.QObject.connect(self.radioButtonNewProject, QtCore.SIGNAL("toggled(bool)"), self.labelBackupFile.setEnabled)
        QtCore.QObject.connect(self.radioButtonNewProject, QtCore.SIGNAL("toggled(bool)"), self.lineEditAlternateBackup.setEnabled)
        QtCore.QObject.connect(self.radioButtonNewProject, QtCore.SIGNAL("toggled(bool)"), self.pushButtonBrowseAlternateBackupFile.setEnabled)
        QtCore.QObject.connect(self.radioButtonNewProject, QtCore.SIGNAL("toggled(bool)"), self.labelNeLocation.setEnabled)
        QtCore.QObject.connect(self.radioButtonNewProject, QtCore.SIGNAL("toggled(bool)"), self.lineEditNewProjectLocation.setEnabled)
        QtCore.QObject.connect(self.radioButtonNewProject, QtCore.SIGNAL("toggled(bool)"), self.pushButtonBrowseProjectLocation.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MenuProjectBackup)
        MenuProjectBackup.setTabOrder(self.pushButtonCancel, self.comboBoxSelectProject)
        MenuProjectBackup.setTabOrder(self.comboBoxSelectProject, self.radioButtonBackup)
        MenuProjectBackup.setTabOrder(self.radioButtonBackup, self.radioButtonRestore)
        MenuProjectBackup.setTabOrder(self.radioButtonRestore, self.radioButtonRemove)
        MenuProjectBackup.setTabOrder(self.radioButtonRemove, self.radioButtonRestoreAlternate)
        MenuProjectBackup.setTabOrder(self.radioButtonRestoreAlternate, self.radioButtonNewProject)
        MenuProjectBackup.setTabOrder(self.radioButtonNewProject, self.radioButtonFlushBackups)
        MenuProjectBackup.setTabOrder(self.radioButtonFlushBackups, self.comboBoxSelectBackup)
        MenuProjectBackup.setTabOrder(self.comboBoxSelectBackup, self.lineEditAlternateBackup)
        MenuProjectBackup.setTabOrder(self.lineEditAlternateBackup, self.pushButtonBrowseAlternateBackupFile)
        MenuProjectBackup.setTabOrder(self.pushButtonBrowseAlternateBackupFile, self.lineEditNewProjectLocation)
        MenuProjectBackup.setTabOrder(self.lineEditNewProjectLocation, self.pushButtonBrowseProjectLocation)
        MenuProjectBackup.setTabOrder(self.pushButtonBrowseProjectLocation, self.pushButtonOk)

    def retranslateUi(self, MenuProjectBackup):
        MenuProjectBackup.setWindowTitle(QtGui.QApplication.translate("MenuProjectBackup", "Rapuma - Manage Backups", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSelectProject.setText(QtGui.QApplication.translate("MenuProjectBackup", "Select Project", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxBackupAction.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Define the action to be taken", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxBackupAction.setTitle(QtGui.QApplication.translate("MenuProjectBackup", "Select Action", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonBackup.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Backup the currently selected local project", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonBackup.setText(QtGui.QApplication.translate("MenuProjectBackup", "Backup Selected Project", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonRestore.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Restore the currently selected backup to the selected project", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonRestore.setText(QtGui.QApplication.translate("MenuProjectBackup", "Restore Selected Backup", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonRemove.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Remove the currently selected backup", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonRemove.setText(QtGui.QApplication.translate("MenuProjectBackup", "Remove Selected Backup", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonRestoreAlternate.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Restore a backup to a project from an alternate location", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonRestoreAlternate.setText(QtGui.QApplication.translate("MenuProjectBackup", "Restore Alternate Backup", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonNewProject.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Create a new project on your local system from an alternative backup", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonNewProject.setText(QtGui.QApplication.translate("MenuProjectBackup", "New Project From Alternate", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonFlushBackups.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Remove/Flush all the backups from the selected project", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonFlushBackups.setText(QtGui.QApplication.translate("MenuProjectBackup", "Flush Project Backups", None, QtGui.QApplication.UnicodeUTF8))
        self.labelBackupFile.setText(QtGui.QApplication.translate("MenuProjectBackup", "Alternate Backup File", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditAlternateBackup.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Path to a backup file", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBrowseAlternateBackupFile.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Browse to backup file you wish to restore", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBrowseAlternateBackupFile.setText(QtGui.QApplication.translate("MenuProjectBackup", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNeLocation.setText(QtGui.QApplication.translate("MenuProjectBackup", "New Project (Folder)", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditNewProjectLocation.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Path to an alternate restore location on the local system", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSelectBackup.setText(QtGui.QApplication.translate("MenuProjectBackup", "Select Backup", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBrowseProjectLocation.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Browse to a location to restore a backup", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBrowseProjectLocation.setText(QtGui.QApplication.translate("MenuProjectBackup", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectBackup.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Select a backup from the current project to restore", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOk.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Manage a backup operation", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOk.setText(QtGui.QApplication.translate("MenuProjectBackup", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Cancel this operation", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setText(QtGui.QApplication.translate("MenuProjectBackup", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectProject.setToolTip(QtGui.QApplication.translate("MenuProjectBackup", "Select project to restore a backup to", None, QtGui.QApplication.UnicodeUTF8))

