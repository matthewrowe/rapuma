# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dennis/Projects/rapuma/lib/rapuma/dialog/main_dlg.ui'
#
# Created: Mon Feb  3 15:25:56 2014
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
        self.stackedWidgetWorkArea = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidgetWorkArea.setGeometry(QtCore.QRect(10, 10, 781, 651))
        self.stackedWidgetWorkArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.stackedWidgetWorkArea.setObjectName("stackedWidgetWorkArea")
        self.pageBlank = QtGui.QWidget()
        self.pageBlank.setObjectName("pageBlank")
        self.stackedWidgetWorkArea.addWidget(self.pageBlank)
        self.pageProject = QtGui.QWidget()
        self.pageProject.setObjectName("pageProject")
        self.lineEditProjectName = QtGui.QLineEdit(self.pageProject)
        self.lineEditProjectName.setGeometry(QtCore.QRect(30, 110, 281, 27))
        self.lineEditProjectName.setObjectName("lineEditProjectName")
        self.labelProjectPid = QtGui.QLabel(self.pageProject)
        self.labelProjectPid.setGeometry(QtCore.QRect(70, 10, 181, 17))
        self.labelProjectPid.setObjectName("labelProjectPid")
        self.labelProjectProject = QtGui.QLabel(self.pageProject)
        self.labelProjectProject.setGeometry(QtCore.QRect(10, 10, 55, 17))
        self.labelProjectProject.setObjectName("labelProjectProject")
        self.pushButtonProjectBind = QtGui.QPushButton(self.pageProject)
        self.pushButtonProjectBind.setGeometry(QtCore.QRect(660, 10, 80, 27))
        self.pushButtonProjectBind.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButtonProjectBind.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButtonProjectBind.setObjectName("pushButtonProjectBind")
        self.stackedWidgetWorkArea.addWidget(self.pageProject)
        self.pageGroup = QtGui.QWidget()
        self.pageGroup.setObjectName("pageGroup")
        self.labelGroup = QtGui.QLabel(self.pageGroup)
        self.labelGroup.setGeometry(QtCore.QRect(10, 10, 50, 17))
        self.labelGroup.setObjectName("labelGroup")
        self.labelGroupGid = QtGui.QLabel(self.pageGroup)
        self.labelGroupGid.setGeometry(QtCore.QRect(70, 10, 80, 17))
        self.labelGroupGid.setObjectName("labelGroupGid")
        self.pushButtonGroupFinal = QtGui.QPushButton(self.pageGroup)
        self.pushButtonGroupFinal.setGeometry(QtCore.QRect(660, 10, 80, 27))
        self.pushButtonGroupFinal.setObjectName("pushButtonGroupFinal")
        self.pushButtonGroupDraft = QtGui.QPushButton(self.pageGroup)
        self.pushButtonGroupDraft.setGeometry(QtCore.QRect(480, 10, 80, 27))
        self.pushButtonGroupDraft.setObjectName("pushButtonGroupDraft")
        self.pushButtonGroupProof = QtGui.QPushButton(self.pageGroup)
        self.pushButtonGroupProof.setGeometry(QtCore.QRect(570, 10, 80, 27))
        self.pushButtonGroupProof.setObjectName("pushButtonGroupProof")
        self.stackedWidgetWorkArea.addWidget(self.pageGroup)
        self.pageComponent = QtGui.QWidget()
        self.pageComponent.setObjectName("pageComponent")
        self.labelComponentCid = QtGui.QLabel(self.pageComponent)
        self.labelComponentCid.setGeometry(QtCore.QRect(100, 10, 70, 17))
        self.labelComponentCid.setObjectName("labelComponentCid")
        self.labelComponentComponent = QtGui.QLabel(self.pageComponent)
        self.labelComponentComponent.setGeometry(QtCore.QRect(10, 10, 85, 17))
        self.labelComponentComponent.setObjectName("labelComponentComponent")
        self.pushButtonComponentFinal = QtGui.QPushButton(self.pageComponent)
        self.pushButtonComponentFinal.setGeometry(QtCore.QRect(660, 10, 80, 27))
        self.pushButtonComponentFinal.setObjectName("pushButtonComponentFinal")
        self.pushButtonComponentDraft = QtGui.QPushButton(self.pageComponent)
        self.pushButtonComponentDraft.setGeometry(QtCore.QRect(480, 10, 80, 27))
        self.pushButtonComponentDraft.setObjectName("pushButtonComponentDraft")
        self.pushButtonComponentProof = QtGui.QPushButton(self.pageComponent)
        self.pushButtonComponentProof.setGeometry(QtCore.QRect(570, 10, 80, 27))
        self.pushButtonComponentProof.setObjectName("pushButtonComponentProof")
        self.stackedWidgetWorkArea.addWidget(self.pageComponent)
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
        self.menuProjectSystempreferences = QtGui.QAction(MainWindow)
        self.menuProjectSystempreferences.setObjectName("menuProjectSystempreferences")
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
        self.actionDraft = QtGui.QAction(MainWindow)
        self.actionDraft.setObjectName("actionDraft")
        self.actionFinal = QtGui.QAction(MainWindow)
        self.actionFinal.setObjectName("actionFinal")
        self.actionProof = QtGui.QAction(MainWindow)
        self.actionProof.setObjectName("actionProof")
        self.actionDraft_2 = QtGui.QAction(MainWindow)
        self.actionDraft_2.setObjectName("actionDraft_2")
        self.actionFinal_2 = QtGui.QAction(MainWindow)
        self.actionFinal_2.setObjectName("actionFinal_2")
        self.actionProof_2 = QtGui.QAction(MainWindow)
        self.actionProof_2.setObjectName("actionProof_2")
        self.menuProjectEdit = QtGui.QAction(MainWindow)
        self.menuProjectEdit.setObjectName("menuProjectEdit")
        self.menuGroupEdit = QtGui.QAction(MainWindow)
        self.menuGroupEdit.setObjectName("menuGroupEdit")
        self.menuComponentEdit = QtGui.QAction(MainWindow)
        self.menuComponentEdit.setObjectName("menuComponentEdit")
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
        self.menuProject.addAction(self.menuProjectSystempreferences)
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
        self.menuGroup.addSeparator()
        self.menuGroup.addAction(self.actionDraft)
        self.menuGroup.addAction(self.actionFinal)
        self.menuGroup.addAction(self.actionProof)
        self.menuComponent.addAction(self.menuComponentAdd)
        self.menuComponent.addAction(self.menuComponentRemove)
        self.menuComponent.addAction(self.menuComponentSelect)
        self.menuComponent.addAction(self.menuComponentUpdate)
        self.menuComponent.addSeparator()
        self.menuComponent.addAction(self.actionDraft_2)
        self.menuComponent.addAction(self.actionFinal_2)
        self.menuComponent.addAction(self.actionProof_2)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuGroup.menuAction())
        self.menubar.addAction(self.menuComponent.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidgetWorkArea.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Rapuma", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditProjectName.setToolTip(QtGui.QApplication.translate("MainWindow", "Project name, could be book title", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditProjectName.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Project Name", None, QtGui.QApplication.UnicodeUTF8))
        self.labelProjectPid.setText(QtGui.QApplication.translate("MainWindow", "Project ID", None, QtGui.QApplication.UnicodeUTF8))
        self.labelProjectProject.setText(QtGui.QApplication.translate("MainWindow", "Project:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonProjectBind.setText(QtGui.QApplication.translate("MainWindow", "Bind", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGroup.setText(QtGui.QApplication.translate("MainWindow", "Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGroupGid.setText(QtGui.QApplication.translate("MainWindow", "Group ID", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGroupFinal.setToolTip(QtGui.QApplication.translate("MainWindow", "Create view of the final output of the selected component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGroupFinal.setText(QtGui.QApplication.translate("MainWindow", "Final", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGroupDraft.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a draft of the selected component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGroupDraft.setText(QtGui.QApplication.translate("MainWindow", "Draft", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGroupProof.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a proof of the selected component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGroupProof.setText(QtGui.QApplication.translate("MainWindow", "Proof", None, QtGui.QApplication.UnicodeUTF8))
        self.labelComponentCid.setText(QtGui.QApplication.translate("MainWindow", "Comp ID", None, QtGui.QApplication.UnicodeUTF8))
        self.labelComponentComponent.setText(QtGui.QApplication.translate("MainWindow", "Component:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonComponentFinal.setToolTip(QtGui.QApplication.translate("MainWindow", "Create view of the final output of the selected component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonComponentFinal.setText(QtGui.QApplication.translate("MainWindow", "Final", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonComponentDraft.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a draft of the selected component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonComponentDraft.setText(QtGui.QApplication.translate("MainWindow", "Draft", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonComponentProof.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a proof of the selected component(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonComponentProof.setText(QtGui.QApplication.translate("MainWindow", "Proof", None, QtGui.QApplication.UnicodeUTF8))
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
        self.menuProjectSystempreferences.setText(QtGui.QApplication.translate("MainWindow", "System Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectSystempreferences.setToolTip(QtGui.QApplication.translate("MainWindow", "Change Rapuma system preferences", None, QtGui.QApplication.UnicodeUTF8))
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
        self.actionDraft.setText(QtGui.QApplication.translate("MainWindow", "Draft", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFinal.setText(QtGui.QApplication.translate("MainWindow", "Final", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProof.setText(QtGui.QApplication.translate("MainWindow", "Proof", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDraft_2.setText(QtGui.QApplication.translate("MainWindow", "Draft", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFinal_2.setText(QtGui.QApplication.translate("MainWindow", "Final", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProof_2.setText(QtGui.QApplication.translate("MainWindow", "Proof", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectEdit.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProjectEdit.setToolTip(QtGui.QApplication.translate("MainWindow", "Edit settings or render the current project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupEdit.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupEdit.setToolTip(QtGui.QApplication.translate("MainWindow", "Edit settings or render the current group", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentEdit.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuComponentEdit.setToolTip(QtGui.QApplication.translate("MainWindow", "Edit settings or render the current component", None, QtGui.QApplication.UnicodeUTF8))

