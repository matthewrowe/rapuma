#!/usr/bin/python
# -*- coding: utf_8 -*-
# version: 20111210
# By Dennis Drescher (dennis_drescher at sil.org)

###############################################################################
######################### Description/Documentation ###########################
###############################################################################

# This class will handle book project tasks.

# History:
# 20111210 - djd - Started with intial file


###############################################################################
################################# Project Class ###############################
###############################################################################
# Firstly, import all the standard Python modules we need for
# this process

import os, codecs


# Load the local classes
from tools import *


###############################################################################
################################## Begin Class ################################
###############################################################################

class Component (object) :

    def __init__(self, project, cfg, parent = None) :
        '''Initialize this class.'''

        print "Initializing Component"

        self.project = project
        self.cfg = cfg
        self.parent = parent or project
        self.managers = {}
#        for key, value in cfg['Managers'].iteritems() :
#            self.managers[key] = project.createManager(value)
        
        # Commands that are associated with the Component level
#        self.addCommand("component_add", cmpCmd.AddCompGroup())

    def render(self) :
        print "Rendering Component"


