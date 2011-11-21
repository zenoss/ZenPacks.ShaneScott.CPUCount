from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
import logging
log = logging.getLogger('zen.CPUCount')


class CPUCount(ZenPackPersistence, SnmpPlugin):

      ZENPACKID = 'ZenPacks.ShaneScott.CPUCount'

      cMonOperEntry = {
              '.1': 'hrProcessorFrwID',
      }

      snmpGetTableMaps = (
              GetTableMap('MonOperEntry', '.1.3.6.1.2.1.25.3.3.1', cMonOperEntry),
      )

      def process(self, device, results, log):
          """
          collect CPU information from device
          """
          log.info('processing %s for device %s', self.name(), device.id)
          log.info('CPU (entries) results: %r', results)

          getdata, tabledata = results
          table = tabledata.get('MonOperEntry')
          count=0

          for info in table.values():
              count=count+1

          om = self.objectMap(getdata)

          log.info('Found a count of %s logical CPUs!', count)
          om.setCpuCount = count
          return om