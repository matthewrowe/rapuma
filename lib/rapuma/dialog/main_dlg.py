# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dennis/Projects/rapuma/lib/rapuma/dialog/main_dlg.ui'
#
# Created: Sun Jan 26 20:24:19 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 714)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainTabWidget = QtGui.QTabWidget(self.centralwidget)
        self.mainTabWidget.setGeometry(QtCore.QRect(10, 40, 781, 611))
        self.mainTabWidget.setObjectName("mainTabWidget")
        self.mainProject = QtGui.QWidget()
        self.mainProject.setObjectName("mainProject")
        self.gridLayout = QtGui.QGridLayout(self.mainProject)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditProjName = QtGui.QLineEdit(self.mainProject)
        self.lineEditProjName.setObjectName("lineEditProjName")
        self.gridLayout.addWidget(self.lineEditProjName, 0, 0, 1, 1)
        self.mainTabWidget.addTab(self.mainProject, "")
        self.mainGroup = QtGui.QWidget()
        self.mainGroup.setObjectName("mainGroup")
        self.mainTabWidget.addTab(self.mainGroup, "")
        self.mainComponent = QtGui.QWidget()
        self.mainComponent.setObjectName("mainComponent")
        self.mainTabWidget.addTab(self.mainComponent, "")
        self.mainLog = QtGui.QWidget()
        self.mainLog.setObjectName("mainLog")
        self.mainTabWidget.addTab(self.mainLog, "")
        self.labelProject = QtGui.QLabel(self.centralwidget)
        self.labelProject.setGeometry(QtCore.QRect(10, 10, 60, 17))
        self.labelProject.setObjectName("labelProject")
        self.labelPid = QtGui.QLabel(self.centralwidget)
        self.labelPid.setGeometry(QtCore.QRect(68, 10, 80, 17))
        self.labelPid.setObjectName("labelPid")
        self.labelGroup = QtGui.QLabel(self.centralwidget)
        self.labelGroup.setGeometry(QtCore.QRect(160, 10, 50, 17))
        self.labelGroup.setObjectName("labelGroup")
        self.labelGid = QtGui.QLabel(self.centralwidget)
        self.labelGid.setGeometry(QtCore.QRect(210, 10, 80, 17))
        self.labelGid.setObjectName("labelGid")
        self.labelComponent = QtGui.QLabel(self.centralwidget)
        self.labelComponent.setGeometry(QtCore.QRect(280, 10, 85, 17))
        self.labelComponent.setObjectName("labelComponent")
        self.labelCid = QtGui.QLabel(self.centralwidget)
        self.labelCid.setGeometry(QtCore.QRect(368, 10, 70, 17))
        self.labelCid.setObjectName("labelCid")
        self.pushButtonDraft = QtGui.QPushButton(self.centralwidget)
        self.pushButtonDraft.setGeometry(QtCore.QRect(470, 5, 80, 27))
        self.pushButtonDraft.setObjectName("pushButtonDraft")
        self.pushButtonProof = QtGui.QPushButton(self.centralwidget)
        self.pushButtonProof.setGeometry(QtCore.QRect(560, 5, 80, 27))
        self.pushButtonProof.setObjectName("pushButtonProof")
        self.pushButtonFinal = QtGui.QPushButton(self.centralwidget)
        self.pushButtonFinal.setGeometry(QtCore.QRect(650, 5, 80, 27))
        self.pushButtonFinal.setObjectName("pushButtonFinal")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuGroup = QtGui.QMenu(self.menubar)
        self.menuGroup.setObjectName("menuGroup")
        self.menuComponent = QtGui.QMenu(self.menubar)
        self.menuComponent.setObjectName("menuComponent")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuProjectSelect = QtGui.QAction(MainWindow)
        self.menuProjectSelect.setObjectName("menuProjectSelect")
        self.menuProjectAdd = QtGui.QAction(MainWindow)
        self.menuProjectAdd.setObjectName("menuProjectAdd")
        self.menuProjectQuit = QtGui.QAction(MainWindow)
        self.menuProjectQuit.setObjectName("menuProjectQuit")
        self.menuHelpAbout = QtGui.QAction(MainWindow)
        self.menuHelpAbout.setObjectName("menuHelpAbout")
        self.menuProjectSystemPreferences = QtGui.QAction(MainWindow)
        self.menuProjectSystemPreferences.setObjectName("menuProjectSystemPreferences")
        self.menuHelpHelp = QtGui.QAction(MainWindow)
        self.menuHelpHelp.setObjectName("menuHelpHelp")
        self.menuProjectBackup = QtGui.QAction(MainWindow)
        self.menuProjectBackup.setObjectName("menuProjectBackup")
        self.menuProjectArchive = QtGui.QAction(MainWindow)
        self.menuProjectArchive.setObjectName("menuProjectArchive")
        self.menuProjectRemove = QtGui.QAction(MainWindow)
        self.menuProjectRemove.setObjectName("menuProjectRemove")
        self.menuProjectReap = QtGui.QAction(MainWindow)
        self.menuProjectReap.setObjectName("menuProjectReap")
        self.menuProjectTemplate = QtGui.QAction(MainWindow)
        self.menuProjectTemplate.setObjectName("menuProjectTemplate")
        self.menuComponentAdd = QtGui.QAction(MainWindow)
        self.menuComponentAdd.setObjectName("menuComponentAdd")
        self.menuComponentRemove = QtGui.QAction(MainWindow)
        self.menuComponentRemove.setObjectName("menuComponentRemove")
        self.menuComponentSelect = QtGui.QAction(MainWindow)
        self.menuComponentSelect.setObjectName("menuComponentSelect")
        self.menuGroupAdd = QtGui.QAction(MainWindow)
        self.menuGroupAdd.setObjectName("menuGroupAdd")
        self.menuGroupRemove = QtGui.QAction(MainWindow)
        self.menuGroupRemove.setObjectName("menuGroupRemove")
        self.menuGroupSelect = QtGui.QAction(MainWindow)
        self.menuGroupSelect.setObjectName("menuGroupSelect")
        self.menuProjectRestore = QtGui.QAction(MainWindow)
        self.menuProjectRestore.setObjectName("menuProjectRestore")
        self.menuProjectBind = QtGui.QAction(MainWindow)
        self.menuProjectBind.setObjectName("menuProjectBind")
        self.menuProjectCloud = QtGui.QAction(MainWindow)
        self.menuProjectCloud.setObjectName("menuProjectCloud")
        self.menuHelpExamples = QtGui.QAction(MainWindow)
        self.menuHelpExamples.setObjectName("menuHelpExamples")
        self.menuGroupUpdate = QtGui.QAction(MainWindow)
        self.menuGroupUpdate.setObjectName("menuGroupUpdate")
        self.menuComponentUpdate = QtGui.QAction(MainWindow)
        self.menuComponentUpdate.setObjectName("menuComponentUpdate")
        self.menuProjectUpdate = QtGui.QAction(MainWindow)
        self.menuProjectUpdate.setObjectName("menuProjectUpdate")
        self.menuProject.addAction(self.menuProjectAdd)
        self.menuProject.addAction(self.menuProjectRemove)
        self.menuProject.addAction(self.menuProjectRestore)
        self.menuProject.addAction(self.menuProjectSelect)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.menuProjectArchive)
        self.menuProject.addAction(self.menuProjectCloud)
        self.menuProject.addAction(self.menuProjectBackup)
        self.menuProject.addAction(self.menuProjectBind)
        self.menuProject.addAction(self.menuProjectReap)
        self.menuProject.addAction(self.menuProjectTemplate)
        self.menuProject.addAction(self.menuProjectUpdate)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.menuProjectSystemPreferences)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.menuProjectQuit)
        self.menuHelp.addAction(self.menuHelpHelp)
        self.menuHelp.addAction(self.menuHelpExamples)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.menuHelpAbout)
        self.menuGroup.addAction(self.menuGroupAdd)
        self.menuGroup.addAction(self.menuGroupRemove)
        self.menuGroup.addAction(self.menuGroupSelect)
        self.menuGroup.addAction(self.menuGroupUpdate)
        self.menuComponent.addAction(self.menuComponentAdd)
        self.menuComponent.addAction(self.menuComponentRemove)
        self.menuComponent.addAction(self.menuComponentSelect)
        self.menuComponent.addAction(self.menuComponentUpdate)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuGroup.menuAction())
        self.menubar.addAction(self.menuComponent.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.mainTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButtonDraft, QtCore.SIGNAL("clicked()"), MainWindow.setupUi)
        QtCore.QObject.connect(self.pushButtonProof, QtCore.SIGNAL("clicked()"), MainWindow.setupUi)
        QtCore.QObject.connect(self.pushButtonFinal, QtCore.SIGNAL("clicked()"), MainWindow.setupUi)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Rapuma", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditProjName.setToolTip(QtGui.QApplication.translate("MainWindow", "Project name, could be book title", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditProjName.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Project Name", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.mainProject), QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabToolTip(self.mainTabWidget.indexOf(self.mainProject), QtGui.QApplication.translate("MainWindow", "Project-wide information and settings", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.mainGroup), QtGui.QApplication.translate("MainWindow", "Group", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabToolTip(self.mainTabWidget.indexOf(self.mainGroup), QtGui.QApplication.translate("MainWindow", "Group-wide settings and information", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.mainComponent), QtGui.QApplication.translate("MainWindow", "Component", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabToolTip(self.mainTabWidget.indexOf(self.mainComponent), QtGui.QApplication.translate("MainWindow", "Component settings, information and source and working text", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.mainLog), QtGui.QApplication.translate("MainWindow", "Logs", None, QtGui.QApplication.UnicodeUTF8))
        self.labelProject.setText(QtGui.QApplication.translate("MainWindow", "Project:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPid.setText(QtGui.QApplication.translate("MainWindow", "Project ID", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGroup.setText(QtGui.QApplication.translate("MainWindow", "Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGid.setText(QtGui.QApplication.translate("MainWindow", "Group ID", None, QtGui.QApplication.UnicodeUTF8))
        self.labelComponent.setText(QtGui.QApplication.translate("MainWindow", "Component:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCid.setText(QtGui.QApplication.translate("MainWindow", "Comp ID", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDraft.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a draft of the selected component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDraft.setText(QtGui.QApplication.translate("MainWindow", "Draft", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonProof.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a proof of the selected component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonProof.setText(QtGui.QApplication.translate("MainWindow", "Proof", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonFinal.setToolTip(QtGui.QApplication.translate("MainWindow", "Create view of the final output of the selected component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonFinal.setText(QtGui.QApplication.translate("MainWindow", "Final", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroup.setTitle(QtGui.QApplication.translate("MainWindow", "Group", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponent.setTitle(QtGui.QApplication.translate("MainWindow", "Component", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "open", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectSelect.setText(QtGui.QApplication.translate("MainWindow", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectSelect.setToolTip(QtGui.QApplication.translate("MainWindow", "Open an exsiting project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectAdd.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectAdd.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a new Rapuma project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectQuit.setToolTip(QtGui.QApplication.translate("MainWindow", "Quit Rapuma", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpAbout.setToolTip(QtGui.QApplication.translate("MainWindow", "Learn about what Rapuma is", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectSystemPreferences.setText(QtGui.QApplication.translate("MainWindow", "System Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectSystemPreferences.setToolTip(QtGui.QApplication.translate("MainWindow", "Change Rapuma system preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpHelp.setToolTip(QtGui.QApplication.translate("MainWindow", "Find information about how to use Rapuma", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectBackup.setText(QtGui.QApplication.translate("MainWindow", "Backup", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectBackup.setToolTip(QtGui.QApplication.translate("MainWindow", "Backup an existing project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectArchive.setText(QtGui.QApplication.translate("MainWindow", "Archive", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectArchive.setToolTip(QtGui.QApplication.translate("MainWindow", "Archive an existing project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectRemove.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectRemove.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove an existing project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectReap.setText(QtGui.QApplication.translate("MainWindow", "REAP", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectReap.setToolTip(QtGui.QApplication.translate("MainWindow", "Add a project to SIL REAP (Archive)", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectTemplate.setText(QtGui.QApplication.translate("MainWindow", "Template", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentAdd.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentAdd.setToolTip(QtGui.QApplication.translate("MainWindow", "Add a component to the selected group", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentRemove.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentRemove.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove a component from the selected group", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentSelect.setText(QtGui.QApplication.translate("MainWindow", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentSelect.setToolTip(QtGui.QApplication.translate("MainWindow", "Select a component(s) to render ", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupAdd.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupAdd.setToolTip(QtGui.QApplication.translate("MainWindow", "Add a group to this project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupRemove.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupRemove.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove a group from this project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupSelect.setText(QtGui.QApplication.translate("MainWindow", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupSelect.setToolTip(QtGui.QApplication.translate("MainWindow", "Select a group to process in this project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectRestore.setText(QtGui.QApplication.translate("MainWindow", "Restore", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectRestore.setToolTip(QtGui.QApplication.translate("MainWindow", "Restore a Rapuma project from backup or archive", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectBind.setText(QtGui.QApplication.translate("MainWindow", "Bind", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectBind.setToolTip(QtGui.QApplication.translate("MainWindow", "Bind groups in the main content section", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectCloud.setText(QtGui.QApplication.translate("MainWindow", "Cloud", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectCloud.setToolTip(QtGui.QApplication.translate("MainWindow", "Save the current project to the cloud", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpExamples.setText(QtGui.QApplication.translate("MainWindow", "Examples", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelpExamples.setToolTip(QtGui.QApplication.translate("MainWindow", "Try a couple Rapuma project examples", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupUpdate.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupUpdate.setToolTip(QtGui.QApplication.translate("MainWindow", "Update a group(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentUpdate.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentUpdate.setToolTip(QtGui.QApplication.translate("MainWindow", "Update a component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectUpdate.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectUpdate.setToolTip(QtGui.QApplication.translate("MainWindow", "Update project elements", None, QtGui.QApplication.UnicodeUTF8))

