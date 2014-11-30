import cpsk

bus_routes = cpsk.get_routes('TO', 'BA', vehicle='bus')
for b in bus_routes:
    print b.__repr__()

train_routes = cpsk.get_routes('NR', 'TO', vehicle='vlak')
for t in train_routes:
    print t.__repr__()

routes = cpsk.get_routes('Bratislava', 'Zilina')
for r in routes:
    print r.__repr__()
