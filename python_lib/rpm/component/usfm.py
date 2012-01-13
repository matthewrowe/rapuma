#!/usr/bin/python
# -*- coding: utf_8 -*-
# version: 20111207
# By Dennis Drescher (dennis_drescher at sil.org)

###############################################################################
######################### Description/Documentation ###########################
###############################################################################

# This class will handle book project tasks.

# History:
# 20111222 - djd - Started with intial file


###############################################################################
################################# Project Class ###############################
###############################################################################
# Firstly, import all the standard Python modules we need for
# this process

import os
from pprint import pprint


# Load the local classes
from tools import *
from component import Component


###############################################################################
################################## Begin Class ################################
###############################################################################

# As we load the module we will bring in all the common information about all the
# components this type will handle.

# All valid USFM IDs
compIDs = {
            'gen' : ['Genesis', '01'], 'exo' : ['Exodus', '02'], 'lev' : ['Leviticus', '03'], 'num' : ['Numbers', '04'], 
            'deu' : ['Deuteronomy', '05'], 'jos' : ['Joshua', '06'], 'jdg' : ['Judges', '07'], 'rut' : ['Ruth', '08'], 
            '1sa' : ['1 Samuel', '09'], '2sa' : ['2 Samuel', '10'], '1ki' : ['1 Kings', '11'], '2ki' : ['2 Kings', '12'], 
            '1ch' : ['1 Chronicles', '13'], '2ch' : ['2 Chronicles', '14'], 'ezr' : ['Ezra', '15'], 'neh' : ['Nehemiah', '16'], 
            'est' : ['Esther', '17'], 'job' : ['Job', '18'], 'psa' : ['Psalms', '19'], 'pro' : ['Proverbs', '20'], 'ecc' : ['Ecclesiastes', '21'], 
            'sng' : ['Song of Songs', '22'], 'isa' : ['Isaiah', '23'], 'jer' : ['Jeremiah', '24'], 'lam' : ['Lamentations', '25'], 
            'ezk' : ['Ezekiel', '26'], 'dan' : ['Daniel', '27'], 'hos' : ['Hosea', '28'], 'jol' : ['Joel', '29'], 
            'amo' : ['Amos', '30'], 'oba' : ['Obadiah', '31'], 'jon' : ['Jonah', '32'], 'mic' : ['Micah', '33'], 
            'nam' : ['Nahum', '34'], 'hab' : ['Habakkuk', '35'], 'zep' : ['Zephaniah', '36'], 'hag' : ['Haggai', '37'], 
            'zec' : ['Zechariah', '38'], 'mal' : ['Malachi', '39'],
            'mat' : ['Matthew', '41'], 'mrk' : ['Mark', '42'], 'luk' : ['Luke', '43'], 'jhn' : ['John', '44'], 
            'act' : ['Acts', '45'], 'rom' : ['Romans', '46'], '1co' : ['1 Corinthians', '47'], '2co' : ['2 Corinthians', '48'], 
            'gal' : ['Galatians', '49'], 'eph' : ['Ephesians', '50'], 'php' : ['Philippians', '51'], 'col' : ['Colossians', '52'], 
            '1th' : ['1 Thessalonians', '53'], '2th' : ['2 Thessalonians', '54'], '1ti' : ['1 Timothy', '55'], '2ti' : ['2 Timothy', '56'], 
            'tit' : ['Titus', '57'], 'phm' : ['Philemon', '58'], 'heb' : ['Hebrews', '59'], 'jas' : ['James', '60'], 
            '1pe' : ['1 Peter', '61'], '2pe' : ['2 Peter', '62'], '1jn' : ['1 John', '63'], '2jn' : ['2 John', '64'], 
            '3jn' : ['3 John', '65'], 'jud' : ['Jude', '66'], 'rev' : ['Revelation', '67'], 
            'tob' : ['Tobit', '68'], 'jdt' : ['Judith', '69'], 'esg' : ['Esther', '70'], 'wis' : ['Wisdom of Solomon', '71'], 
            'sir' : ['Sirach', '72'], 'bar' : ['Baruch', '73'], 'lje' : ['Letter of Jeremiah', '74'], 's3y' : ['Song of the Three Children', '75'], 
            'sus' : ['Susanna', '76'], 'bel' : ['Bel and the Dragon', '77'], '1ma' : ['1 Maccabees', '78'], '2ma' : ['2 Maccabees', '79'], 
            '3ma' : ['3 Maccabees', '80'], '4ma' : ['4 Maccabees', '81'], '1es' : ['1 Esdras', '82'], '2es' : ['2 Esdras', '83'], 
            'man' : ['Prayer of Manasses', '84'], 'ps2' : ['Psalms 151', '85'], 'oda' : ['Odae', '86'], 'pss' : ['Psalms of Solomon', '87'], 
            'jsa' : ['Joshua A', '88'], 'jdb' : ['Joshua B', '89'], 'tbs' : ['Tobit S', '90'], 'sst' : ['Susannah (Theodotion)', '91'], 
            'dnt' : ['Daniel (Theodotion)', '92'], 'blt' : ['Bel and the Dragon (Theodotion)', '93'], 
            'frt' : ['Front Matter', 'A0'], 'int' : ['Introductions', 'A7'], 'bak' : ['Back Matter', 'A1'], 
            'cnc' : ['Concordance', 'A8'], 'glo' : ['Glossary', 'A9'], 'tdx' : ['Topical Index', 'B0'], 'ndx' : ['Names Index', 'B1'], 
            'xxa' : ['Extra A', '94'], 'xxb' : ['Extra B', '95'], 'xxc' : ['Extra C', '96'], 'xxd' : ['Extra D', '97'],
            'xxe' : ['Extra E', '98'], 'xxf' : ['Extra F', '99'], 'xxg' : ['Extra G', '100'], 'oth' : ['Other', 'A2'], 
            'eza' : ['Apocalypse of Ezra', 'A4'], '5ez' : ['5 Ezra (Latin Prologue)', 'A5'], '6ez' : ['6 Ezra (Latin Epilogue)', 'A6'], 'dag' : ['Daniel Greek', 'B2'], 
            'ps3' : ['Psalms 152-155', 'B3'], '2ba' : ['2 Baruch (Apocalypse)', 'B4'], 'lba' : ['Letter of Baruch', 'B5'], 'jub' : ['Jubilees', 'B6'], 
            'eno' : ['Enoch', 'B7'], '1mq' : ['1 Meqabyan', 'B8'], '2mq' : ['2 Meqabyan', 'B9'], '3mq' : ['3 Meqabyan', 'C0'], 
            'rep' : ['Reproof (Proverbs 25-31)', 'C1'], '4ba' : ['4 Baruch (Rest of Baruch)', 'C2'], 'lao' : ['Laodiceans', 'C3'] 
          }


class Usfm (Component) :
    '''This class contains information about a type of component 
    used in a type of project.'''

    def __init__(self, project, config) :
        super(Usfm, self).__init__(project, config)

        self.compIDs = compIDs
        self.project = project

        # Get settings from config file (or defaults if they are not there)
        if not testForSetting(self.project._projConfig, 'CompTypes', 'Usfm') :
            compDefaults = getXMLSettings(os.path.join(self.project.rpmConfigFolder, 'usfm.xml'))
            buildConfSection(self.project._projConfig, 'CompTypes')
            buildConfSection(self.project._projConfig['CompTypes'], 'Usfm')
            for k, v, in compDefaults.iteritems() :
                self.project._projConfig['CompTypes']['Usfm'][k] = v

            self.project.writeOutProjConfFile = True

        self.compConfig = self.project._projConfig['CompTypes']['Usfm']
        for k, v in self.compConfig.iteritems() :
            setattr(self, k, v)


#        self.ptProjectInfoFile = os.path.join('gather', getPtId() + '.ssf')
#        self.usfmManagers = [self.renderer, 'source', 'font', 'preprocess', 'style', 'illustration', 'hyphenation']
        self.usfmManagers = ['font']

        # Manager Descrptions
        #    source - Locate component source file, copy or link to project if needed
        #    font - Manage fonts for all component types and renderers
        #    preprocess - Create the process file, do any preprocesses needed
        #    style - Manage element styles
        #    illustration - Manage illustrations for all component types and renderers
        #    hyphenation - Manage hyphenation information for components according to renderer

        # Init the general managers
        for mType in self.usfmManagers :
            self.project.createManager('usfm', mType)


    def render(self) :
        '''Does USFM specific rendering of a USFM component'''
        #useful variables: self.project, self.cfg

        # FIXME: This function, when everything has been prepared
        # by the component managers, will call a specific renderer
        # that will (some how) have access to the other managers
        # A call might look like: xetex.???(param1, param2)


        # Is this a valid component ID for this component type?
        if self.cfg['name'] in self.compIDs :
            terminal("Rendering: " + self.compIDs[self.cfg['name']][0])

        # Check for font elements and information
#        self.project.managers['usfm_Font'].recordFont(self.primaryFont, 'usfm_Font')
        self.project.managers['usfm_Font'].installFont(self.primaryFont, 'usfm_Font')
        # Check to see what kind of renderer we are using and create any supporting
        # font config files needed
        if self.renderer == 'xetex' :
            self.project.managers['usfm_Font'].makeFontInfoTexFile()
        else :
            self.project.writeToLog('ERR', 'The [' + renderer + '] is not supported by RPM at this time')


        # Check for source
        sourceFile = testForSetting(self.cfg, 'sourceFile')
        if not sourceFile :
            pass #sourceFile = howdowecallthesourcemanager?(sourceType)
            






