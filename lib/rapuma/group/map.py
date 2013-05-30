#!/usr/bin/python
# -*- coding: utf_8 -*-
# version: 20111207
# By Dennis Drescher (dennis_drescher at sil.org)

###############################################################################
######################### Description/Documentation ###########################
###############################################################################

# This class handles Map component type tasks for book projects.


###############################################################################
################################# Project Class ###############################
###############################################################################
# Firstly, import all the standard Python modules we need for
# this process

import os, codecs
from configobj import ConfigObj, Section
#from functools import partial

# Load the local classes
from rapuma.core.tools              import Tools
from rapuma.core.page_background    import PageBackground
from rapuma.group.group             import Group


###############################################################################
################################## Begin Class ################################
###############################################################################

# As we load the module we will bring in all the common information about all the
# components this type will handle.



class Map (Group) :
    '''This class contains information about a type of component 
    used in a type of project.'''

    # Shared values
    xmlConfFile     = 'map.xml'

    def __init__(self, project, cfg) :
        super(Map, self).__init__(project, cfg)

        # Set values for this manager
        self.pid                    = project.projectIDCode
        self.gid                    = project.gid
        self.cType                  = 'map'
        self.Ctype                  = self.cType.capitalize()
        self.mType                  = project.projectMediaIDCode
        self.tools                  = Tools()
        self.project                = project
        self.projConfig             = project.projConfig
        self.local                  = project.local
        self.log                    = project.log
        self.cfg                    = cfg
        self.renderer               = project.projConfig['CompTypes'][self.Ctype]['renderer']
        self.sourceEditor           = project.projConfig['CompTypes'][self.Ctype]['sourceEditor']
        # Get the comp settings
        self.compSettings           = project.projConfig['CompTypes'][self.Ctype]

        # Build a tuple of managers this component type needs to use
        self.mapManagers = ('component', 'text', 'style', 'font', 'layout', 'illustration', self.renderer)

        # Init the general managers
        for mType in self.mapManagers :
            self.project.createManager(mType)

        # Create the internal ref names we use in this module
        self.font                   = self.project.managers[self.cType + '_Font']
        self.component              = self.project.managers[self.cType + '_Component']
        self.layout                 = self.project.managers[self.cType + '_Layout']
        self.illustration           = self.project.managers[self.cType + '_Illustration']
        self.text                   = self.project.managers[self.cType + '_Text']
        self.style                  = self.project.managers[self.cType + '_Style']
        # File names

        # Folder paths
        self.projScriptsFolder      = self.local.projScriptsFolder
        self.projComponentsFolder   = self.local.projComponentsFolder
        self.gidFolder              = os.path.join(self.projComponentsFolder, self.gid)
        # File names with folder paths
        self.rapumaXmlCompConfig    = os.path.join(self.project.local.rapumaConfigFolder, self.xmlConfFile)

        # Get persistant values from the config if there are any
        newSectionSettings = self.tools.getPersistantSettings(self.projConfig['CompTypes'][self.Ctype], self.rapumaXmlCompConfig)
        if newSectionSettings != self.projConfig['CompTypes'][self.Ctype] :
            self.projConfig['CompTypes'][self.Ctype] = newSectionSettings
        # Set them here
        for k, v in self.compSettings.iteritems() :
            setattr(self, k, v)

        # Check if there is a font installed
        if not self.font.varifyFont() :
            # If a PT project, use that font, otherwise, install default
            if self.sourceEditor.lower() == 'paratext' :
                font = self.project.projConfig['Managers'][self.cType + '_Font']['ptDefaultFont']
            else :
                font = 'DefaultFont'

            self.font.installFont(font)

        # Module Error Codes
        self.errorCodes     = {

            '0010' : ['LOG', 'Created the [<<1>>] master adjustment file.'],
            '0220' : ['ERR', 'Cannot find: [<<1>>] working file, unable to complete preprocessing for rendering.'],
            '0230' : ['LOG', 'Created the [<<1>>] component adjustment file.'],
            '0240' : ['LOG', 'Could not find adjustments for [<<1>>], created place holder setting.'],
            '0255' : ['LOG', 'Illustrations not being used. The piclist file has been removed from the [<<1>>] illustrations folder.'],
            '0265' : ['LOG', 'Piclist file for [<<1>>] has been created.'],
        }

        # Pick up some init settings that come after the managers have been installed
        self.macroPackage           = self.projConfig['Managers'][self.cType + '_' + self.renderer.capitalize()]['macroPackage']
        self.layoutConfig           = self.layout.layoutConfig


###############################################################################
############################ Functions Begin Here #############################
###############################################################################
######################## Error Code Block Series = 0200 #######################
###############################################################################

    def getCidPath (self, cid) :
        '''Return the full path of the cName working text file. This assumes
        the cid is valid.'''

        return os.path.join(self.local.projComponentsFolder, cid, self.component.makeFileNameWithExt(cid))


    def getCidPiclistPath (self, cid) :
        '''Return the full path of the cName working text illustrations file. 
        This assumes the cName is valid.'''

        return os.path.join(self.local.projComponentsFolder, cid, self.component.makeFileName(cid) + '.piclist')


    def render(self, gid, mode, cidList, force) :
        '''Does Map specific rendering of a Map component'''

#        import pdb; pdb.set_trace()

        # If the whole group is being rendered, we need to preprocess it
        cids = []
        if not cidList :
            cids = self.projConfig['Groups'][gid]['cidList']
        else :
            cids = cidList

        # Preprocess all subcomponents (one or more)
        # Stop if it breaks at any point
        for cid in cids :
            if not self.preProcessGroup(gid, mode, cids) :
                return False

        # With everything in place we can render the component and we pass-through
        # the force (render/view) command so the renderer will do the right thing.
        # Note: We pass the cidList straight through
        self.project.managers['map_' + self.renderer.capitalize()].run(gid, mode, cidList, force)

        return True


    def preProcessGroup (self, gid, mode, cidList) :
        '''This will prepare a map component group for rendering by checking
        for and/or creating any dependents it needs to render properly.'''

        # Check if there is a font installed
        if not self.font.varifyFont() :
            # If a PT project, use that font, otherwise, install default
            if self.sourceEditor.lower() == 'paratext' :
                font = self.projConfig['Managers'][self.cType + '_Font']['ptDefaultFont']
            else :
                font = 'DefaultFont'

            self.font.installFont(font)

        # Will need the stylesheet for copy if that has not been added
        # to the project yet, we will do that now
        self.style.checkDefaultStyFile()
        self.style.checkDefaultExtStyFile()
        self.style.checkGrpExtStyFile()

        # See if the working text is present for each subcomponent in the
        # component and try to install it if it is not
        for cid in cidList :
            cType = self.cfg['cType']
            cidMap = self.getCidPath(cid)
            # Test for source here and die if it isn't there
            if not os.path.isfile(cidMap) :
                self.log.writeToLog(self.errorCodes['0220'], [cid], 'map.preProcessGroup():0220')

            # Add/manage the dependent files for this cid
            if self.macroPackage == 'usfmTex' :
                # Component piclist file
                cidPiclist = self.getCidPiclistPath(cid)


#                import pdb; pdb.set_trace()



                if self.illustration.hasIllustrations(gid, cid) :
                    # Create if not there of if the config has changed
                    if not os.path.isfile(cidPiclist) or self.tools.isOlder(cidPiclist, self.local.illustrationConfFile) :
                        # First check if we have the illustrations we think we need
                        # and get them if we do not.
                        self.illustration.getPics(gid, cid)
                        # Now make a fresh version of the piclist file
                        self.illustration.createPiclistFile(gid, cid)
                        self.log.writeToLog(self.errorCodes['0265'], [cid])
                    else :
                        for f in [self.local.layoutConfFile, self.local.illustrationConfFile] :
                            if self.tools.isOlder(cidPiclist, f) or not os.path.isfile(cidPiclist) :
                                # Remake the piclist file
                                self.illustration.createPiclistFile(gid, cid)
                                self.log.writeToLog(self.errorCodes['0265'], [cid])
                    # Do a quick check to see if the illustration files for this book
                    # are in the project. If it isn't, the run will be killed
                    self.illustration.getPics(gid, cid)
                else :
                    # If we are not using illustrations then any existing piclist file will be removed
                    if os.path.isfile(cidPiclist) :
                        os.remove(cidPiclist)
                        self.log.writeToLog(self.errorCodes['0255'], [cid])
            else :
                self.log.writeToLog(self.errorCodes['0220'], [self.macroPackage])

        # Background management
        bgList = self.projConfig['Managers'][self.cType + '_' + self.renderer.capitalize()][mode + 'Background']
        for bg in bgList :
            # For some reason it is best to load the mod right here
            PageBackground(self.pid).checkForBackground(bg, mode)

        # Any more stuff to run?

        return True



###############################################################################
######################### Map Component Text Functions ########################
###############################################################################
######################## Error Code Block Series = 0400 #######################
###############################################################################


    def getComponentType (self, gid) :
        '''Return the cType for a component.'''

#        import pdb; pdb.set_trace()

        try :
            cType = self.projConfig['Groups'][gid]['cType']
        except Exception as e :
            # If we don't succeed, we should probably quite here
            self.log.writeToLog('COMP-200', ['Key not found ' + str(e)])
            self.tools.dieNow()

        return cType


    def isCompleteComponent (self, gid, cid) :
        '''A two-part test to see if a component has a config entry and a file.'''

        if self.hasCidFile(gid, cid) :
            return True


    def hasCidFile (self, gid, cid) :
        '''Return True or False depending on if a working file exists 
        for a given cName.'''

        cType = self.projConfig['Groups'][gid]['cType']
        return os.path.isfile(os.path.join(self.local.projComponentsFolder, cid, cid + '.' + cType))


