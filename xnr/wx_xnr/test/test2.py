#-*- coding: utf-8 -*-
import sys
sys.path.append('../../')
from xnr.global_utils import r

r.set('hmc_name', 'hmc')

print r.get('hmc_name')