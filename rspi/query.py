
#import humongolus as orm
from influxdb import InfluxDBClient

host = 'crtlabsdev.realtors.org'
port = 8086
user = 'admin'
password = 'admin'
db_name = 'lablog'

db = InfluxDBClient(host, port, user, password, db_name)
result = db.query("SELECT MEAN(value) as value FROM lablog")
#print("Result: {0}".format(result))
rlist = result.get_points
print rlist


