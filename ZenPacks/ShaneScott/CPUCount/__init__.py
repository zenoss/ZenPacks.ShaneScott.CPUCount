import Globals
import logging
import os

log = logging.getLogger('zen.CPUCount')

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.ZenMenu import ZenMenu
from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.Utils import monkeypatch

class ZenPack(ZenPackBase):
    def install(self, app):
        super(ZenPack, self).install(app)
        log.info('Cleaning up old values')
        self.cleanup(app)
        log.info('Creating custom schema')
        self.createCustomSchema()
        lnxCpuCount = app.dmd.Devices.createOrganizer('/Server/Linux')
        solCpuCount = app.dmd.Devices.createOrganizer('/Server/Solaris')
        lnxPlugins=[]
        lnxServer = app.dmd.findChild('Devices/Server/Linux')
        solPlugins=[]
        solServer = app.dmd.findChild('Devices/Server/Solaris')
        for lnxPlugin in lnxServer.zCollectorPlugins:
            lnxPlugins.append(lnxPlugin)

        for solPlugin in solServer.zCollectorPlugins:
            solPlugins.append(solPlugin)

        lnxPlugins.append('CPUCount')
        solPlugins.append('CPUCount')

        lnxCpuCount.setZenProperty('zCollectorPlugins', lnxPlugins)
        solCpuCount.setZenProperty('zCollectorPlugins', solPlugins)


    def remove(self, app, leaveObjects=False):
        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)
        if not leaveObjects:
            log.info('Removing custom schema')
            self.removeCustomSchema()
            log.info('Cleaning up old values')
            self.cleanup(app)


    def createCustomSchema(self):
        if not self.dmd.Devices.hasProperty('CpuCount'):
            self.dmd.Devices._setProperty('CpuCount', 1, label='Logical CPU count', type='int')

        self.dmd.Devices.setZenProperty('CpuCount', 1)


    def removeCustomSchema(self):
        if self.dmd.Devices.hasProperty('CpuCount'):
            self.dmd.Devices.deleteZenProperty('CpuCount')


    def cleanup(self, app):
        for i in app.dmd.Devices.getSubDevices():
            try:
                del i.CpuCount
            except:
                pass


@monkeypatch('Products.ZenModel.Device.Device')
def setCpuCount(self, CpuCount):
    setattr(self, 'CpuCount', CpuCount)


@monkeypatch('Products.ZenModel.Device.Device')
def getCpuCount(self):
    if hasattr(self, 'CpuCount'):
        return self.CpuCount
    else:
        return 1