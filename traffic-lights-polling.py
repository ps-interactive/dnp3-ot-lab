from time import sleep

from pydnp3 import opendnp3
from master import MyMaster, MyLogger, AppChannelListener, SOEHandler, MasterApplication

app = MyMaster(log_handler=MyLogger(), listener=AppChannelListener(), soe_handler=SOEHandler(), master_application=MasterApplication())

while True:
    app.master.ScanRange(opendnp3.GroupVariationID(10, 2), 0, 4, opendnp3.TaskConfig().Default())
    sleep(1)
