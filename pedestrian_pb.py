from time import sleep

from pydnp3 import opendnp3
from master import MyMaster, MyLogger, AppChannelListener, SOEHandler, MasterApplication

app = MyMaster(log_handler=MyLogger(), listener=AppChannelListener(), soe_handler=SOEHandler(), master_application=MasterApplication())

while True:
    app.master.send_select_and_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON),
                                                         4,
                                                         command_callback)
    sleep(5)
    app.master.send_select_and_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_OFF),
                                                         4,
                                                         command_callback)
