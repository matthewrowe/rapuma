#!/usr/bin/python
# -*- coding: utf_8 -*-
# version: 20111207
# By Dennis Drescher (dennis_drescher at sil.org)

###############################################################################
######################### Description/Documentation ###########################
###############################################################################

# This class will handle book project tasks.

# History:
# 20111207 - djd - Started with intial file


###############################################################################
################################# Project Class ###############################
###############################################################################
# Firstly, import all the standard Python modules we need for
# this process

import os


# Load the local classes
from tools import *
from project import Project


###############################################################################
################################## Begin Class ################################
###############################################################################

class Book (Project) :
    '''This contains basic information about a type of project.'''

    configFile = "book.xml"
    configInitFile = "book_init.xml"

# FIXME: Here we want to run through the settings in the init.xml file and
# create anything that the project is supposed to have. Processes that follow
# will rely on this being done. Otherwise, things will break.


