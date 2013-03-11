#!/usr/bin/python
# -*- coding: utf_8 -*-
# version: 20111203
# By Dennis Drescher (dennis_drescher at sil.org)

###############################################################################
######################### Description/Documentation ###########################
###############################################################################

# This class will handle project infrastructure tasks.

# History:
# 20110823 - djd - Started with intial file from Rapuma project
# 20111203 - djd - Begin changing over to new manager model


###############################################################################
################################# Project Class ###############################
###############################################################################
# Firstly, import all the standard Python modules we need for
# this process

import codecs, os, sys, shutil, imp, subprocess, zipfile, StringIO, filecmp, difflib
from configobj import ConfigObj, Section


# Load the local classes
from rapuma.core.tools import *
import rapuma.project.manager as mngr
import rapuma.core.user_config as userConfig
#from rapuma.component.usfm import PT_Tools
from rapuma.group.usfm import PT_Tools
from importlib import import_module

###############################################################################
################################## Begin Class ################################
###############################################################################

class Project (object) :

    def __init__(self, userConfig, projConfig, local, log, systemVersion) :
        '''Instantiate this class.'''

#        import pdb; pdb.set_trace()
#        self.pt_tools               = PT_Tools(self)
        self.local                  = local
        self.userConfig             = userConfig
        self.projConfig             = projConfig
        self.log                    = log
        self.systemVersion          = systemVersion
        self.gid                    = ''
        self.groups                 = {}
#        self.components             = {}
#        self.componentType          = {}
        self.managers               = {}
        self.projectMediaIDCode     = self.projConfig['ProjectInfo']['projectMediaIDCode']
        self.projectIDCode          = self.projConfig['ProjectInfo']['projectIDCode']
        self.projectName            = self.projConfig['ProjectInfo']['projectName']

        # Get component source path(s)
        for cType in self.userConfig['System']['recognizedComponentTypes'] :
            sourcePath = ''
            try :
                sourcePath = userConfig['Projects'][self.projectIDCode][cType + '_sourcePath']
            except Exception as e :
                # If we don't succeed, we should probably quite here
                terminal('No source path found for: [' + str(e) + ']')
                terminal('Please add a source path for this component type.')
#                dieNow()
            if sourcePath :
                setattr(self, cType + '_sourcePath', sourcePath)

        # Do some cleanup like getting rid of the last sessions error log file.
        try :
            if os.path.isfile(self.local.projErrorLogFile) :
                os.remove(self.local.projErrorLogFile)
        except :
            pass

        # Initialize the project type
        # FIXME: some additional work needs to be done to simplify this
        # This will have to do for now.
        
#        import pdb; pdb.set_trace()

        m = import_module('rapuma.project.' + self.projectMediaIDCode)
#       or you could use:
#        m = import_module('..' + self.projectMediaIDCode, mngr.__name__)
        self.__class__ = getattr(m, self.projectMediaIDCode[0].upper() + self.projectMediaIDCode[1:])

        # Update the existing config file with the project type XML file
        # if needed
        newXmlDefaults = os.path.join(self.local.rapumaConfigFolder, self.projectMediaIDCode + '.xml')
        xmlConfig = getXMLSettings(newXmlDefaults)
        newConf = ConfigObj(xmlConfig.dict(), encoding='utf-8').override(self.projConfig)
        for s,v in self.projConfig.items() :
            if s not in newConf :
                newConf[s] = v

        # Replace with new conf if new is different from old
        # Rem new conf doesn't have a filename, give it one
        if self.projConfig != newConf :
            self.projConfig = newConf
            self.projConfig.filename = self.local.projConfFile

        # Up the creatorVersion on the project if needed
        if not testForSetting(self.projConfig, 'ProjectInfo', 'projectCreatorVersion') :
            self.projConfig['ProjectInfo']['projectCreatorVersion'] = self.systemVersion
            writeConfFile(self.projConfig)
        else :
            if self.projConfig['ProjectInfo']['projectCreatorVersion'] != self.systemVersion :
                self.projConfig['ProjectInfo']['projectCreatorVersion'] = self.systemVersion
                writeConfFile(self.projConfig)

        # If this is a valid project we might as well put in the folders
        for folder in self.local.projFolders :
            if not os.path.isdir(getattr(self.local, folder)) :
                os.makedirs(getattr(self.local, folder))

        # Go ahead and set this as the current project
        self.setProjCurrent(self.projectIDCode)

        # Add modules because we have all the "self" needed at this point
        self.pt_tools = PT_Tools(self)

###############################################################################
############################ Manager Level Functions ##########################
###############################################################################

    def createManager (self, cType, mType) :
        '''Check to see if a manager is listed in the config and load it if
        it is not already.'''

        fullName = cType + '_' + mType.capitalize()
        if fullName not in self.managers :
            self.addManager(cType, mType)
            self.loadManager(cType, mType)
            self.log.writeToLog('PROJ-005', [fullName])


    def loadManager (self, cType, mType) :
        '''Do basic load on a manager.'''

#        import pdb; pdb.set_trace()

        fullName = cType + '_' + mType.capitalize()
        cfg = self.projConfig['Managers'][fullName]
        module = import_module('rapuma.manager.' + mType)
        ManagerClass = getattr(module, mType.capitalize())
        manobj = ManagerClass(self, cfg, cType)
        self.managers[fullName] = manobj


    def addManager (self, cType, mType) :
        '''Create a manager reference in the project config that components
        will point to.'''

#        import pdb; pdb.set_trace()

        fullName = cType + '_' + mType.capitalize()
        managerDefaults = None
        # Insert the Manager section if it is not already there
        buildConfSection(self.projConfig, 'Managers')
        if not testForSetting(self.projConfig['Managers'], fullName) :
            buildConfSection(self.projConfig['Managers'], fullName)

        # Update settings if needed
        update = False
        managerDefaults = getXMLSettings(os.path.join(self.local.rapumaConfigFolder, mType + '.xml'))
        for k, v, in managerDefaults.iteritems() :
            # Do not overwrite if a value is already there
            if not testForSetting(self.projConfig['Managers'][fullName], k) :
                self.projConfig['Managers'][fullName][k] = v
                # If we are dealing with an empty string, don't bother writing out
                # Trying to avoid needless conf updating here. Just in case we are
                # working with a list, we'll use len()
                if len(v) > 0 :
                    update = True
        # Update the conf if one or more settings were changed
        if update :
            if writeConfFile(self.projConfig) :
                self.log.writeToLog('PROJ-010',[fullName])
            else :
                self.log.writeToLog('PROJ-011',[fullName])


###############################################################################
############################ Group Level Functions ############################
###############################################################################

    def renderGroup (self, cType, gid, force = False) :
        '''Render a group of subcomponents.'''

#        import pdb; pdb.set_trace()

        # If we made it this far, try rendering
        if checkForGid(gid) :
            cType = self.projConfig['Groups'][gid]['cType']
            self.createGroup(gid, cType).render(force)
            self.setGidCurrent(cType, gid)
            return True


    def createGroup (self, gid, cType) :
        '''Create a group object that can be acted on. It is assumed
        this only happens for one group per session. This group
        will contain one or more compoenents. The information for
        each one will be contained in the group object.'''

        # If the object already exists just return it
        if gid in self.groups: return self.groups[gid]

#        import pdb; pdb.set_trace()

        # Create a special component object if called
        self.gid = gid
        cfg = self.projConfig['Groups'][gid]
        module = import_module('rapuma.group.' + cType)
        ManagerClass = getattr(module, cType.capitalize())
        compobj = ManagerClass(self, cfg)
        self.groups[gid] = compobj

        return compobj


    def addGroup (self, cType, gid, cidList, newSource = None, force = False) :
        '''This handels adding a group which can contain one or more components.'''

        # Set the gid if it is not already
        if not self.gid :
            self.gid = gid

        # Do not want to add this group, non-force, if it already exsists.
        buildConfSection(self.projConfig, 'Groups')
        if testForSetting(self.projConfig['Groups'], gid) and not force :
            self.log.writeToLog('GRUP-010', [gid])
            dieNow()

        # Work out the source path to components used in this group
        oldSource = ''
        if newSource :
            newSource = resolvePath(newSource)
            if not os.path.isdir(newSource) :
                self.log.writeToLog('GRUP-020', [newSource])
                dieNow()

        if self.hasSourcePath(gid) :
            if os.path.isdir(self.userConfig['Projects'][self.projectIDCode][gid + '_sourcePath']) :
                oldSource = self.userConfig['Projects'][self.projectIDCode][gid + '_sourcePath']

        # If the new source is valid, we will add that to the config now
        # so that processes to follow will have that setting available.
        if newSource :
            source = newSource
            self.addCompGroupSourcePath(gid, source)
            setattr(self, gid + '_sourcePath', source)
        # If there is no newSource, then the status quo will work okay
        elif oldSource :
            source = oldSource
        # No new or old source means we are hossed
        else :
            self.log.writeToLog('GRUP-030')
            dieNow()

        # The cList can be one or more valid component IDs
        # It is expected that the data for this list is in
        # this format: "id1 id2 id3 ect", unless it is coming
        # internally which means it might alread be a proper
        # list. We'll check first.
        if type(cidList) != list :
            cidList = cidList.split()

#        import pdb; pdb.set_trace()

        # Add the info to the group config info
        buildConfSection(self.projConfig, 'Groups')
        buildConfSection(self.projConfig['Groups'], gid)
        self.projConfig['Groups'][gid]['cType']     = cType
        self.projConfig['Groups'][gid]['cidList']   = cidList
        self.projConfig['Groups'][gid]['style']     = ''

        # Create the group object now that we have an entry in the config
        self.createGroup(gid, cType)
        # Install the group's components
        self.installGroupComps(gid, force)
        # Create an empty component group folder if needed
        groupFolder = os.path.join(self.local.projComponentsFolder, gid)
        if not os.path.exists(groupFolder) :
            os.makedirs(groupFolder)
            self.log.writeToLog('GRUP-110', [gid])
        # Lock and save our config settings
        self.projConfig['Groups'][gid]['isLocked']  = True
        if writeConfFile(self.projConfig) :
            self.log.writeToLog('GRUP-040', [gid])


    def installGroupComps (self, gid, force = False) :
        '''This will install components to the group we created above in createGroup().
        If a component is already installed in the project it will not proceed unless
        force is set to True. Then it will remove the component files so a fresh copy
        can be added to the project.'''

#        import pdb; pdb.set_trace()

        # Get some group settings
        cType       = self.projConfig['Groups'][gid]['cType']
        cidList     = self.projConfig['Groups'][gid]['cidList']
        sourcePath  = self.userConfig['Projects'][self.projectIDCode][gid + '_sourcePath']

        for cid in cidList :
            # See if the working text is present, quite if it is not
            if cType == 'usfm' :
                # Force on add always means we delete the component first
                # before we do anything else
                if force :
                    self.uninstallGroupComponents(gid, cid, force)

                # Install our working text files
                self.createManager(cType, 'text')
                if self.groups[gid].installUsfmWorkingText(gid, cid, force) :
                    # Report in context to force use or not
                    if force :
                        self.log.writeToLog('COMP-022', [cid])
                    else :
                        self.log.writeToLog('COMP-020', [cid])

                else :
                    self.log.writeToLog('TEXT-160', [cid])
                    return False
            else :
                self.log.writeToLog('COMP-005', [cType])
                dieNow()

        # If we got this far it must be okay to leave
        return True


    def removeGroup (self, gid, force = False) :
        '''Handler to remove a group. If it is not found return True anyway.'''

        cidList     = self.projConfig['Groups'][gid]['cidList']
        cType     = self.projConfig['Groups'][gid]['cType']
        groupFolder = os.path.join(self.local.projComponentsFolder, gid)
        # Create the group object now
        self.createGroup(gid, cType)

        # First test for lock
        if self.isLocked(gid) and force == False :
            self.log.writeToLog('COMP-110', [gid])
            dieNow()

        # Remove subcomponents from the target if there are any
        buildConfSection(self.projConfig, 'Groups')
        if isConfSection(self.projConfig['Groups'], gid) :
            for cid in cidList :
                self.uninstallGroupComponents(gid, cid, force)
            if os.path.exists(groupFolder) :
                shutil.rmtree(groupFolder)
                self.log.writeToLog('GRUP-090', [gid])
        else :
            self.log.writeToLog('GRUP-050', [gid])


#    def uninstallGroup (self, gid, force = False) :
#        '''This will remove a specific component from the project configuration as
#        well as the physical files. However, a backup will be made of the working
#        text for comparison purposes. If the component is locked, the function will

#        abort. This does not return anything. We trust it worked.'''

#        # First test for lock
#        if self.isLocked(gid) and force == False :
#            self.log.writeToLog('COMP-110', [gid])
#            dieNow()

#        # We will not bother if it is not in the config file.
#        # Otherwise, delete both the config and physical files
#        buildConfSection(self.projConfig, 'Groups')
#        if isConfSection(self.projConfig['Groups'], gid) :
#            # We will need to record the cType
#            cType = self.projConfig['Groups'][gid]['cType']
#            del self.projConfig['Groups'][gid]
#            # Sanity check
#            if not isConfSection(self.projConfig['Groups'], gid) :
#                writeConfFile(self.projConfig)
#                self.log.writeToLog('COMP-030', [gid])
#            # Hopefully all went well with config delete, now on to the files
#            if force :
#                cid             = self.groups[gid].getUsfmCid(cid)
#                targetFolder    = os.path.join(self.local.projComponentsFolder, cid)
#                source          = os.path.join(targetFolder, cid + '.' + cType)
#                targetComp      = os.path.join(source + '.cv1')
#                if os.path.isfile(source) :
#                    # First a comparison backup needs to be made of the working text
#                    if os.path.isfile(targetComp) :
#                        makeWriteable(targetComp)
#                    shutil.copy(source, targetComp)
#                    makeReadOnly(targetComp)
#                    for fn in os.listdir(targetFolder) :
#                        f = os.path.join(targetFolder, fn)
#                        if f != targetComp :
#                            os.remove(f)

#                    self.log.writeToLog('COMP-031', [cid])
#                else :
#                    self.log.writeToLog('COMP-032', [cid])

#                self.log.writeToLog('COMP-033', [cid])

#            self.log.writeToLog('COMP-035', [cid])


    def updateGroup (self, gid, source = None, force = False) :
        '''Update a component, --source is optional but if given it will
        overwrite the current setting. The use of this function implies
        that this is forced so no force setting is used.'''

        # Create the component object now
        self.createComponent(cName)

        # Check to be sure the component exsits
        if not self.components[cName] :
            self.log.writeToLog('COMP-210', [cName])
            dieNow()

        # If force is used, just unlock by default
        if force :
            self.lockUnlock(cName, False, force)

        # Be sure the component (and subcomponents) are unlocked
        if self.isLocked(cName) :
            self.log.writeToLog('COMP-110', [cName])
            dieNow()

        # Here we essentially re-add the component
        cType = self.groups[gid].getComponentType(gid)
        cidList = self.groups[gid].getSubcomponentList(gid)
        if not source :
            source = self.userConfig['Projects'][self.projectIDCode][cType + '_sourcePath']
        self.addComponent(cType, cName, cidList, source, force)
        
        # Now do a compare between the old component and the new one
        if str2bool(self.projConfig['Managers'][cType + '_Text']['useAutoCompare']) :
            self.compareComponent(cName, 'working')


    def hasSourcePath (self, gid) :

        '''Check to see if there is a pre-exsisting path.'''

        if testForSetting(self.userConfig['Projects'][self.projectIDCode], gid + '_sourcePath') :
            if self.userConfig['Projects'][self.projectIDCode][gid + '_sourcePath'] != '' :
                return True


    def sourceIsSame (self, gid, source) :
        '''Check to see if the existing path is the same as the
        new proposed path.'''

        curPath = self.userConfig['Projects'][self.projectIDCode][gid + '_sourcePath']
        if curPath == source :
            return True


    def addCompGroupSourcePath (self, gid, source) :
        '''Add a source path for components used in a group if none
        exsist. If one exists, replace anyway. Last in wins! The 
        assumption is only one path per component group.'''

        # Path has been resolved in Rapuma, we assume it should be valid.
        # But it could be a full file name. We need to sort that out.
        try :
            if os.path.isdir(source) :
                self.userConfig['Projects'][self.projectIDCode][gid + '_sourcePath'] = source
            else :
                self.userConfig['Projects'][self.projectIDCode][gid + '_sourcePath'] = os.path.split(source)[0]

            writeConfFile(self.userConfig)
        except Exception as e :
            # If we don't succeed, we should probably quite here
            self.log.writeToLog('GRUP-100', [str(e)])
            dieNow()


    def isLocked (self, gid) :
        '''Test to see if a group is locked. Return True if the group is 
        locked. However, if the group doesn't even exsist, it is assumed
        that it is unlocked and return False. :-)'''

        if not testForSetting(self.projConfig['Groups'], gid, 'isLocked') :
            return False
        elif str2bool(self.projConfig['Groups'][gid]['isLocked']) == True :
            return True
        else :
            return False


    def lockUnlock (self, gid, lock = True) :
        '''Lock or unlock to enable or disable actions to be taken on a group.'''

        # First be sure this is a valid component
        if not self.groups[gid] :
            self.log.writeToLog('LOCK-010', [gid])
            dieNow()
        else :
            self.setLock(gid, lock)
            return True


    def setLock (self, gid, lock) :
        '''Set a group lock to True or False.'''

        if testForSetting(self.projConfig['Groups'], gid) :
            self.projConfig['Groups'][gid]['isLocked'] = lock
            # Update the projConfig
            if writeConfFile(self.projConfig) :
                # Report back
                self.log.writeToLog('LOCK-020', [gid, str(lock)])
                return True
        else :
            self.log.writeToLog('LOCK-030', [gid, str(lock)])
            return False


    def listAllComponents (self, cType) :
        '''Generate a list of valid component IDs and cNames for this cType.'''

        # Create the component object now with a special component caller ID
        self.createComponent('usfm_internal_caller')
        # Get the component info dictionary
        comps = self.components['usfm_internal_caller'].usfmCidInfo()
        # List and sort
        cList = list(comps.keys())
        cList.sort()
        # For now we'll output to terminal but may want to change this later.
        for c in cList :
            if c != '_z_' :
                print c, comps[c][1]


    def uninstallGroupComponents (self, gid, cid, force = False) :
        '''This will remove all the component (files) from a group in the project.
        However, a backup will be made of the working text for comparison purposes. 
       This does not return anything. We trust it worked.'''

        cType       = self.projConfig['Groups'][gid]['cType']

        # Test to see if it is shared
        if self.isSharedComponent(gid, cid) :
            self.log.writeToLog('GRUP-060', [gid])
            dieNow()

        # Remove the files
        if force :
            targetFolder    = os.path.join(self.local.projComponentsFolder, cid)
            source          = os.path.join(targetFolder, cid + '.' + cType)
            targetComp      = os.path.join(source + '.cv1')
            if os.path.isfile(source) :
                # First a comparison backup needs to be made of the working text
                if os.path.isfile(targetComp) :
                    makeWriteable(targetComp)
                shutil.copy(source, targetComp)
                makeReadOnly(targetComp)
                self.log.writeToLog('GRUP-070', [fName(targetComp), cid])
                for fn in os.listdir(targetFolder) :
                    f = os.path.join(targetFolder, fn)
                    if f != targetComp :
                        os.remove(f)
                        self.log.writeToLog('GRUP-080', [fName(f), cid])


    def isSharedComponent (self, gid, cid) :
        '''If the cid is shared by any other groups, return True.'''

        try :
            for g in self.projConfig['Groups'].keys() :
                if g != gid :
                    if cid in self.projConfig['Groups'][g]['cidList'] :
                        return True
        except :
            return False


###############################################################################
########################## Component Level Functions ##########################
###############################################################################

    def setProjCurrent (self, pid) :
        '''Compare pid with the current recored pid e rapuma.conf. If it is
        different change to the new pid. If not, leave it alone.'''

        currentPid = self.userConfig['System']['current']
        if pid != currentPid :
            self.userConfig['System']['current'] = pid
            writeConfFile(self.userConfig)


    def setCidCurrent (self, cType, cName) :
        '''Compare cName with the current recorded cName. If it is different
        then change to the new cName. If not, leave it alone.'''

        currentCName = self.projConfig['CompTypes'][cType.capitalize()]['current']
        if cName != currentCName :
            self.projConfig['CompTypes'][cType.capitalize()]['current'] = cName
            writeConfFile(self.projConfig)


    def renderComponent (self, cType, cName, force = False) :
        '''Render a component which includes any subcomponents. If a cid
        is passed it will first try to find out the real component name,
        then render that. A valid cType must be passed to it to work.'''

#        import pdb; pdb.set_trace()

        # Create the component object now
        self.createComponent(cName)

        # Initialize some vars
        validCName = ''
        testCid = ''

        # Render by types
        if cType == 'usfm' :
            # It may be that a valid ID was used and needs to be
            # translated to a valid component name. Before giving up
            # try to do that first. This would be for cases where a
            # single (atomic) component is being rendered and the
            # user only gave its cid. Do a look up to find the
            # actual component name.
            if self.components[cName].isCompleteComponent(cName) :
                validCName = cName
            else :
                cName = self.components[cName].getRapumaCName(cName)
                if self.components[cName].hasCNameEntry(cName) :
                    validCName = cName
                else :
                    # Well, we did try
                    self.log.writeToLog('COMP-010', [cName])
                    return False
        else :
            self.log.writeToLog('COMP-005', [self.cType])
            return False
        
        # Reset the session cName
        self.cName = validCName

        # If we made it this far, try rendering
        if validCName :
            self.createComponent(validCName).render(force)
            self.setCidCurrent(cType, cName)
            return True


#    def createComponent (self, cName) :
#        '''Create a component object that can be acted on. It is assumed
#        this only happens for one component per session. This component
#        may contain subcomponents that support this one.'''

#        # If the object already exists just return it
#        if cName in self.components : return self.components[cName]

##        import pdb; pdb.set_trace()

#        # Create a special component object if called
#        if cName == 'usfm_internal_caller' :
#            cfg = dict()
#            self.cName = cName
#            cType = cName.split('_')[0]
#            buildConfSection(cfg, 'Components')
#            buildConfSection(cfg['Components'], cName)
#            cfg['Components'][cName]['type'] = cType
#            module = import_module('rapuma.component.' + cType)
#            ManagerClass = getattr(module, cType.capitalize())
#            compobj = ManagerClass(self, cfg)
#            self.components[cName] = compobj
#        # Otherwise, create a new one and return it
#        elif testForSetting(self.projConfig, 'Components', cName) :
#            # Set the primary component name
#            self.cName = cName
#            cfg = self.projConfig['Components'][cName]
#            cType = cfg['type']
#            module = import_module('rapuma.component.' + cType)
#            ManagerClass = getattr(module, cType.capitalize())
#            compobj = ManagerClass(self, cfg)
#            self.components[cName] = compobj
#        else :
#            self.log.writeToLog('COMP-040', [cName])
#            return False

#        return compobj


#    def addComponent (self, cType, cName, cidList, newSource = None, force = False) :
#        '''This handels adding a component which can contain one or more sub-components.'''

#        # Check for cName setting
#        # FIXME: There is something is wrong about doing this here
#        if not self.cName :
#            self.cName = cName

#        # Do not want to add this component, non-force, if it already exsists.
#        if cName in self.projConfig['Components'].keys() and not force and self.isLocked(cName) :
#            self.log.writeToLog('COMP-115', [cName])
#            dieNow()

#        # Work out the source path
#        oldSource = ''
#        if newSource :
#            newSource = resolvePath(newSource)
#            if not os.path.isdir(newSource) :
#                self.log.writeToLog('COMP-160', [newSource])
#                dieNow()

#        if self.hasSourcePath(cType) :
#            if os.path.isdir(self.userConfig['Projects'][self.projectIDCode][cType + '_sourcePath']) :
#                oldSource = self.userConfig['Projects'][self.projectIDCode][cType + '_sourcePath']

#        # If the new source is valid, we will add that to the config now
#        # so that processes to follow will have that setting available.
#        if newSource :
#            source = newSource
#            self.addCompTypeSourcePath(cType, source)
#            setattr(self, cType + '_sourcePath', source)
#        # If there is no newSource, then the status quo will work okay
#        elif oldSource :
#            source = oldSource
#        # No new or old source means we are hossed
#        else :
#            self.log.writeToLog('COMP-170')
#            dieNow()

#        # The cList can be one or more valid component IDs
#        # It is expected that the data for this list is in
#        # this format: "id1 id2 id3 ect", unless it is coming
#        # internally which means it might alread be a proper
#        # list. We'll check first.
#        if type(cidList) != list :
#            cidList = cidList.split()

##        import pdb; pdb.set_trace()

#        # Add the info to the components
#        buildConfSection(self.projConfig, 'Components')
#        buildConfSection(self.projConfig['Components'], cName)
#        self.projConfig['Components'][cName]['type'] = cType
#        self.projConfig['Components'][cName]['cidList'] = cidList
#        self.projConfig['Components'][cName]['isLocked'] = True

#        # Create the component object now that we have an entry in the config
#        self.createComponent(cName)

#        # Add subcomponents
#        for cid in cidList :
#            # If cName for the cid is the same as the main component cName
#            # we have to unlock it to avoid a problem in this step.
#            if self.components[cName].getRapumaCName(cid) == cName :
#                self.projConfig['Components'][cName]['isLocked'] = False
#            if not self.installComponent(cType, cName, cid, source, force) :
#                if not self.components[cName].isCompleteComponent(self.components[cName].getRapumaCName(cid)) :
#                    dieNow()

#        # If there was more than one subcomponent, this is a group
#        # thus we should make a folder for it.
#        if len(cidList) > 1 :
#            if not os.path.isdir(os.path.join(self.local.projComponentsFolder, cName)) :
#                os.mkdir(os.path.join(self.local.projComponentsFolder, cName))

#        # Save our config settings
#        if writeConfFile(self.projConfig) :
#            self.log.writeToLog('COMP-015', [cName])


#    def installComponent (self, cType, cName, cid, source, force = False) :
#        '''This will add a component to the object we created above in createComponent().
#        If the component is already listed in the project configuration it will not proceed
#        unless force is set to True. Then it will remove the component listing, along with 
#        its files so a fresh copy can be added to the project. This works at the single
#        component level. The cid must be validated against its type.'''

##        import pdb; pdb.set_trace()

#        # See if the working text is present, quite if it is not
#        if cType == 'usfm' :
#            # To maintain the distinction between comp name and comp ID, we will
#            # auto-create a name for this component that is taken from its valid
#            # name in the component dictionary. We will also validate the ID too.
#            if self.components[cName].hasUsfmCidInfo(cid) :
#                cName = self.components[cName].getRapumaCName(cid)
#            else :
#                self.log.writeToLog('COMP-010', [cid])
#                dieNow()

#            # Current thinking is that a locked component cannot be touched,
#            # not even by force (-f) Check here to see if that is the case.
#            # Give a warning if it is and return False
#            if self.isLocked(cName) :
#                self.log.writeToLog('COMP-115', [cName])
#                return False

#            # Force on add always means we delete the component first
#            # before we do anything else
#            if force :
#                self.removeComponentFiles(gid, cid, force)

#            # Put the (refreshed) settings back in the project config
#            if not self.insertComponent(cType, cName, cid) :
#                self.log.writeToLog('COMP-100', [cName])
#                dieNow()

#            # Install our working text files
#            self.createManager(cType, 'text')
#            if self.components[cName].installUsfmWorkingText(cName, cid, force) :

#                # Finish the install by locking
#                self.lockUnlock(cName, True)

#                # Report in context to force use or not
#                if force :
#                    self.log.writeToLog('COMP-022', [cName])
#                else :
#                    self.log.writeToLog('COMP-020', [cName])

#            else :
#                self.log.writeToLog('TEXT-160', [cName])
#                return False
#        else :
#            self.log.writeToLog('COMP-005', [cType])
#            dieNow()

#        # If we got this far it must be okay to leave
#        return True


#    def insertComponent (self, cType, cName, cid) :
#        '''Insert a single component into the project.conf and create a component manager.'''

#        buildConfSection(self.projConfig, 'Components')
#        buildConfSection(self.projConfig['Components'], cName)
#        self.projConfig['Components'][cName]['type'] = cType
#        self.projConfig['Components'][cName]['cidList'] = [cid]
#        self.projConfig['Components'][cName]['isLocked'] = False
#        self.buildComponentObject(cType, cName)
#        # Save our config settings
#        if writeConfFile(self.projConfig) :
#            return True


#    def buildComponentObject (self, cType, cName) :
#        '''This will load the component type manager object.'''

#        cfg = self.projConfig['Components'][cName]
#        module = import_module('rapuma.component.' + cType)
#        ManagerClass = getattr(module, cType.capitalize())
#        compobj = ManagerClass(self, cfg)
#        self.components[cName] = compobj












#    def removeComponentFiles (self, gid, cid, force = False) :
#        '''Handler to remove a component from a project group. However, if the
#        files are shared by another group, it will not remove them. and return
#        False. If the files are not found return True.'''

## FIXME: Do we want a force override, for now, no.

#        # First check to see if this cid is shared by another gid
#        if not isSharedComponent(gid, cid) :
#            # Remove the target component
#            self.uninstallGroupComponent(gid, cid, force)
#            # Test for success
#            if not self.components[cName].isCompleteComponent(cName) :
#                self.log.writeToLog('COMP-120', [cName])
#            else :
#                self.log.writeToLog('COMP-140', [cName])
#                dieNow()
#        else :
#            self.log.writeToLog('COMP-150', [cName])


    def addComponentType (self, cType) :
        '''Add (register) a component type to the config if it 
        is not there already.'''

        Ctype = cType.capitalize()
        if cType not in self.components :
            # Build the comp type config section
            buildConfSection(self.projConfig, 'CompTypes')
            buildConfSection(self.projConfig['CompTypes'], Ctype)

            # Get persistant values from the config if there are any
            newSectionSettings = getPersistantSettings(self.projConfig['CompTypes'][Ctype], os.path.join(self.local.rapumaConfigFolder, cType + '.xml'))
            if newSectionSettings != self.projConfig['CompTypes'][Ctype] :
                self.projConfig['CompTypes'][Ctype] = newSectionSettings
                # Save the setting rightaway
#                import pdb; pdb.set_trace()
                writeConfFile(self.projConfig)

            # Sanity check
            if cType not in self.components :
                self.log.writeToLog('COMP-060', [cType])
                return True
            else :
                self.log.writeToLog('COMP-065', [cType])
                return False
        else :
            # Bow out gracefully
            return False


    def updateComponent (self, cName, source = None, force = False) :
        '''Update a component, --source is optional but if given it will
        overwrite the current setting. The use of this function implies
        that this is forced so no force setting is used.'''

        # Create the component object now
        self.createComponent(cName)

        # Check to be sure the component exsits
        if not self.components[cName] :
            self.log.writeToLog('COMP-210', [cName])
            dieNow()

        # If force is used, just unlock by default
        if force :
            self.lockUnlock(cName, False, force)

        # Be sure the component (and subcomponents) are unlocked
        if self.isLocked(cName) :
            self.log.writeToLog('COMP-110', [cName])
            dieNow()

        # Here we essentially re-add the component
        cType = self.groups[gid].getComponentType(gid)
        cidList = self.groups[gid].getSubcomponentList(gid)
        if not source :
            source = self.userConfig['Projects'][self.projectIDCode][cType + '_sourcePath']
        self.addComponent(cType, cName, cidList, source, force)
        
        # Now do a compare between the old component and the new one
        if str2bool(self.projConfig['Managers'][cType + '_Text']['useAutoCompare']) :
            self.compareComponent(cName, 'working')


    def compareComponent (self, cName, test) :
        '''Compare a component with its source which was copied into the project
        when the component was created. This will pull up the user's differential
        viewer and compare the two files.'''

        # Create the component object now (if there is not one)
        self.createComponent(cName)
        # First check to see if it is a valid component and get the cid
        if self.components[cName].hasCNameEntry(cName) :
            if self.components[cName].getUsfmCid(cName) :
                cid = self.components[cName].getUsfmCid(cName)
            else :
                self.log.writeToLog('COMP-185', [cName])
                dieNow()
        else :
            # Might the cName be a cid?
            cid = cName
            if self.components[cName].getRapumaCName(cid) :
                cName = self.components[cName].getRapumaCName(cid)
            else :
                self.log.writeToLog('COMP-185', [cName])
                dieNow()

        # What kind of test is this
        cType = self.projConfig['Components'][cName]['type']
        if test == 'working' :
            new = os.path.join(self.local.projComponentsFolder, cName, cid + '.' + cType)
            old = os.path.join(self.local.projComponentsFolder, cName, cid + '.' + cType + '.cv1')
        elif test == 'source' :
            new = os.path.join(self.local.projComponentsFolder, cName, cid + '.' + cType)
            for files in os.listdir(os.path.join(self.local.projComponentsFolder, cName)) :
                if files.find('.source') > 0 :
                    old = os.path.join(self.local.projComponentsFolder, cName, files)
                    break
        else :
            self.log.writeToLog('COMP-190', [test])

        # Turn it over to the generic compare tool
        self.compare(new, old)


###############################################################################
########################## Text Processing Functions ##########################
###############################################################################

    def turnOnOffPreprocess (self, cType, onOff = False) :
        '''Turn on or off preprocessing on incoming component text.'''

        # Current status
        current = self.projConfig['CompTypes'][cType.capitalize()]['usePreprocessScript']

        if current != onOff :
            if onOff == True :
                self.projConfig['CompTypes'][cType.capitalize()]['usePreprocessScript'] = True
                # Now check to see if the script is there and warn if not
                self.installPreprocess(cType)
            else :
                self.projConfig['CompTypes'][cType.capitalize()]['usePreprocessScript'] = False

            writeConfFile(self.projConfig)
            self.log.writeToLog('PROC-140', [str(onOff),cType])
        else :
            self.log.writeToLog('PROC-150', [cType,str(onOff)])


    def installPreprocess (self, cType) :
        '''Check to see if a preprocess script is installed. If not, install the
        default script and give a warning that the script is not complete.'''

        # File paths
        preprocessScriptName   = self.projConfig['CompTypes'][cType.capitalize()]['preprocessScript']
        rapumaPreprocessScript = os.path.join(self.local.rapumaScriptsFolder, preprocessScriptName)
        preprocessScript       = os.path.join(self.local.projScriptsFolder, cType + '_' + preprocessScriptName)
        # Check and copy if needed
        if not os.path.isfile(preprocessScript) :
            shutil.copy(rapumaPreprocessScript, preprocessScript)
            makeExecutable(preprocessScript)
            self.log.writeToLog('PROC-160')
            dieNow()
        else :
            self.log.writeToLog('PROC-165')


    def runProcessScript (self, gid, scriptFileName = None) :
        '''Run a text processing script on a component (including subcomponents).
        This assumes the component and the script are valid and the component 
        lock is turned off. However, it will look for a lock at the subcomponent 
        level too.'''

        # First test to see if we can run, quite if not
        if self.groups[gid].isCompleteComponent(cid) :
            cType = self.groups[gid].getComponentType(gid)
        else :
            self.log.writeToLog('PROC-110', [cType])
            dieNow()

        # Find the script we will use. It is assumed that if there is
        # no scriptFileName given, we are working with a pre, not
        # post process.
        if scriptFileName :
            script = os.path.join(self.local.projScriptsFolder, scriptFileName)
            if not os.path.isfile(script) :
                self.log.writeToLog('PROC-120', [cType])
                return False
        else :
            if testForSetting(self.projConfig['CompTypes'][cType.capitalize()], 'preprocessScript') :
                if self.projConfig['CompTypes'][cType.capitalize()]['preprocessScript'] :
                    scriptFileName = self.projConfig['CompTypes'][cType.capitalize()]['preprocessScript']
                    script = os.path.join(self.local.projScriptsFolder, scriptFileName)
                    if not os.path.isfile(script) :
                        self.log.writeToLog('PROC-120', [cType])
                        return False

        # Check to see if the component is locked
        if testForSetting(self.projConfig['Components'][cName], 'isLocked') :
            if str2bool(self.projConfig['Components'][cName]['isLocked']) == True :
                self.log.writeToLog('PROC-130', [cType])
                return False

        # If we made it this far, we can try running it
        for cid in self.components[cName].getSubcomponentList(cName) :
            cidName = self.components[cName].getRapumaCName(cid)
            if not str2bool(self.projConfig['Components'][cidName]['isLocked']) :
                cType = self.groups[gid].getComponentType(gid)
                target = os.path.join(self.local.projComponentsFolder, cidName, cid + '.' + cType)
                if os.path.isfile(script) :
                    # subprocess will fail if permissions are not set on the
                    # script we want to run. The correct permission should have
                    # been set when we did the installation.
                    err = subprocess.call([script, target])
                    if err == 0 :
                        self.log.writeToLog('PROC-010', [fName(target), fName(script)])
                    else :
                        self.log.writeToLog('PROC-020', [fName(target), fName(script), str(err)])
                        return False
                else :
                    self.log.writeToLog('PROC-030', [fName(target), fName(script)])
                    return False
            else :
                self.log.writeToLog('PROC-050', [cName, fName(script)])
                return False

        return True


#    def recordPreprocessScript (self, cType, script) :
#        '''Record a preprocess script in the project.'''

#        self.projConfig['CompTypes'][cType.capitalize()]['preprocessScript'] = fName(script)
#        writeConfFile(self.projConfig)


    def scriptInstall (self, source, target) :
        '''Install a script. A script can be a collection of items in
        a zip file or a single .py script file.'''

        scriptTargetFolder, fileName = os.path.split(target)
        if isExecutable(source) :
            shutil.copy(source, target)
            makeExecutable(target)
        elif fName(source).split('.')[1].lower() == 'zip' :
            myZip = zipfile.ZipFile(source, 'r')
            for f in myZip.namelist() :
                data = myZip.read(f, source)
                # Pretty sure zip represents directory separator char as "/" regardless of OS
                myPath = os.path.join(scriptTargetFolder, f.split("/")[-1])
                try :
                    myFile = open(myPath, "wb")
                    myFile.write(data)
                    myFile.close()
                except :
                    pass
            myZip.close()
            return True
        else :
            dieNow('Script is an unrecognized type: ' + fName(source) + ' Cannot continue with installation.')


    def installPostProcess (self, cType, script, force = None) :
        '''Install a post process script into the main components processing
        folder for a specified component type. This script will be run on 
        every file of that type that is imported into the project. Some
        projects will have their own specially developed post process
        script. Use the "script" var to specify a process (which should be
        bundled in a system compatable way). If "script" is not specified
        we will copy in a default script that the user can modify. This is
        currently limited to Python scripts only which do in-place processes
        on the target files. The script needs to have the same name as the
        zip file it is bundled in, except the extention is .py instead of
        the bundle .zip extention.'''

        # Define some internal vars
        Ctype               = cType.capitalize()
        oldScript           = ''
        scriptName          = os.path.split(script)[1]
        scriptSourceFolder  = os.path.split(script)[0]
        scriptTarget        = os.path.join(self.local.projScriptsFolder, fName(script).split('.')[0] + '.py')
        if scriptName in self.projConfig['CompTypes'][Ctype]['postprocessScripts'] :
            oldScript = scriptName

        # First check for prexsisting script record
        if not force :
            if oldScript :
                self.log.writeToLog('POST-080', [oldScript])
                return False

        # In case this is a new project we may need to install a component
        # type and make a process (components) folder
        if not self.components[cType] :
            self.addComponentType(cType)

        # Make the target folder if needed
        if not os.path.isdir(self.local.projScriptsFolder) :
            os.makedirs(self.local.projScriptsFolder)

        # First check to see if there already is a script file, return if there is
        if os.path.isfile(scriptTarget) and not force :
            self.log.writeToLog('POST-082', [fName(scriptTarget)])
            return False

        # No script found, we can proceed
        if not os.path.isfile(scriptTarget) :
            self.scriptInstall(script, scriptTarget)
            if not os.path.isfile(scriptTarget) :
                dieNow('Failed to install script!: ' + fName(scriptTarget))
            self.log.writeToLog('POST-110', [fName(scriptTarget)])
        elif force :
            self.scriptInstall(script, scriptTarget)
            if not os.path.isfile(scriptTarget) :
                dieNow('Failed to install script!: ' + fName(scriptTarget))
            self.log.writeToLog('POST-115', [fName(scriptTarget)])

        # Record the script with the cType post process scripts list
        scriptList = self.projConfig['CompTypes'][Ctype]['postprocessScripts']
        if fName(scriptTarget) not in scriptList :
            self.projConfig['CompTypes'][Ctype]['postprocessScripts'] = addToList(scriptList, fName(scriptTarget))
            writeConfFile(self.projConfig)

        return True


    def removePostProcess (self, cType) :
        '''Remove (actually disconnect) a preprocess script from a

        component type. This will not actually remove the script. That
        would need to be done manually. Rather, this will remove the
        script name entry from the component type so the process cannot
        be accessed for this specific component type.'''

        Ctype = cType.capitalize()
        # Get old setting
        old = self.projConfig['CompTypes'][Ctype]['postprocessScripts']
        # Reset the field to ''
        if old != '' :
            self.projConfig['CompTypes'][Ctype]['postprocessScripts'] = ''
            writeConfFile(self.projConfig)
            self.log.writeToLog('POST-130', [old,Ctype])

        else :
            self.log.writeToLog('POST-135', [cType.capitalize()])

        return True


###############################################################################
############################## Exporting Functions ############################
###############################################################################


    def export (self, cType, cName, path = None, script = None, bundle = False, force = False) :
        '''Facilitate the exporting of project text. It is assumed that the
        text is clean and ready to go and if any extraneous publishing info
        has been injected into the text, it will be removed by an appropreate
        post-process that can be applied by this function. No validation
        will be initiated by this function.'''
        
        # FIXME - Todo: add post processing script feature

        # Probably need to create the component object now
        self.createComponent(cName)

        # Figure out target path
        if path :
            path = resolvePath(path)
        else :
            parentFolder = os.path.dirname(self.local.projHome)
            path = os.path.join(parentFolder, 'Export')

        # Make target folder if needed
        if not os.path.isdir(path) :
            os.makedirs(path)

        # Start a list for one or more files we will process
        fList = []

        # Will need the stylesheet for copy
        projSty = self.projConfig['Managers'][cType + '_Style']['mainStyleFile']
        projSty = os.path.join(self.local.projStylesFolder, projSty)
        # Process as list of components

        self.log.writeToLog('XPRT-040')
        for cid in self.components[cName].getSubcomponentList(cName) :
            cidCName = self.components[cName].getRapumaCName(cid)
            ptName = self.pt_tools.formPTName(cName, cid)
            # Test, no name = no success
            if not ptName :
                self.log.writeToLog('XPRT-010')
                dieNow()

            target = os.path.join(path, ptName)
            source = os.path.join(self.local.projComponentsFolder, cidCName, cid + '.' + cType)
            # If shutil.copy() spits anything back its bad news
            if shutil.copy(source, target) :
                self.log.writeToLog('XPRT-020', [fName(target)])
            else :
                fList.append(target)

        # Start the main process here
        if bundle :
            archFile = os.path.join(path, cName + '_' + ymd() + '.zip')
            # Hopefully, this is a one time operation but if force is not True,
            # we will expand the file name so nothing is lost.
            if not force :
                if os.path.isfile(archFile) :
                    archFile = os.path.join(path, cName + '_' + fullFileTimeStamp() + '.zip')

            myzip = zipfile.ZipFile(archFile, 'w', zipfile.ZIP_DEFLATED)
            for f in fList :
                # Create a string object from the contents of the file
                strObj = StringIO.StringIO()
                for l in open(f, "rb") :
                    strObj.write(l)
                # Write out string object to zip
                myzip.writestr(fName(f), strObj.getvalue())
                strObj.close()
            # Close out the zip and report
            myzip.close()
            # Clean out the folder
            for f in fList :
                os.remove(f)
            self.log.writeToLog('XPRT-030', [fName(archFile)])
        else :
            self.log.writeToLog('XPRT-030', [path])

        return True


###############################################################################
############################ System Level Functions ###########################
###############################################################################

    def isDifferent (self, new, old) :
        '''Return True if the contents of the files are different.'''

        # Inside of diffl() open both files with universial line endings then
        # check each line for differences.
        diff = difflib.ndiff(open(new, 'rU').readlines(), open(old, 'rU').readlines())
        comp = False
        for d in diff :
            if d[:1] == '+' or d[:1] == '-' :
                return True


    def compare (self, new, old) :
        '''Run a compare on two files. Do not open in viewer unless it is different.'''

        # If there are any differences, open the diff viewer
        if self.isDifferent(new, old) :
            # Get diff viewer
            diffViewer = self.userConfig['System']['textDifferentialViewerCommand']
            try :
                self.log.writeToLog('COMP-195', [fName(new),fName(old)])
                subprocess.call([diffViewer, new, old])
            except Exception as e :
                # If we don't succeed, we should probably quite here
                self.log.writeToLog('COMP-180', [str(e)])
                dieNow()
        else :
            self.log.writeToLog('COMP-198')


    def run (self, command, opts, userConfig) :
        '''Run a command'''

        if command in self.commands :
            self.commands[command].run(opts, self, userConfig)
        else :
            terminalError('The command: [' + command + '] failed to run with these options: ' + str(opts))


    def isProject (self, pid) :
        '''Look up in the user config to see if a project is registered. This
        is a duplicate of the function in the main rapuma file.'''

        try :
            if pid in self.userConfig['Projects'].keys() :
                pass
        except :
            sys.exit('\nERROR: Project ID given is not valid! Process halted.\n')


    def changeConfigSetting (self, config, section, key, newValue) :
        '''Change a value in a specified config/section/key.  This will 
        write out changes immediately. If this is called internally, the
        calling function will need to reload to the config for the
        changes to take place in the current session. This is currently
        designed to work more as a single call to Rapuma.'''

        oldValue = ''
        if config.lower() == 'rapuma' :
            confFile = os.path.join(self.local.userHome, 'rapuma.conf')
        else :
            confFile = os.path.join(self.local.projConfFolder, config + '.conf')

        confObj = ConfigObj(confFile, encoding='utf-8')
        outConfObj = confObj
        try :
            # Walk our confObj to get to the section we want
            for s in section.split('/') :
                confObj = confObj[s]
        except :
            self.log.writeToLog('PROJ-040', [section])
            return

        # Get the old value, if there is one, for reporting
        try :
            oldValue = confObj[key]
        except :
            pass

        # Insert the new value in its proper form
        if type(oldValue) == list :
            newValue = newValue.split(',')
            confObj[key] = newValue
        else :
            confObj[key] = newValue

        # Write out the original copy of the confObj which now 
        # has the change in it, then report what we did
        outConfObj.filename = confFile
        if writeConfFile(outConfObj) :
            self.log.writeToLog('PROJ-030', [config, section, key, str(oldValue), str(newValue)])


    def installFile (self, source, path, force) :
        '''Install a file into a project. Overwrite if force is set to True.'''

        source = resolvePath(source)
        target = os.path.join(resolvePath(path), fName(source))
        if not os.path.isfile(source) :
            self.log.writeToLog('PROJ-070', [source])

        if os.path.isfile(target) :
            if force :
                if not shutil.copy(source, target) :
                    self.log.writeToLog('PROJ-080', [source,target])
            else :
                self.log.writeToLog('PROJ-090', [source,target])
        else :
            if not shutil.copy(source, target) :
                self.log.writeToLog('PROJ-080', [source,target])


    def addMacro (self, name, cmd = None, path = None, force = False) :
        '''Install a user defined macro.'''

        # Define some internal vars
        oldMacro            = ''
        sourceMacro         = ''
        # FIXME: This needs to support a file extention such as .sh
        if path and os.path.isfile(os.path.join(resolvePath(path))) :
            sourceMacro     = os.path.join(resolvePath(path))
        macroTarget         = os.path.join(self.local.projUserMacrosFolder, name)
        if testForSetting(self.projConfig['GeneralSettings'], 'userMacros') and name in self.projConfig['GeneralSettings']['userMacros'] :
            oldMacro = name

        # First check for prexsisting macro record
        if not force :
            if oldMacro :
                self.log.writeToLog('MCRO-010', [oldMacro])
                dieNow()

        # Make the target folder if needed (should be there already, though)
        if not os.path.isdir(self.local.projUserMacrosFolder) :
            os.makedirs(self.local.projUserMacrosFolder)

        # First check to see if there already is a macro file, die if there is
        if os.path.isfile(macroTarget) and not force :
            self.log.writeToLog('MCRO-020', [fName(macroTarget)])
            dieNow()
            
        # If force, then get rid of the file before going on
        if force :
            if os.path.isfile(macroTarget) :
                os.remove(macroTarget)

        # No script found, we can proceed
        if os.path.isfile(sourceMacro) :
            shutil.copy(sourceMacro, macroTarget)
        else :
            # Create a new user macro file
            mf = codecs.open(macroTarget, 'w', 'utf_8_sig')
            mf.write('#!/bin/sh\n\n')
            mf.write('# This macro file was auto-generated by Rapuma. Add commands as desired.\n\n')
            # FIXME: This should be done as a list so multiple commands can be added
            if cmd :
                mf.write(cmd + '\n')
            mf.close

        # Be sure that it is executable
        makeExecutable(macroTarget)

        # Record the macro with the project
        if testForSetting(self.projConfig['GeneralSettings'], 'userMacros') :
            macroList = self.projConfig['GeneralSettings']['userMacros']
            if fName(macroTarget) not in macroList :
                self.projConfig['GeneralSettings']['userMacros'] = addToList(macroList, fName(macroTarget))
                writeConfFile(self.projConfig)
        else :
                self.projConfig['GeneralSettings']['userMacros'] = [fName(macroTarget)]
                writeConfFile(self.projConfig)

        self.log.writeToLog('MCRO-030', [fName(macroTarget)])
        return True


    def runMacro (self, name) :
        '''Run an installed, user defined macro.'''

        # In most cases we use subprocess.call() to do a process call.  However,
        # in this case it takes too much fiddling to get a these more complex Rapuma
        # calls to run from within Rapuma.  To make it easy, we use os.system() to
        # make the call out.
        macroFile = os.path.join(self.local.projUserMacrosFolder, name)
        if os.path.isfile(macroFile) :
            if self.macroRunner(macroFile) :
                return True
        else :
            self.log.writeToLog('MCRO-060', [fName(macroFile)])


    def macroRunner (self, macroFile) :
        '''Run a macro. This assumes the macroFile includes a full path.'''

        try :
            macro = codecs.open(macroFile, "r", encoding='utf_8')
            for line in macro :
                # Clean the line, may be a BOM to remove
                line = line.replace(u'\ufeff', '').strip()
                if line[:1] != '#' and line[:1] != '' and line[:1] != '\n' :
                    self.log.writeToLog('MCRO-050', [line])
                    # FIXME: Could this be done better with subprocess()?
                    os.system(line)
            return True

        except Exception as e :
            # If we don't succeed, we should probably quite here
            terminal('Macro failed with the following error: ' + str(e))
            dieNow()


# FIXME: Still lots to do on this next function

    def edit (self, cName = None, glob = False, sys = False) :
        '''Call editing application to edit various project and system files.'''

        editDocs = ['gedit']
        # If a subcomponent is called, pull it up and its dependencies
        # This will not work with components that have more than one
        # subcomponent.
        if cName :
            # Probably need to create the component object now
            self.createComponent(cName)

            cid = self.components[cName].getUsfmCid(cName)

            cType = self.groups[gid].getComponentType(gid)
            self.buildComponentObject(cType, cid)
            cidList = self.groups[gid].getSubcomponentList(gid)
            if len(cidList) > 1 :
                self.log.writeToLog('EDIT-010', [cid])
                dieNow()

            self.createManager(cType, 'text')
            compWorkText = self.groups[gid].getCidPath(cid)
            if os.path.isfile(compWorkText) :
                editDocs.append(compWorkText)
                compTextAdj = self.components[cName].getCidAdjPath(cid)
                compTextIlls = self.components[cName].getCidPiclistPath(cid)
                dep = [compTextAdj, compTextIlls]
                for d in dep :
                    if os.path.isfile(d) :
                        editDocs.append(d)
            else :
                self.log.writeToLog('EDIT-020', [fName(compWorkText)])
                dieNow()

        # Look at project global settings
        if glob :
            for files in os.listdir(self.local.projConfFolder):
                if files.endswith(".conf"):
                    editDocs.append(os.path.join(self.local.projConfFolder, files))

            globSty = os.path.join(self.local.projStylesFolder, self.projConfig['Managers']['usfm_Style']['mainStyleFile'])
            custSty = os.path.join(self.local.projStylesFolder, self.projConfig['Managers']['usfm_Style']['customStyleFile'])
            if os.path.isfile(globSty) :
                editDocs.append(globSty)
            if os.path.isfile(custSty) :
                editDocs.append(custSty)

            # FIXME: This next part is hard-wired, be nice to do better
            fileName = 'xetex_settings_usfm-ext.tex'
            macExt = os.path.join(self.local.projMacrosFolder, 'usfmTex', fileName)
            editDocs.append(macExt)

        # Look at system setting files
        if sys :
            editDocs.append(self.local.userConfFile)

        # Pull up our docs in the editor
        if len(editDocs) > 1 :
            subprocess.call(editDocs)
            self.log.writeToLog('EDIT-040', [cName])
        else :
            self.log.writeToLog('EDIT-030')




