import roslib;roslib.load_manifest('turtlebot2_dashboard')
import rospy

import diagnostic_msgs
from linux_hardware.msg import LaptopChargeStatus

from rqt_robot_dashboard.dashboard import Dashboard
from rqt_robot_dashboard.widgets import MonitorDashWidget, ConsoleDashWidget, MenuDashWidget, BatteryDashWidget, IconToolButton, NavViewDashWidget
from QtGui import QMessageBox, QAction
from python_qt_binding.QtCore import QSize

from .led_widget import LedWidget
from .motor_widget import MotorWidget

class TurtlebotDashboard(Dashboard):
    def setup(self, context):
        self.message = None

        self._dashboard_message = None
        self._last_dashboard_message_time = 0.0
        
        self._motor_widget = MotorWidget('/mobile_base/commands/motor_power')
        self._laptop_bat = BatteryDashWidget("Laptop")
        self._kobuki_bat = BatteryDashWidget("Kobuki")

        self._dashboard_agg_sub = rospy.Subscriber('diagnostics_agg', diagnostic_msgs.msg.DiagnosticArray, self.dashboard_callback)
        self._laptop_bat_sub = rospy.Subscriber('/laptop_charge', LaptopChargeStatus, self.laptop_cb)

    def get_widgets(self):
        leds = [LedWidget('/mobile_base/commands/led1'), LedWidget('/mobile_base/commands/led2')]

        return [[MonitorDashWidget(self.context), ConsoleDashWidget(self.context), self._motor_widget], leds, [self._laptop_bat, self._kobuki_bat]]

    def dashboard_callback(self, msg):
        self._dashboard_message = msg
        self._last_dashboard_message_time = rospy.get_time()

        for status in msg.status:
            if status.name == "/Kobuki/Motor State":
                motor_state = int(status.values[0].value)
                self._motor_widget.update_state(motor_state)

            elif status.name == "/Power System/Battery":
                for value in status.values:
                    if value.key == 'Percent':
                        self._kobuki_bat.update_perc(float(value.value))
                        self._kobuki_bat.update_time(float(value.value))
                    elif value.key == "State":
                        if value.value == "Charging":
                            self._kobuki_bat.set_charging(True)
                        else:
                            self._kobuki_bat.set_charging(False)

    def laptop_cb(self, msg):
        self._laptop_bat.update_perc(float(msg.percentage))
        self._laptop_bat.update_time(float(msg.percentage))
        self._laptop_bat.set_charging(bool(msg.charge_state))
