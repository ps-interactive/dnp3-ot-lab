import cmd
import logging
import sys

from datetime import datetime
from pydnp3 import opendnp3, openpal
from master import MyMaster, MyLogger, AppChannelListener, SOEHandler, MasterApplication
from master import command_callback, restart_callback
from time import sleep

stdout_stream = logging.StreamHandler(sys.stdout)
stdout_stream.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))

_log = logging.getLogger(__name__)
_log.addHandler(stdout_stream)
_log.setLevel(logging.DEBUG)


class MasterCmd(cmd.Cmd):
    """
        Create a DNP3Manager that acts as the Master in a DNP3 Master/Outstation interaction.

        Accept command-line input that sends commands and data to the Outstation,
        using the line-oriented command interpreter framework from the 'cmd' Python Standard Library.
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'master> '   # Used by the Cmd framework, displayed when issuing a command-line prompt.
        self.application = MyMaster(log_handler=MyLogger(),
                                    listener=AppChannelListener(),
                                    soe_handler=SOEHandler(),
                                    master_application=MasterApplication())

    def startup(self):
        """Display the command-line interface's menu and issue a prompt."""
        print('Welcome to the DNP3 master request command line. Supported commands include:')
        self.do_menu('')
        self.cmdloop('Please enter a command.')
        exit()

    def do_menu(self, line):
        """Display a menu of command-line options. Command syntax is: menu"""

        print('\thelp\t\tDisplay command-line help.')
        print('\tem_on\t\tActivate Emergency mode.')
        print('\tem_off\t\tDeactivate Emergency Mode.')
        print('\tped_pb\t\tSimulate a pedestrian pushbutton press.')
        print('\tstatus\t\tRead the status of selected points')
        print('\twrite_time\tWrite a TimeAndInterval to the outstation.')
        print('\tquit')

    def do_em_on(self, line):
        """Send a DirectOperate BinaryOutput (group 12) index 3 LATCH_ON to the Outstation."""
        self.application.send_direct_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON),
                                                     3,
                                                     command_callback)
    def do_em_off(self, line):
        """Send a DirectOperate BinaryOutput (group 12) index 3 LATCH_OFF to the Outstation."""
        self.application.send_direct_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_OFF),
                                                     3,
                                                     command_callback)

    def do_ped_pb(self, line):
        """Send a DirectOperate BinaryOutput (group 12) index 4 LATCH_ON to the Outstation, then sleep for 6 seconds 
        and finally send a DirectOperate BinaryOutput (group 12) index 4 LATCH_OFF to the Outstation """
        self.application.send_direct_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON),
                                                     4,
                                                     command_callback)
        sleep(6)
        self.application.send_direct_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_OFF),
                                                     4,
                                                     command_callback)

    def do_status(self, line):
        """Do an ad-hoc scan of all points (group 10, variation 2, indexes 0-4). """
        self.application.master.ScanRange(opendnp3.GroupVariationID(10, 2), 0, 4, opendnp3.TaskConfig().Default())

    def do_write_time(self, line):
        """Write a TimeAndInterval to the Outstation. Command syntax is: write_time"""
        millis_since_epoch = int((datetime.now() - datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)
        self.application.master.Write(opendnp3.TimeAndInterval(opendnp3.DNPTime(millis_since_epoch),
                                                               100,
                                                               opendnp3.IntervalUnits.Seconds),
                                      0,                            # index
                                      opendnp3.TaskConfig().Default())

    def do_quit(self, line):
        """Quit the command-line interface. Command syntax is: quit"""
        self.application.shutdown()
        exit()


def main():
    cmd_interface = MasterCmd()
    _log.debug('Initialization complete. In command loop.')
    cmd_interface.startup()
    _log.debug('Exiting.')


if __name__ == '__main__':
    main()
