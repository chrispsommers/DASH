from abc import ABC, abstractmethod
from copy import deepcopy
import os, sys
from dflt_params import *
from munch import DefaultMunch
from datetime import datetime
import ipaddress
import macaddress
ipp = ipaddress.ip_address
macM = macaddress.MAC
from confutils import *

class ConfBase(ABC):

    def __init__(self, name='base', params={}, args=None):
        self._dictname = name
        self.dflt_params = deepcopy(dflt_params)
        self.cooked_params = {}
        self.mergeParams(params)
        self.numYields = 0
        if args is not None:
            self.args = args
        
        self.subgens = []

    def mergeParams(self, params):
        # Merge provided params into/onto defaults
        self.params_dict = deepcopy(self.dflt_params)
        self.params_dict.update(params)

        # make scalar attributes for speed & brevity (compared to dict)
        # https://stackoverflow.com/questions/1305532/how-to-convert-a-nested-python-dict-to-object
        self.cookParams()
        self.params = DefaultMunch.fromDict(self.params_dict)
        # print ('%s: self.params=' % self._dictname, self.params)
        self.cooked_params = DefaultMunch.fromDict(self.cooked_params_dict)
        # print ("cooked_params = ", self.cooked_params)

    def cookParams(self):
        self.cooked_params_dict = {}
        for ip in [
                    'IP_STEP1',
                    'IP_STEP2',
                    'IP_STEP3',
                    'IP_STEP4',
                    'IP_STEPE'
                ]:
            self.cooked_params_dict[ip] = int(ipp(self.params_dict[ip]))
        for ip in [
                    'IP_L_START',
                    'IP_R_START',
                    'PAL',
                    'PAR'
                ]:
            self.cooked_params_dict[ip] = ipp(self.params_dict[ip])
        for mac in [
                    'MAC_L_START',
                    'MAC_R_START'
                ]:
            self.cooked_params_dict[mac] = macM(self.params_dict[mac])

    @abstractmethod
    def items(self):
        pass

    # expensive - runs generator
    def itemCount(self):
        return len(self.items())

    def itemsGenerated(self):
        """ Last count of # yields, accumulates each yield until cleared"""
        return self.numYields

    def subItemsGenerated(self):
        """ Sum of subgenerator items"""
        return sum(c.itemsGenerated()+ c.subItemsGenerated() for c in self.subgens)

    def clearCount(self):
        """ Reset count of # yields"""
        self.numYields=0

    def count(self):
        """ Increment of # yields"""
        self.numYields+=1

    def dictName(self):
        return self._dictname

    def toDict(self):
        return ({self._dictname: self.items()})

    def getParams(self):
        return self.params_dict

    def getMeta(self, message=''):
        """Generate metadata. For reference, could also add e.g. data to help drive tests"""
        return { 'meta': { 
                    'tstamp': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    'msg': message,
                    'params': self.getParams()
                }
            }

    def __str__(self):
            """String repr of all items in generator"""
            if len(self.subgens) > 0:
                subtotal = sum(c.itemsGenerated() for c in self.subgens)

                return '%s: %d items, %d sub-items:\n' % \
                            (self.dictName(), self.itemsGenerated(), self.subItemsGenerated()) + \
                        '    ' + \
                        '\n    '.join(c.__str__() for c in self.subgens)
            else:
               return '%s: %d items' % (self.dictName(), self.itemsGenerated())

    def pretty(self):
        pprint.pprint(self.toDict())

    def log_verbose(self, msg=''):
        log_msg(msg, self.args.verbose)

    def log_details(self, msg=''):
        log_msg(msg, self.args.detailed_stats)

    def log_mem(self, msg=''):
        log_memory(msg,  self.args.detailed_stats)

