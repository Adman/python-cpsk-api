# -*- coding: utf-8 -*-
import cpsk
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

bus_routes = cpsk.get_routes('TO', 'BA', vehicle='bus')
for b in bus_routes:
    print b

train_routes = cpsk.get_routes('NR', 'TO', vehicle='vlak')
for t in train_routes:
    print t

routes = cpsk.get_routes('KE', 'TO')
for r in routes:
    print r
