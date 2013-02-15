#!/usr/bin/python
# -*- coding: utf_8 -*-
# version: 20111207
# By Dennis Drescher (dennis_drescher at sil.org)

###############################################################################
######################### Description/Documentation ###########################
###############################################################################

# This class handles USFM component type tasks for book projects.


###############################################################################
################################# Project Class ###############################
###############################################################################
# Firstly, import all the standard Python modules we need for
# this process

import os, dircache
from configobj import ConfigObj, Section

# Load the local classes
from rapuma.core.tools import *
from rapuma.component.component import Component


###############################################################################
################################## Begin Class ################################
###############################################################################

# As we load the module we will bring in all the common information about all the
# components this type will handle.



class Usfm (Component) :
    '''This class contains information about a type of component 
    used in a type of project.'''

    # Shared values
    xmlConfFile     = 'usfm.xml'

    def __init__(self, project, cfg) :
        super(Usfm, self).__init__(project, cfg)

        # Set values for this manager
        self.project                = project
        self.cName                  = ''
        self.cfg                    = cfg
        self.cType                  = 'usfm'
        self.Ctype                  = self.cType.capitalize()
        self.mType                  = self.project.projectMediaIDCode
        self.rapumaXmlCompConfig    = os.path.join(self.project.local.rapumaConfigFolder, self.xmlConfFile)
        self.sourcePath             = getattr(self.project, self.cType + '_sourcePath')
        self.renderer               = self.project.projConfig['CompTypes'][self.Ctype]['renderer']
        self.adjustmentConfFile     = self.project.local.adjustmentConfFile
        # Get the comp settings
#        self.project.addComponentType(self.Ctype)
        self.compSettings = self.project.projConfig['CompTypes'][self.Ctype]

        # Get persistant values from the config if there are any
        newSectionSettings = getPersistantSettings(self.project.projConfig['CompTypes'][self.Ctype], self.rapumaXmlCompConfig)
        if newSectionSettings != self.project.projConfig['CompTypes'][self.Ctype] :
            self.project.projConfig['CompTypes'][self.Ctype] = newSectionSettings

        for k, v in self.compSettings.iteritems() :
            setattr(self, k, v)

        self.usfmManagers = ['text', 'style', 'font', 'layout', 'hyphenation', 'illustration', self.renderer]
#        self.usfmManagers = ['text', 'style', 'font', 'layout', 'illustration', self.renderer]

        # Init the general managers
        for mType in self.usfmManagers :
            self.project.createManager(self.cType, mType)

        # Pick up some init settings that come after the managers have been installed
        self.macroPackage           = self.project.projConfig['Managers'][self.cType + '_' + self.renderer.capitalize()]['macroPackage']
        self.layoutConfig           = self.project.managers[self.cType + '_Layout'].layoutConfig
        if not os.path.isfile(self.adjustmentConfFile) :
            self.createProjAdjustmentConfFile(self.cType)
        self.adjustmentConfig       = ConfigObj(self.adjustmentConfFile, encoding='utf-8')

        # Check if there is a font installed
        self.project.createManager(self.cType, 'font')
        if not self.project.managers[self.cType + '_Font'].varifyFont() :
            # If a PT project, use that font, otherwise, install default
            if self.sourceEditor.lower() == 'paratext' :
                font = self.project.projConfig['Managers'][self.cType + '_Font']['ptDefaultFont']
            else :
                font = 'DefaultFont'

            self.project.managers[self.cType + '_Font'].installFont(font)

        # To better facilitate rendering that might be happening on this run, we
        # will update source file names and other settings used in the usfm_Text
        # manager (It might be better to do this elsewhere, but where?)
        self.project.managers[self.cType + '_Text'].updateManagerSettings()


###############################################################################
############################ Functions Begin Here #############################
###############################################################################

    def getCidPath (self, cid) :
        '''Return the full path of the cName working text file. This assumes
        the cName is valid.'''

        cName = self.getRapumaCName(cid)
        cType = self.project.projConfig['Components'][cName]['type']
        return os.path.join(self.project.local.projComponentsFolder, cName, cid + '.' + cType)


    def getCidAdjPath (self, cid) :
        '''Return the full path of the cName working text adjustments file. 
        This assumes the cName is valid.'''

        cName = self.getRapumaCName(cid)
        cType = self.project.projConfig['Components'][cName]['type']
        return os.path.join(self.project.local.projComponentsFolder, cName, cid + '.adj')


    def getCidPiclistPath (self, cid) :
        '''Return the full path of the cName working text illustrations file. 
        This assumes the cName is valid.'''

        cName = self.getRapumaCName(cid)
        cType = self.project.projConfig['Components'][cName]['type']
        return os.path.join(self.project.local.projComponentsFolder, cName, cid + '.piclist')


    def render(self, force) :
        '''Does USFM specific rendering of a USFM component'''
            # useful variables: self.project, self.cfg

        self.cidList = self.cfg['cidList']

#        import pdb; pdb.set_trace()

        # Preprocess all subcomponents (one or more)
        # Stop if it breaks at any point
        for cid in self.cidList :
            cName = self.getRapumaCName(cid)
            if not self.preProcessComponent(cName) :
                return False

        # With everything in place we can render the component and we pass-through
        # the force (render/view) command so the renderer will do the right thing.
        self.project.managers['usfm_' + self.renderer.capitalize()].run(force)

        return True


    def preProcessComponent (self, cName) :
        '''This will prepare a component for rendering by checking for
        and/or creating any dependents it needs to render properly.'''

        # Get some relevant settings
        useHyphenation          = str2bool(self.project.managers[self.cType + '_Layout'].layoutConfig['Hyphenation']['useHyphenation'])
        useWatermark            = str2bool(self.project.managers[self.cType + '_Layout'].layoutConfig['PageLayout']['useWatermark'])
        useLines                = str2bool(self.project.managers[self.cType + '_Layout'].layoutConfig['PageLayout']['useLines'])
        usePageBorder           = str2bool(self.project.managers[self.cType + '_Layout'].layoutConfig['PageLayout']['usePageBorder'])
        useIllustrations        = str2bool(self.project.managers[self.cType + '_Layout'].layoutConfig['Illustrations']['useIllustrations'])
        useManualAdjustments    = str2bool(self.project.projConfig['CompTypes'][self.Ctype]['useManualAdjustments'])

        # First see if this is a valid component. This is a little
        # redundant as this is done in project.py as well. It should
        # be caught there first but just in case we'll do it here too.
        if not self.hasCNameEntry(cName) :
            self.project.log.writeToLog('COMP-010', [cName])
            return False
        else :
            # See if the working text is present for each subcomponent in the
            # component and try to install it if it is not
            for cid in self.project.projConfig['Components'][cName]['cidList'] :
                cidCName = self.getRapumaCName(cid)
                cType = self.project.projConfig['Components'][cidCName]['type']
                cidUsfm = self.getCidPath(cid)
                # Build a component object for this cid (cidCName)
                self.project.buildComponentObject(self.cType, cidCName)
                # Create the working text
                if not os.path.isfile(cidUsfm) :
                    self.project.managers[self.cType + '_Text'].installUsfmWorkingText(cName, cid)
                # Add/manage the dependent files for this cid
                if self.macroPackage == 'usfmTex' :
                    # Component adjustment file
                    if useManualAdjustments :
                        self.createProjAdjustmentConfFile(cType, cid)
                        cidAdjFile = self.getCidAdjPath(cid)
                        if isOlder(cidAdjFile, self.adjustmentConfFile) or not os.path.isfile(cidAdjFile) :
                            # Remake the adjustment file
                            if not self.createCompAdjustmentFile(cid) :
                                # If no adjustments, remove any exsiting file
                                if os.path.isfile(cidAdjFile) :
                                    os.remove(cidAdjFile)
                    # Component piclist file
                    self.project.buildComponentObject(self.cType, cidCName)
                    cidPiclist = self.project.components[cidCName].getCidPiclistPath(cid)
                    if useIllustrations :
#                        import pdb; pdb.set_trace()
                        if self.project.managers[cType + '_Illustration'].hasIllustrations(cidCName) :
                            if not os.path.isfile(cidPiclist) :
                                # First check if we have the illustrations we think we need
                                # and get them if we do not.
                                self.project.managers[cType + '_Illustration'].getPics(cid)
                                # Now make a fresh version of the piclist file
                                self.project.managers[cType + '_Illustration'].createPiclistFile(cName, cid)
                                self.project.log.writeToLog('ILUS-065', [cid])
                            else :
                                for f in [self.project.local.layoutConfFile, self.project.local.illustrationConfFile] :
                                    if isOlder(cidPiclist, f) or not os.path.isfile(cidPiclist) :
                                        # Remake the piclist file
                                        self.project.managers[cType + '_Illustration'].createPiclistFile(cName, cid)
                                        self.project.log.writeToLog('ILUS-065', [cid])
                            # Do a quick check to see if the illustration files for this book
                            # are in the project. If it isn't, the run will be killed
                            self.project.managers[cType + '_Illustration'].getPics(cid)
                        else :
                            # Do a little clean up and remove the auto-generated piclist file
                            if os.path.isfile(cidPiclist) :
                                os.remove(cidPiclist)
                            
                    else :
                        # If we are not using illustrations then any existing piclist file will be removed
                        if os.path.isfile(cidPiclist) :
                            os.remove(cidPiclist)
                            self.project.log.writeToLog('ILUS-055', [cName])
                else :
                    self.project.log.writeToLog('COMP-220', [self.macroPackage])

            # FIXME: This may not be needed here as it is called during the setup file checks
            # Check to see if everything is good with hyphenation, die if it is not
#            if not self.project.managers[cType + '_Xetex'].checkDepHyphenFile() :
#                dieNow('Cannot continue. Hyphenation dependencies failed during check in usfm.py preProcessComponent()')

            # Be sure there is a watermark file listed in the conf and
            # installed if watermark is turned on (True). Fallback on the
            # the default if needed.
            if useWatermark :
                if not self.project.managers[cType + '_Illustration'].hasBackgroundFile('watermark') :
                    self.project.managers[cType + '_Illustration'].installBackgroundFile('watermark', 'watermark_default.pdf', self.project.local.rapumaIllustrationsFolder, True)

            # Same for lines background file used for composition
            if useLines :
                if not self.project.managers[cType + '_Illustration'].hasBackgroundFile('lines') :
                    self.project.managers[cType + '_Illustration'].installBackgroundFile('lines', 'lines_default.pdf', self.project.local.rapumaIllustrationsFolder, True)

            # Any more stuff to run?

        return True


    def hasAdjustments (self, cType, cid) :
        '''Check for exsiting adjustments under a book section in
        the adjustment.conf file. Return True if found.'''

        try :
            if self.adjustmentConfig[cType.upper() + ':' + cid.upper()].keys() :
                return True
        except  :
            return False


    def createCompAdjustmentFile (self, cid) :
        '''Create an adjustment file for this cid. If entries exsist in
        the adjustment.conf file.'''

#        import pdb; pdb.set_trace()



        cType = self.getComponentType(self.getRapumaCName(cid))
        if self.hasAdjustments(cType, cid) :
            # Check for a master adj conf file
            if os.path.isfile(self.adjustmentConfFile) :
                adjFile = self.getCidAdjPath(cid)
                for c in self.adjustmentConfig.keys() :
                    try :
                        if c == 'GeneralSettings' :
                            continue
                        if c.lower().split(':')[0] != 'usfm' :
                            continue
                        comp = c.lower().split(':')[1]
                    except Exception as e :
                        # If this doesn't work, we should probably quite here
                        dieNow('Error: Malformed component ID [' + c + '] in adjustment file: ' + str(e) + '\n')
                    if  comp == cid and len(self.adjustmentConfig[c].keys()) > 0 :
                        with codecs.open(adjFile, "w", encoding='utf_8') as writeObject :
                            writeObject.write('% Auto-generated text adjustments file for: ' + cid + '\n')
                            writeObject.write('% Do not edit. To make adjustments refer to: ' + fName(self.project.local.adjustmentConfFile) + ' \n\n')
                            # Output like this: JAS 1.13 +1
                            for k, v in self.adjustmentConfig[c].iteritems() :
                                adj = v
                                if int(v) > 0 : 
                                    adj = '+' + str(v)
                                writeObject.write(comp.upper() + ' ' + k + ' ' + adj + '\n')

                            self.project.log.writeToLog('COMP-230', [fName(adjFile)])
                return True
            else :
                self.createProjAdjustmentConfFile(cType, cid)


    def createProjAdjustmentConfFile (self, cType, cid = None) :
        '''Create a project master component adjustment file that cid piclist
        files will be created from. This will run every time preprocess is
        run but after the first time it will only add a section for the current
        cid that is being run.'''

        adjustmentConfFile = self.project.local.adjustmentConfFile
        if not os.path.isfile(adjustmentConfFile) :
            with codecs.open(adjustmentConfFile, "w", encoding='utf_8') as writeObject :
                writeObject.write('# This is the master manual adjustment file for the ' + cType.capitalize() + ' component type.\n')
                writeObject.write('# Adjustments are layed out in a section/key/value arrangment as follows:\n')
                writeObject.write('# \t[CTYPE:COMPONENT]\n')
                writeObject.write('# \t\t3.4 = 1\n')
                writeObject.write('# \t\t5.8 = 2\n')
                writeObject.write('# \t\t8.3 = -1\n')
                writeObject.write('# Whereas CTYPE is the component type code (upper case) and \n')
                writeObject.write('# COMPONENT is the component the adjustments to follow are for.\n')
                writeObject.write('# Key is the chapter and verse and value is the number of lines\n')
                writeObject.write('# to be added or removed from a specified paragraph.\n\n\n')
        # Now add a section for a cid if needed
        if not cid :
            return
        if not self.adjustmentConfig :
            self.adjustmentConfig = ConfigObj(self.adjustmentConfFile, encoding='utf-8')

        section = cType.upper() + ':' + cid.upper()
        if section not in self.adjustmentConfig.keys() :
            buildConfSection(self.adjustmentConfig, section)
#            self.adjustmentConfig[section]['#1.1'] = 1
            writeConfFile(self.adjustmentConfig)

        self.project.log.writeToLog('COMP-240', [fName(adjustmentConfFile)])


###############################################################################
########################## USFM Component Functions ###########################
###############################################################################


    def logFigure (self, cid, figConts) :
        '''Log the figure data in the illustration.conf. If nothing is returned, the
        existing \fig markers with their contents will be removed. That is the default
        behavior.'''

        # Description of figKeys (in order found in \fig)
            # description = A brief description of what the illustration is about
            # file = The file name of the illustration (only the file name)
            # caption = The caption that will be used with the illustration (if turned on)
            # width = The width or span the illustration will have (span/col)
            # location = Location information that could be printed in the caption reference
            # copyright = Copyright information for the illustration
            # reference = The book ID (upper-case) plus the chapter and verse (eg. MAT 8:23)

        fig = figConts.group(1).split('|')
        figKeys = ['description', 'fileName', 'width', 'location', 'copyright', 'caption', 'reference']
        figDict = {}
        cvSep = self.layoutConfig['Illustrations']['chapterVerseSeperator']

        # Add all the figure info to the dictionary
        c = 0
        for value in fig :
            figDict[figKeys[c]] = value
            c +=1

        # Add additional information, get rid of stuff we don't need
        figDict['illustrationID'] = figDict['fileName'].split('.')[0]
        figDict['useThisIllustration'] = True
        figDict['useThisCaptionRef'] = True
        figDict['bid'] = cid.lower()
        figDict['chapter'] = re.sub(ur'[A-Z]+\s([0-9]+)[.:][0-9]+', ur'\1', figDict['reference'].upper())
        figDict['verse'] = re.sub(ur'[A-Z]+\s[0-9]+[.:]([0-9]+)', ur'\1', figDict['reference'].upper())
        figDict['scale'] = '1.0'
        if figDict['width'] == 'col' :
            figDict['position'] = 'tl'
        else :
            figDict['position'] = 't'
        if not figDict['location'] :
            figDict['location'] = figDict['chapter'] + cvSep + figDict['verse']

        illustrationConfig = self.project.managers[self.cType + '_Illustration'].illustrationConfig
        if not testForSetting(illustrationConfig, 'Illustrations') :
            buildConfSection(illustrationConfig, 'Illustrations')
        # Put the dictionary info into the illustration conf file
        if not testForSetting(illustrationConfig['Illustrations'], figDict['illustrationID'].upper()) :
            buildConfSection(illustrationConfig['Illustrations'], figDict['illustrationID'].upper())
        for k in figDict.keys() :
            illustrationConfig['Illustrations'][figDict['illustrationID'].upper()][k] = figDict[k]

        # Write out the conf file to preserve the data found
        writeConfFile(illustrationConfig)

        # Just incase we need to keep the fig markers intact this will
        # allow for that. However, default behavior is to strip them
        # because usfmTex does not handle \fig markers. By returning
        # them here, they will not be removed from the working text.
        if str2bool(self.project.projConfig['Managers'][self.cType + '_Illustration']['preserveUsfmFigData']) :
            return '\\fig ' + figConts.group(1) + '\\fig*'


    def getComponentType (self, cName) :
        '''Return the cType for a component.'''

        try :
            cType = self.project.projConfig['Components'][cName]['type']
        except Exception as e :
            # If we don't succeed, we should probably quite here
            self.log.writeToLog('COMP-200', ['Key not found ' + str(e)])
            dieNow()

        return cType


    def isCompleteComponent (self, cName) :
        '''A two-part test to see if a component has a config entry and a file.'''

        if self.hasCNameEntry(cName) :
            for cid in self.getSubcomponentList(cName) :
                cidName = self.getRapumaCName(cid)
                cType = self.getComponentType(cidName)
                # For subcomponents look for working text
                if not self.hasCidFile(cidName, cid, cType) :
                    return False
        else :
            return False

        return True


    def hasCNameEntry (self, cName) :
        '''Check for a config component entry.'''

        buildConfSection(self.project.projConfig, 'Components')

        if testForSetting(self.project.projConfig['Components'], cName) :
            return True


    def hasUsfmCidInfo (self, cid) :
        '''Return True if this cid is in the PT USFM cid info dictionary.'''

        if cid in self.usfmCidInfo().keys() :
            return True


    def hasCidFile (self, cName, cid, cType) :
        '''Return True or False depending on if a working file exists 
        for a given cName.'''

        return os.path.isfile(os.path.join(self.project.local.projComponentsFolder, cName, cid + '.' + cType))


    def getUsfmCidInfo (self, cid) :
        '''Return a list of info about a specific cid used in the PT context.'''

        try :
            return self.usfmCidInfo()[cid]
        except :
            return False


    def getUsfmName (self, cid) :
        '''Look up and return the actual name for a valid cid.'''

        if self.hasUsfmCidInfo(cid) :
            return self.getUsfmCidInfo(cid)[0]


    def getRapumaCName (self, cid) :
        '''Look up and return the Rapuma component name for a valid cid.
        But if the cid happens to be a cName already, that will be returned.'''

        if self.hasUsfmCidInfo(cid) :
            return self.getUsfmCidInfo(cid)[1]
        else :
            # FIXME: This seems a little weak. What if the cid is an invalid cName?
            return cid


    def getUsfmCid (self, cName) :
        '''Find the cid by using the cName to look.'''

        info = self.usfmCidInfo()
        for k, v in info.iteritems() :
            if info[k][1] == cName :
                return k


    def getSubcomponentList (self, cName) :
        '''Return the list of subcomponents for a cName.'''

        try :
            cidList = self.project.projConfig['Components'][cName]['cidList']
        except Exception as e :
            # If we don't succeed, we should probably quite here
            self.log.writeToLog('COMP-200', ['Key not found ' + str(e)])
            dieNow()

        return cidList


    def usfmCidInfo (self) :
        '''Return a dictionary of all valid information about USFMs used in PT.'''

    #            ID     Comp Name                               Comp ID                         PT ID
        return {
                'gen' : ['Genesis',                             'genesis',                      '01'],
                'exo' : ['Exodus',                              'exodus',                       '02'], 
                'lev' : ['Leviticus',                           'leviticus',                    '03'], 
                'num' : ['Numbers',                             'numbers',                      '04'], 
                'deu' : ['Deuteronomy',                         'deuteronomy',                  '05'], 
                'jos' : ['Joshua',                              'joshua',                       '06'], 
                'jdg' : ['Judges',                              'judges',                       '07'], 
                'rut' : ['Ruth',                                'ruth',                         '08'], 
                '1sa' : ['1 Samuel',                            '1_samuel',                     '09'], 
                '2sa' : ['2 Samuel',                            '2_samuel',                     '10'], 
                '1ki' : ['1 Kings',                             '1_kings',                      '11'], 
                '2ki' : ['2 Kings',                             '2_kings',                      '12'], 
                '1ch' : ['1 Chronicles',                        '1_chronicles',                 '13'], 
                '2ch' : ['2 Chronicles',                        '2_chronicles',                 '14'], 
                'ezr' : ['Ezra',                                'ezra',                         '15'], 
                'neh' : ['Nehemiah',                            'nehemiah',                     '16'], 
                'est' : ['Esther',                              'esther',                       '17'], 
                'job' : ['Job',                                 'job',                          '18'], 
                'psa' : ['Psalms',                              'psalms',                       '19'], 
                'pro' : ['Proverbs',                            'proverbs',                     '20'], 
                'ecc' : ['Ecclesiastes',                        'ecclesiastes',                 '21'], 
                'sng' : ['Song of Songs',                       'song_of_songs',                '22'], 
                'isa' : ['Isaiah',                              'isaiah',                       '23'], 
                'jer' : ['Jeremiah',                            'jeremiah',                     '24'], 
                'lam' : ['Lamentations',                        'lamentations',                 '25'], 
                'ezk' : ['Ezekiel',                             'ezekiel',                      '26'], 
                'dan' : ['Daniel',                              'daniel',                       '27'], 
                'hos' : ['Hosea',                               'hosea',                        '28'], 
                'jol' : ['Joel',                                'joel',                         '29'], 
                'amo' : ['Amos',                                'amos',                         '30'], 
                'oba' : ['Obadiah',                             'obadiah',                      '31'], 
                'jon' : ['Jonah',                               'jonah',                        '32'], 
                'mic' : ['Micah',                               'micah',                        '33'], 
                'nam' : ['Nahum',                               'nahum',                        '34'], 
                'hab' : ['Habakkuk',                            'habakkuk',                     '35'], 
                'zep' : ['Zephaniah',                           'zephaniah',                    '36'], 
                'hag' : ['Haggai',                              'haggai',                       '37'], 
                'zec' : ['Zechariah',                           'zechariah',                    '38'], 
                'mal' : ['Malachi',                             'malachi',                      '39'],
                'mat' : ['Matthew',                             'matthew',                      '41'], 
                'mrk' : ['Mark',                                'mark',                         '42'], 
                'luk' : ['Luke',                                'luke',                         '43'], 
                'jhn' : ['John',                                'john',                         '44'], 
                'act' : ['Acts',                                'acts',                         '45'], 
                'rom' : ['Romans',                              'romans',                       '46'], 
                '1co' : ['1 Corinthians',                       '1_corinthians',                '47'], 
                '2co' : ['2 Corinthians',                       '2_corinthians',                '48'], 
                'gal' : ['Galatians',                           'galatians',                    '49'], 
                'eph' : ['Ephesians',                           'ephesians',                    '50'], 
                'php' : ['Philippians',                         'philippians',                  '51'], 
                'col' : ['Colossians',                          'colossians',                   '52'], 
                '1th' : ['1 Thessalonians',                     '1_thessalonians',              '53'], 
                '2th' : ['2 Thessalonians',                     '2_thessalonians',              '54'], 
                '1ti' : ['1 Timothy',                           '1_timothy',                    '55'], 
                '2ti' : ['2 Timothy',                           '2_timothy',                    '56'], 
                'tit' : ['Titus',                               'titus',                        '57'], 
                'phm' : ['Philemon',                            'philemon',                     '58'], 
                'heb' : ['Hebrews',                             'hebrews',                      '59'], 
                'jas' : ['James',                               'james',                        '60'], 
                '1pe' : ['1 Peter',                             '1_peter',                      '61'], 
                '2pe' : ['2 Peter',                             '2_peter',                      '62'], 
                '1jn' : ['1 John',                              '1_john',                       '63'], 
                '2jn' : ['2 John',                              '2_john',                       '64'], 
                '3jn' : ['3 John',                              '3_john',                       '65'], 
                'jud' : ['Jude',                                'jude',                         '66'], 
                'rev' : ['Revelation',                          'revelation',                   '67'], 
                'tob' : ['Tobit',                               'tobit',                        '68'], 
                'jdt' : ['Judith',                              'judith',                       '69'], 
                'esg' : ['Esther',                              'esther',                       '70'], 
                'wis' : ['Wisdom of Solomon',                   'wisdom_of_solomon',            '71'], 
                'sir' : ['Sirach',                              'sirach',                       '72'], 
                'bar' : ['Baruch',                              'baruch',                       '73'], 
                'lje' : ['Letter of Jeremiah',                  'letter_of_jeremiah',           '74'], 
                's3y' : ['Song of the Three Children',          'song_3_children',              '75'], 
                'sus' : ['Susanna',                             'susanna',                      '76'], 
                'bel' : ['Bel and the Dragon',                  'bel_dragon',                   '77'], 
                '1ma' : ['1 Maccabees',                         '1_maccabees',                  '78'], 
                '2ma' : ['2 Maccabees',                         '2_maccabees',                  '79'], 
                '3ma' : ['3 Maccabees',                         '3_maccabees',                  '80'], 
                '4ma' : ['4 Maccabees',                         '4_maccabees',                  '81'], 
                '1es' : ['1 Esdras',                            '1_esdras',                     '82'], 
                '2es' : ['2 Esdras',                            '2_esdras',                     '83'], 
                'man' : ['Prayer of Manasses',                  'prayer_of_manasses',           '84'], 
                'ps2' : ['Psalms 151',                          'psalms_151',                   '85'], 
                'oda' : ['Odae',                                'odae',                         '86'], 
                'pss' : ['Psalms of Solomon',                   'psalms_of_solomon',            '87'], 
                'jsa' : ['Joshua A',                            'joshua_a',                     '88'], 
                'jdb' : ['Joshua B',                            'joshua_b',                     '89'], 
                'tbs' : ['Tobit S',                             'tobit_s',                      '90'], 
                'sst' : ['Susannah (Theodotion)',               'susannah_t',                   '91'], 
                'dnt' : ['Daniel (Theodotion)',                 'daniel_t',                     '92'], 
                'blt' : ['Bel and the Dragon (Theodotion)',     'bel_dragon_t',                 '93'], 
                'frt' : ['Front Matter',                        'front_matter',                 'A0'], 
                'int' : ['Introductions',                       'introductions',                'A7'], 
                'bak' : ['Back Matter',                         'back_matter',                  'A1'], 
                'cnc' : ['Concordance',                         'concordance',                  'A8'], 
                'glo' : ['Glossary',                            'glossary',                     'A9'], 
                'tdx' : ['Topical Index',                       'topical_index',                'B0'], 
                'ndx' : ['Names Index',                         'names_index',                  'B1'], 
                'xxa' : ['Extra A',                             'extra_a',                      '94'], 
                'xxb' : ['Extra B',                             'extra_b',                      '95'], 
                'xxc' : ['Extra C',                             'extra_c',                      '96'], 
                'xxd' : ['Extra D',                             'extra_d',                      '97'],
                'xxe' : ['Extra E',                             'extra_e',                      '98'], 
                'xxf' : ['Extra F',                             'extra_f',                      '99'], 
                'xxg' : ['Extra G',                             'extra_g',                      '100'], 
                'oth' : ['Other',                               'other',                        'A2'], 
                'eza' : ['Apocalypse of Ezra',                  'apocalypse_of_ezra',           'A4'], 
                '5ez' : ['5 Ezra',                              '5_ezra_lp',                    'A5'], 
                '6ez' : ['6 Ezra (Latin Epilogue)',             '6_ezra_lp',                    'A6'], 
                'dag' : ['Daniel Greek',                        'daniel_greek',                 'B2'], 
                'ps3' : ['Psalms 152-155',                      'psalms_152-155',               'B3'], 
                '2ba' : ['2 Baruch (Apocalypse)',               '2_baruch_apocalypse',          'B4'], 
                'lba' : ['Letter of Baruch',                    'letter_of_baruch',             'B5'], 
                'jub' : ['Jubilees',                            'jubilees',                     'B6'], 
                'eno' : ['Enoch',                               'enoch',                        'B7'], 
                '1mq' : ['1 Meqabyan',                          '1_meqabyan',                   'B8'], 
                '2mq' : ['2 Meqabyan',                          '2_meqabyan',                   'B9'], 
                '3mq' : ['3 Meqabyan',                          '3_meqabyan',                   'C0'], 
                'rep' : ['Reproof (Proverbs 25-31)',            'reproof_proverbs_25-31',       'C1'], 
                '4ba' : ['4 Baruch (Rest of Baruch)',           '4_baruch',                     'C2'], 
                'lao' : ['Laodiceans',                          'laodiceans',                   'C3'] 
               }








###############################################################################
###############################################################################
########################## ParaTExt Class Functions ###########################
###############################################################################
###############################################################################

class PT_Tools (Component) :
    '''This class contains functions for working with USFM data in ParaTExt.'''

    def __init__(self, project) :

        self.project = project



    def getPTHyphenWordList (self) :
        '''Return a list of hyphenated words found in a ParaTExt project
        hyphated words text file.'''

        # Note: it is a given that the cType is usfm
        projectIDCode = self.project.projConfig['ProjectInfo']['projectIDCode']
        usfm_sourcePath = self.project.userConfig['Projects'][projectIDCode]['usfm_sourcePath']
        ptHyphenFileName = self.project.projConfig['Managers']['usfm_Hyphenation']['ptHyphenFileName']
        ptHyphenFile = os.path.join(usfm_sourcePath, ptHyphenFileName)
        wordList = []
        
        # Go get the file if it is to be had
        if os.path.isfile(ptHyphenFile) :
            with codecs.open(ptHyphenFile, "r", encoding='utf_8') as hyphenWords :
                for line in hyphenWords :
                    # Using the logic that there can only be one word in a line
                    # if the line contains more than one word it is not wanted
                    word = line.split()
                    if len(word) == 1 :
                        wordList.append(word[0])
            return wordList
        else :
            return False


    def ptToTexHyphenWordList (self, wordList) :
        '''Convert a hyphenated word list from PT to a TeX type word list.'''

        # The ptHyphenImportRegEx will come in in a 2 element list
        ptHyphenImportRegEx = self.project.projConfig['Managers']['usfm_Hyphenation']['ptHyphenImportRegEx']
        advancedHyphenImportRegEx = self.project.projConfig['Managers']['usfm_Hyphenation']['advancedHyphenImportRegEx']
        search = ptHyphenImportRegEx[0]
        replace = ptHyphenImportRegEx[1]
        texWordList = []
        for word in wordList :
            tWord = re.sub(ptHyphenImportRegEx[0], ptHyphenImportRegEx[1], word)
            # In case we want to do more...
            if advancedHyphenImportRegEx :
                tWord = re.sub(advancedHyphenImportRegEx[0], advancedHyphenImportRegEx[1], tWord)
            texWordList.append(tWord)

        if len(texWordList) > 0 :
            return texWordList
        else :
            return False







    def formPTName (self, cName, cid) :
        '''Using valid PT project settings from the project configuration, form
        a valid PT file name that can be used for a number of operations.'''

        # FIXME: Currently very simplistic, will need to be more refined for
        #           number of use cases.

        try :
            nameFormID = self.project.projConfig['Managers']['usfm_Text']['nameFormID']
            postPart = self.project.projConfig['Managers']['usfm_Text']['postPart']
            prePart = self.project.projConfig['Managers']['usfm_Text']['prePart']

            if nameFormID == '41MAT' :
                mainName = self.project.components[cName].getUsfmCidInfo(cid)[2] + cid.upper()
                if prePart and prePart != 'None' :
                    thisFile = prePart + mainName + postPart
                else :
                    thisFile = mainName + postPart
            return thisFile
        except :
            return False


    def formGenericName (self, cid) :
        '''Figure out the best way to form a valid file name given the
        source is not coming from a PT project.'''

    # FIXME: This will be expanded as we find more use cases

        postPart = self.project.projConfig['Managers']['usfm_Text']['postPart']
        return cid + '.' + postPart


    def getPTFont (self, sourcePath) :
        '''Just return the name of the font used in a PT project.'''

        ssf = self.getPTSettings(sourcePath)
        return ssf['ScriptureText']['DefaultFont']


    def mapPTTextSettings (self, sysSet, ptSet, force=False) :
        '''Map the text settings from a PT project SSF file into the text
        manager's settings. If no setting is present in the config, add
        what is in the PT SSF. If force is True, replace any exsisting
        settings.'''

        # A PT to Rapuma text mapping dictionary
        mapping   = {
                    'FileNameBookNameForm'      : 'nameFormID',
                    'FileNameForm'              : 'nameFormID',
                    'FileNamePrePart'           : 'prePart',
                    'FileNamePostPart'          : 'postPart',
                    'DefaultFont'               : 'ptDefaultFont'
                    }

        # Loop through all the PT settings and check against the mapping
        for k in mapping.keys() :
            try :
                if sysSet[mapping[k]] == '' or sysSet[mapping[k]] == 'None' :
                    # This is for getting rid of "None" settings in the config
                    if not ptSet['ScriptureText'][k] :
                        sysSet[mapping[k]] = ''
                    else :
                        sysSet[mapping[k]] = ptSet['ScriptureText'][k]
                elif force :
                    sysSet[mapping[k]] = ptSet['ScriptureText'][k]
            except :
                pass

        return sysSet


    def findSsfFile (self, sourcePath) :
        '''Look for the ParaTExt project settings file. The immediat PT project
        is the parent folder and the PT environment that the PT projet is found
        in, if any, is the grandparent folder. the .ssf (settings) file in the
        grandparent folder takes presidence over the one found in the parent folder.
        This function will determine where the primary .ssf file is and return the
        .ssf path/file and the PT path. If not found, return None.'''

        # Not sure where the PT SSF file might be or even what its name is.
        # Starting in parent, we should find the first .ssf file. That will
        # give us the name of the file. Then we will look in the grandparent
        # folder and if we find the same named file there, that will be
        # harvested for the settings. Otherwise, the settings will be taken
        # from the parent folder.
        # Note: Starting with PT 7 the "gather" folder was introduced to
        # projects. We will need to look in that folder as well for the 
        # .ssf file.
        ssfFileName = ''
        ptPath = ''
        parentFolder = sourcePath
        grandparentFolder = os.path.dirname(parentFolder)
        gatherFolder = os.path.join(parentFolder, 'gather')

        # For now, we will assume that if there is a gather folder, it must have a .ssf file in it
        if os.path.isdir(gatherFolder) :
            parentFolder = gatherFolder
        # Get a file list from the parent folder and look for a .ssf/.SSF file
        # This assumes there is (has to be) only one ssf/SSF file in the folder.
        # The main problem at this point is we don't really know the name of
        # the file, only the extention.
        parentFileList = dircache.listdir(parentFolder)
        grandparentFileList = dircache.listdir(grandparentFolder)

        # Parent first to find the actual settings file name. Right now, there
        # can only be 2 possibilities, either ssf or SSF. (No one in their right
        # mind would ever use mixed case on an extention. That would be stupid!)
        for f in parentFileList :
            if os.path.isfile(os.path.join(parentFolder, f)) :
                # Not every file we test has an extention, look first
                if len(f.split('.')) > 1 :
                    if f.split('.')[1] == 'ssf' or f.split('.')[1] == 'SSF' :
                        ssfFileName = f
                        ptPath = parentFolder

        # At this point we need a sanity test. If no ssfFileName is present
        # then there probably isn't one and we should just return False now
        if not ssfFileName :
            return False

        # Now now look in the grandparent folder and change to override settings
        # file if there is one
        for f in grandparentFileList :
            if os.path.isfile(os.path.join(grandparentFolder, f)) :
                ucn = ssfFileName.split('.')[0] + '.' + ssfFileName.split('.')[1].upper()
                lcn = ssfFileName.split('.')[0] + '.' + ssfFileName.split('.')[1].lower()
                if f == (ucn or lcn) :
                    ssfFileName = f
                    ptPath = grandparentFolder

        return os.path.join(ptPath, ssfFileName)


    def getPTSettings (self, sourcePath) :
        '''Return the data into a dictionary for the system to use.'''

        # Return the dictionary
        if os.path.isdir(sourcePath) :
            ssfFile = self.findSsfFile(sourcePath)
            if ssfFile :
                if os.path.isfile(ssfFile) :
                    return xmlFileToDict(ssfFile)


    def getSourceEditor (self, sourcePath, cType) :
        '''Return the sourceEditor if it is set. If not try to
        figure out what it should be and return that. Unless we
        find we are in a PT project, we'll call it generic.'''

    #    import pdb; pdb.set_trace()
        se = 'generic'
        Ctype = cType.capitalize()
        # FIXME: This may need expanding as more use cases arrise
        if testForSetting(self.project.projConfig['CompTypes'][Ctype], 'sourceEditor') :
            se = self.project.projConfig['CompTypes'][Ctype]['sourceEditor']
        else :
            if self.findSsfFile(sourcePath) :
                se = 'paratext'

        return se





