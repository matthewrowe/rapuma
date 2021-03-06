#!/usr/bin/python
# -*- coding: utf-8 -*-

#    Copyright 2014, SIL International
#    All rights reserved.
#
#    This library is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 2.1 of License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should also have received a copy of the GNU Lesser General Public
#    License along with this library in the file named "LICENSE".
#    If not, write to the Free Software Foundation, 51 Franklin Street,
#    suite 500, Boston, MA 02110-1335, USA or visit their web page on the 
#    internet at http://www.fsf.org/licenses/lgpl.html.


import os, sys, StringIO

# Load GUI modules
from PySide                             import QtGui, QtCore
from PySide.QtGui                       import QDialog, QApplication, QMessageBox
from PySide.QtCore                      import QPropertyAnimation
from rapuma.dialog                      import menu_component_select_dlg
from rapuma.core.paratext               import Paratext

# Load the Rapuma lib classes
from rapuma.core.tools                  import Tools

class MenuComponentSelectCtrl (QDialog, QPropertyAnimation, menu_component_select_dlg.Ui_MenuComponentSelect) :

    def __init__ (self, guiSettings, userConfig, projectConfig, parent=None) :
        '''Initialize and start up the UI'''

        super(MenuComponentSelectCtrl, self).__init__(parent)

        self.tools = Tools()
        self.setupUi(self)
        self.connectionActions()
        self.userConfig         = userConfig
        self.projectConfig      = projectConfig
        self.guiSettings        = guiSettings
        self.selectedComponent  = None
        self.pt_tools           = Paratext(self.guiSettings.currentPid, self.guiSettings.currentGid)

        # Populate the list with groups from the current project
        for c in self.projectConfig['Groups'][self.guiSettings.currentGid]['cidList'] :
            name = self.pt_tools.usfmCidInfo()[c.lower()][0]
            # The ID has the name tacked on
            self.listWidgetComponents.addItem(c + ' (' + name + ')')


    def main (self) :
        '''This function shows the main dialog'''

        self.show()


    def connectionActions (self) :
        '''Connect to form buttons.'''

        self.pushButtonOk.clicked.connect(self.okClicked)


    def okClicked (self) :
        '''Execute the OK button.'''

        self.guiSettings.currentCid = self.listWidgetComponents.currentItem().text().split()[0]
        self.selectedComponent = self.guiSettings.currentCid
        self.guiSettings.setBookmarks()
        self.close()


###############################################################################
############################## Dialog Starts Here #############################
###############################################################################

if __name__ == '__main__' :

    app = QApplication(sys.argv)
    window = MenuComponentSelectCtrl()
    window.main()
    sys.exit(app.exec_())


