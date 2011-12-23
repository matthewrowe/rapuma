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
from component import Component


###############################################################################
################################## Begin Class ################################
###############################################################################

class Usfm (Component) :

    def render(self) :

        print "Rendering USFM"

