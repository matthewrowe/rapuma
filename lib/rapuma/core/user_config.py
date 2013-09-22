#!/usr/bin/python
# -*- coding: utf_8 -*-
# version: 20110823
# By Dennis Drescher (dennis_drescher at sil.org)

###############################################################################
######################### Description/Documentation ###########################
###############################################################################

# This class will handle user configuration operations.

###############################################################################
############################# Component Class #################################
###############################################################################
# Firstly, import all the standard Python modules we need for
# this process

import codecs, os, sys, site
from configobj import ConfigObj

# Load the local classes
from rapuma.core.tools          import Tools


class UserConfig (object) :

    def __init__(self) :
        '''Intitate the whole class and create the object.'''

        self.rapumaHome         = os.environ.get('RAPUMA_BASE')
        self.defaultUserHome    = os.environ.get('RAPUMA_USER')
        self.userConfFileName   = 'rapuma.conf'
        self.tools              = Tools()

        # Point to the right user config
        # Look for a web installation first, if not go to default
        # Note that a slash is put before var as it is off of root
        # That kind of stops this from being cross-platform
        rapumaWebConfig         = os.path.join('/var', 'lib', 'rapuma', 'config', self.userConfFileName)
        defaultConfig           = os.path.join(self.defaultUserHome, self.userConfFileName)
        if os.path.exists(rapumaWebConfig) :
            self.userConfFile   = rapumaWebConfig
        else :
            self.userConfFile   = defaultConfig

        # Check to see if the file is there, then read it in and break it into
        # sections. If it fails, scream really loud!
        rapumaXMLDefaults = os.path.join(self.rapumaHome, 'config', 'rapuma.xml')
        if os.path.exists(rapumaXMLDefaults) :
            self.tools.sysXmlConfig = self.tools.xml_to_section(rapumaXMLDefaults)
        else :
            raise IOError, "Can't open " + rapumaXMLDefaults

#        import pdb; pdb.set_trace()

        # Now make the users local rapuma.conf file if it isn't there
        if not os.path.exists(self.userConfFile) :
            self.initUserHome()

        # Load the Rapuma conf file into an object
        self.userConfig = ConfigObj(self.userConfFile, encoding='utf-8')

        # Initialize the user's home folders, like resouces, etc
        self.makeHomeFolders()

        # Look for any projects that might be registered and copy the data out
        try :
            userProjs = self.userConfig['Projects']
        except :
            userProjs = ''

        # Create a new conf object based on all the XML default settings
        # Then override them with any exsiting user settings.
        newConfig = ConfigObj(self.tools.sysXmlConfig.dict(), encoding='utf-8').override(self.userConfig)

        # Put back the copied data of any project information that we might have
        # lost from the XML/conf file merging.
        if userProjs :
            newConfig['Projects'] = userProjs

        # Do not bother writing if nothing has changed
        if not self.userConfig.__eq__(newConfig) :
            self.userConfig = newConfig
            self.userConfig.filename = self.userConfFile
            self.userConfig.write()

        # Log messages for this module
        self.errorCodes     = {
            '0000' : ['MSG', 'Placeholder message'],
        }

###############################################################################
############################ User Config Functions ############################
###############################################################################


    def initUserHome (self) :
        '''Initialize a user config file on a new install or system re-init.'''

        # Create home folders
        if not os.path.isdir(self.defaultUserHome) :
            os.mkdir(self.defaultUserHome)

        # Make the default global rapuma.conf for custom environment settings
        if not os.path.isfile(self.userConfFile) :
            self.userConfig = ConfigObj(encoding='utf-8')
            self.userConfig.filename = self.userConfFile
            self.userConfig['System'] = {}
            self.userConfig['System']['userName'] = 'Default User'
            self.userConfig['System']['initDate'] = self.tools.tStamp()
            self.userConfig.write()


    def isRegisteredProject (self, pid) :
        '''Check to see if this project is recorded in the user's config'''

        try :
            return pid in self.userConfig['Projects']
        except :
            pass


    def registerProject (self, pid, pname, pmid, projHome) :
        '''If it is not there, create an entry in the user's
        rapuma.conf located in the user's config folder.'''

#        import pdb; pdb.set_trace()

        self.tools.buildConfSection(self.userConfig, 'Projects')
        self.tools.buildConfSection(self.userConfig['Projects'], pid)

        # Now add the project data
        self.userConfig['Projects'][pid]['projectName']         = pname
        self.userConfig['Projects'][pid]['projectMediaIDCode']  = pmid
        self.userConfig['Projects'][pid]['projectPath']         = projHome
        self.userConfig['Projects'][pid]['projectCreateDate']   = self.tools.tStamp()

        self.userConfig.write()
        return True


    def unregisterProject (self, pid) :
        '''Remove a project from the user config file.'''
        
#        import pdb; pdb.set_trace()
        
        del self.userConfig['Projects'][pid]
        self.userConfig.write()
        
        # Check to see if we were succeful
        if not self.userConfig['Projects'].has_key(pid) :
            return True


    def setSystemSettings (self, section, key, value) :
        '''Function to make system settings.'''

        oldValue = self.userConfig[section][key]
        if oldValue != value :
            self.userConfig[section][key] = value
            # Write out the results
            self.userConfig.write()
            self.tools.terminal('\nRapuma user name setting changed from [' + oldValue + '] to [' + value + '].\n\n')
        else :
            self.tools.terminal('\nSame value given, nothing to changed.\n\n')


    def makeHomeFolders (self) :
        '''Setup the default Rapuma resource folders.'''

#        import pdb; pdb.set_trace()

        # We do not write out unless this flag is set
        confWriteFlag = False

        # Setup Resources section if needed
        if not self.userConfig.has_key('Resources') :
            self.tools.buildConfSection(self.userConfig, 'Resources')

        # Get the user config project folder location (or set a default)
        if not self.userConfig['Resources'].has_key('projects') :
            self.tools.buildConfSection(self.userConfig['Resources'], 'projects')
        if not self.userConfig['Resources']['projects'] :
            projects = os.path.join(os.environ.get('HOME'), 'Publishing')
            if not os.path.exists(projects) :
                os.makedirs(projects)
                self.userConfig['Resources']['projects'] = projects
                confWriteFlag = True
        elif not os.path.exists(self.tools.resolvePath(self.userConfig['Resources']['projects'])) :
            sys.exit('\nERROR: Invalid projects folder path: ' + self.userConfig['Resources']['projects'] + '\n\nProcess halted.\n')
        else :
            projects = self.tools.resolvePath(self.userConfig['Resources']['projects'])

        # Get the user config Rapuma resouce folder location
        if not self.userConfig['Resources'].has_key('rapumaResouce') :
            self.tools.buildConfSection(self.userConfig['Resources'], 'rapumaResouce')
        if len(self.userConfig['Resources']['rapumaResouce']) > 0 :
            rapumaResouce = self.userConfig['Resources']['rapumaResouce']
        else :
            # This is the default location
            rapumaResouce = os.path.join(site.USER_BASE, 'share', 'rapuma')
            self.userConfig['Resources']['rapumaResouce'] = rapumaResouce
            confWriteFlag = True

        # Make a list of sub-folders to make in the Rapuma resourcs folder
        resourceFolders = ['archive', 'backup', 'font', 'illustration', \
                            'macro','script', 'template']

        for r in resourceFolders :
            # Build the path and check if it can be made
            thisPath = os.path.join(rapumaResouce, r)
            if not os.path.isdir(thisPath) :
                os.makedirs(thisPath)
                self.userConfig['Resources'][r] = thisPath
                confWriteFlag = True

        # Write out if needed
        if confWriteFlag :
            self.userConfig.write()
        return True






