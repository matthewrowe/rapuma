#!/usr/bin/python
# -*- coding: utf_8 -*-
# version: 20111014
# By Dennis Drescher (dennis_drescher at sil.org)

###############################################################################
######################### Description/Documentation ###########################
###############################################################################

# This class will handle mostly housekeeping processes at the component level.

# History:
# 20111014 - djd - Started with intial file from RPM project


###############################################################################
################################### Shell Class ###############################
###############################################################################
# Firstly, import all the standard Python modules we need for
# this process

# import codecs, os

# Load the local classes

auxiliaryTypes = {}

class MetaAuxiliary(type) :

    def __init__(cls, namestring, t, d) :
        global auxiliaryTypes
        super(MetaAuxiliary, cls).__init__(namestring, t, d)
        if cls.type :
            auxiliaryTypes[cls.type] = cls


class Auxiliary (object) :
    __metaclass__ = MetaAuxiliary
    type = None

    initialized = False

    def __init__(self, aProject, auxConfig, typeConfig) :
        '''Initiate the entire class here'''
        self.project = aProject
        self.auxConfig = auxConfig
        self.typeConfig = typeConfig
        if not self.initialized : self.__class__.initType(aProject, typeConfig)

    def initClass(self) :
        '''Ensures everything is in place for components of this type to do their thing'''
        self.__class__.initialized = True
        
        
    @classmethod
    def initType(cls, aProject, typeConfig) :
        '''Internal housekeeping for the component type when it first wakes up'''
        cls.typeConfig = typeConfig


###############################################################################
########################### Auxiliary Init Functions ##########################
###############################################################################

    def initAuxiliary (self) :
        '''A dummy function to avoid errors.  Any real initilization of any
        auxiliary component should happen in the auxiliary itself.'''
        
        pass

