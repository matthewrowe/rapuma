# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/rapuma/dialog/main.ui'
#
# Created: Fri Jan 24 04:35:57 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSystem = QtGui.QMenu(self.menubar)
        self.menuSystem.setObjectName("menuSystem")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuManageOpen = QtGui.QAction(MainWindow)
        self.menuManageOpen.setObjectName("menuManageOpen")
        self.menuManageNew = QtGui.QAction(MainWindow)
        self.menuManageNew.setObjectName("menuManageNew")
        self.menuManageQuit = QtGui.QAction(MainWindow)
        self.menuManageQuit.setObjectName("menuManageQuit")
        self.menuHelpAbout = QtGui.QAction(MainWindow)
        self.menuHelpAbout.setObjectName("menuHelpAbout")
        self.menuSystemPreferences = QtGui.QAction(MainWindow)
        self.menuSystemPreferences.setObjectName("menuSystemPreferences")
        self.menuHelpHelp = QtGui.QAction(MainWindow)
        self.menuHelpHelp.setObjectName("menuHelpHelp")
        self.menuManageBackup = QtGui.QAction(MainWindow)
        self.menuManageBackup.setObjectName("menuManageBackup")
        self.menuManageArchive = QtGui.QAction(MainWindow)
        self.menuManageArchive.setObjectName("menuManageArchive")
        self.menuManageRemove = QtGui.QAction(MainWindow)
        self.menuManageRemove.setObjectName("menuManageRemove")
        self.menuManageReap = QtGui.QAction(MainWindow)
        self.menuManageReap.setObjectName("menuManageReap")
        self.menuFile.addAction(self.menuManageNew)
        self.menuFile.addAction(self.menuManageOpen)
        self.menuFile.addAction(self.menuManageBackup)
        self.menuFile.addAction(self.menuManageArchive)
        self.menuFile.addAction(self.menuManageReap)
        self.menuFile.addAction(self.menuManageRemove)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuManageQuit)
        self.menuHelp.addAction(self.menuHelpHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.menuHelpAbout)
        self.menuSystem.addAction(self.menuSystemPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSystem.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Rapuma", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "Manage", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSystem.setTitle(QtGui.QApplication.translate("MainWindow", "System", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "open", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageOpen.setToolTip(QtGui.QApplication.translate("MainWindow", "Open an exsiting project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageNew.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageNew.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a new Rapuma project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageQuit.setToolTip(QtGui.QApplication.translate("MainWindow", "Quit Rapuma", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpAbout.setToolTip(QtGui.QApplication.translate("MainWindow", "Learn about what Rapuma is", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSystemPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSystemPreferences.setToolTip(QtGui.QApplication.translate("MainWindow", "Change Rapuma system preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpHelp.setToolTip(QtGui.QApplication.translate("MainWindow", "Find information about how to use Rapuma", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageBackup.setText(QtGui.QApplication.translate("MainWindow", "Backup", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageBackup.setToolTip(QtGui.QApplication.translate("MainWindow", "Backup an existing project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageArchive.setText(QtGui.QApplication.translate("MainWindow", "Archive", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageArchive.setToolTip(QtGui.QApplication.translate("MainWindow", "Archive an existing project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageRemove.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageRemove.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove an existing project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageReap.setText(QtGui.QApplication.translate("MainWindow", "REAP", None, QtGui.QApplication.UnicodeUTF8))
        self.menuManageReap.setToolTip(QtGui.QApplication.translate("MainWindow", "Add a project to SIL REAP (Archive)", None, QtGui.QApplication.UnicodeUTF8))

