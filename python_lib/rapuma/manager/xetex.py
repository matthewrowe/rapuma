#!/usr/bin/python
# -*- coding: utf_8 -*-
# version: 20111207
# By Dennis Drescher (dennis_drescher at sil.org)

###############################################################################
######################### Description/Documentation ###########################
###############################################################################

# This manager class will handle component rendering with XeTeX.



###############################################################################
################################# Project Class ###############################
###############################################################################
# Firstly, import all the standard Python modules we need for
# this process

import os, shutil, re
import subprocess

# Load the local classes
from rapuma.core.tools import *
from rapuma.core.pt_tools import *
from rapuma.project.manager import Manager


###############################################################################
################################## Begin Class ################################
###############################################################################

class Xetex (Manager) :

    # Shared values
    xmlConfFile     = 'xetex.xml'

    def __init__(self, project, cfg, cType) :
        '''Do the primary initialization for this manager.'''

        super(Xetex, self).__init__(project, cfg)

        # Create all the values we can right now for this manager.
        # Others will be created at run time when we know the cid.
        self.project                = project
        self.local                  = project.local
        self.projConfig             = project.projConfig
        self.managers               = project.managers
        self.cfg                    = cfg
        self.cType                  = cType
        self.Ctype                  = cType.capitalize()
        self.cName                  = project.cName
        self.manager                = self.cType + '_Xetex'
        self.usePdfViewer           = self.projConfig['Managers'][self.manager]['usePdfViewer']
        self.pdfViewer              = self.projConfig['Managers'][self.manager]['pdfViewerCommand']
        self.macroPackage           = self.projConfig['Managers'][self.manager]['macroPackage']
        self.projComponentsFolder   = self.local.projComponentsFolder
        self.projStylesFolder       = self.local.projStylesFolder
        self.projMacrosFolder       = self.local.projMacrosFolder
        self.cNameFolder            = os.path.join(self.projComponentsFolder, self.cName)
        self.macLayoutValFile       = os.path.join(self.local.rapumaConfigFolder, 'layout_' + self.macroPackage + '.xml')
        self.projMacPackFolder      = os.path.join(self.local.projMacrosFolder, self.macroPackage)
        self.macPackFile            = os.path.join(self.projMacPackFolder, self.macroPackage + '.tex')
        self.ptxMargVerseFile       = os.path.join(self.projMacPackFolder, 'ptxplus-marginalverses.tex')
        self.sourceEditor           = self.projConfig['CompTypes'][self.Ctype]['sourceEditor']
        self.layoutConfig           = {}
        self.ptSSFConf              = {}
        # Make a PT settings dictionary
        if self.sourceEditor.lower() == 'paratext' :
            sourcePath = self.projConfig['CompTypes'][self.Ctype]['sourcePath']
            self.ptSSFConf = getPTSettings(sourcePath)
            if not self.ptSSFConf :
                self.project.log.writeToLog('XTEX-005')


        # This manager is dependent on usfm_Layout. Load it if needed.
        if 'usfm_Layout' not in self.project.managers :
            self.project.createManager(self.cType, 'layout')

        self.layoutConfig           = self.managers[self.cType + '_Layout'].layoutConfig

        # Get persistant values from the config if there are any
        # We assume at this point that if the merge has already taken place,
        # we do not need to do it again. We will check for a version number 
        # under the General Settings section to tell if it has been merged
        # already. FIXME: This may not be the best way to do this but we cannot
        # be writing this file out every time as it causes the PDF to get
        # rendered every time, which is not helpful.
        try :
            version = self.layoutConfig['GeneralSettings']['usfmTexVersion']
            self.project.log.writeToLog('XTEX-010', [version])
        except :
            # No version number means we need to merge the default and usfmTex layout settings
            newSectionSettings = getPersistantSettings(self.layoutConfig, self.macLayoutValFile)
            if newSectionSettings != self.layoutConfig :
                self.managers[self.cType + '_Layout'].layoutConfig = newSectionSettings

            macVals = ConfigObj(getXMLSettings(self.macLayoutValFile))
            layoutCopy = ConfigObj(self.local.layoutConfFile)
            layoutCopy.merge(macVals)
            self.managers[self.cType + '_Layout'].layoutConfig = layoutCopy
            self.layoutConfig = layoutCopy
            if writeConfFile(self.managers[self.cType + '_Layout'].layoutConfig) :
                self.project.log.writeToLog('XTEX-020')

        # Get settings for this component
        self.managerSettings = self.projConfig['Managers'][self.manager]
        for k, v in self.managerSettings.iteritems() :
            if v == 'True' or v == 'False' :
                setattr(self, k, str2bool(v))
            else :
                setattr(self, k, v)

        self.xetexErrorCodes =  {
            0   : 'Rendering succeful.',
            256 : 'Something really awful happened.'
                                }


###############################################################################
############################ Manager Level Functions ##########################
###############################################################################


###############################################################################
############################# DEPENDENCY FUNCTIONS ############################
###############################################################################

    def makeDepMacLink (self, thisFile) :
        '''Check for the exsistance of or the age of the macLink dependent file.
        Create or refresh if needed. If there are any problems, report and die.'''

        return True


    def makeDepSetFile (self, thisFile) :
        '''Check for the exsistance of or the age of the setFile dependent file.
        Create or refresh if needed. If there are any problems, report and die.'''

        return True


    def makeDepExtFile (self, thisFile) :
        '''Check for the exsistance of or the age of the extFile dependent file.
        Create or refresh if needed. If there are any problems, report and die.'''

        return True


    def makeDepGlobSty (self, thisFile) :
        '''Check for the exsistance of or the age of the globSty dependent file.
        Create or refresh if needed. If there are any problems, report and die.'''

        return True


    def makeDepCidUsfm (self, thisFile) :
        '''Check for the exsistance of or the age of the cidUsfm dependent file.
        Create or refresh if needed. If there are any problems, report and die.'''

        return True


###############################################################################
################################# Main Function ###############################
###############################################################################

    def run (self, force) :
        '''This will check all the dependencies for a component and then
        use XeTeX to render it.'''

        # Set the the file/path values we need
        macPack                = self.projConfig['Managers'][self.cType + '_Xetex']['macroPackage']
        if str2bool(self.projConfig['Managers'][self.cType + '_Hyphenation']['useHyphenation']) :
            hyphenTexFile      = os.path.join(self.local.projHyphenationFolder, self.projConfig['Managers']['usfm_Hyphenation']['hyphenTexFile'])
        else :
            hyphenTexFile      = ''
        layoutConfFile         = self.local.layoutConfFile
        fontConfFile           = self.local.fontConfFile
        setFileName            = 'xetex_settings_' + self.cType + '.tex'
        extFileName            = 'xetex_settings_' + self.cType + '-ext.tex'
        setFile                = os.path.join(self.projMacrosFolder, macPack, setFileName)
        extFile                = os.path.join(self.projMacrosFolder, macPack, extFileName)
        mainStyleFile          = self.projConfig['Managers'][self.cType + '_Style']['mainStyleFile']
        customStyleFile        = self.projConfig['Managers'][self.cType + '_Style']['customStyleFile']
        globSty                = os.path.join(self.projStylesFolder, mainStyleFile)
        custSty                = os.path.join(self.projStylesFolder, customStyleFile)

        # The macro link file is named according to the type of component
        macLinkFile                 = self.cType + 'MacLinkFile.tex'
        macLink                     = os.path.join(self.projMacrosFolder, macPack, macLinkFile)

        # Create the cid.tex file(s) that the cName.tex will use to get at the source
        # We will create this first so if something goes wrong we die sooner than later
        for cid in self.projConfig['Components'][self.cName]['cidList'] :
            cidCName = getUsfmCName(cid)
            cidFolder = os.path.join(self.projComponentsFolder, cidCName)
            cidTex = os.path.join(cidFolder, cid + '.tex')
            cidUsfm = os.path.join(cidFolder, cid + '.usfm')
            # User sty and macro extentions are optional at the cid level
            cidSty = ''
            if os.path.isfile(os.path.join(cidFolder, cid + '.sty')) :
                cidSty = os.path.join(cidFolder, cid + '.sty')
            cidExt = ''
            if os.path.isfile(os.path.join(cidFolder, cid + '-ext.tex')) :
                cidExt = os.path.join(cidFolder, cid + '-ext.tex')
            # Write out the cidTex file
            with codecs.open(cidTex, "w", encoding='utf_8') as cidTexObject :
                cidTexObject.write('% ' + fName(cidTex) + ' is auto-generated. Do not bother editing it.\n\n')
                if cidExt :
                    cNameTexObject.write('\\stylesheet{' + cidExt + '}\n')
                if cidSty :
                    cNameTexObject.write('\\stylesheet{' + cidSty + '}\n')
                if self.makeDepCidUsfm(cidUsfm) :
                    cidTexObject.write('\\ptxfile{' + cidUsfm + '}\n')

        # Create the cName.tex file that createCNamePDF() will use to render
        cNameTex            = os.path.join(self.cNameFolder, self.cName + '.tex')
        cNamePdf            = os.path.join(self.cNameFolder, self.cName + '.pdf')
        # Start writing out the cName.tex file. Check/make dependencies as we go.
        # If we fail to make a dependency it will die and report during that process.
        with codecs.open(cNameTex, "w", encoding='utf_8') as cNameTexObject :
            cNameTexObject.write('% ' + fName(cNameTex) + ' is auto-generated. Do not bother editing it.\n\n')
            if self.makeDepMacLink(macLink) :
                cNameTexObject.write('\\input \"' + macLink + '\"\n')
            if self.makeDepSetFile(setFile) :
                cNameTexObject.write('\\input \"' + setFile + '\"\n')
            if self.makeDepExtFile(extFile) :
                cNameTexObject.write('\\input \"' + extFile + '\"\n')
            if self.makeDepGlobSty(globSty) :
                cNameTexObject.write('\\stylesheet{' + globSty + '}\n')
            # Custom sty file at the global level is optional as is hyphenation
            if customStyleFile :
                cNameTexObject.write('\\stylesheet{' + custSty + '}\n')
            if hyphenTexFile :
                cNameTexObject.write('\\input \"' + hyphenTexFile + '\"\n')
            # Create the cidUsfm list which is one or more cid components
            for cid in self.projConfig['Components'][self.cName]['cidList'] :
                cidCName = getUsfmCName(cid)
                cidUsfm = os.path.join(self.projComponentsFolder, cidCName, cid + '.usfm')
                if self.makeDepCidUsfm(cidUsfm) :
                    cNameTexObject.write('\\ptxfile{' + cidUsfm + '}\n')
            # This can only hapen once in the whole process, this marks the end
            cNameTexObject.write('\\bye\n')


        
        
        # Call on createCNamePDF() to finish the process
        
        
        
