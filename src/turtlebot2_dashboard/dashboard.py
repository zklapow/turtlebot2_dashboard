import roslib;roslib.load_manifest('turtlebot2_dashboard')
import rospy

import diagnostic_msgs

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

        self._dashboard_agg_sub = rospy.Subscriber('diagnostics_agg', diagnostic_msgs.msg.DiagnosticArray, self.dashboard_callback)

    def get_widgets(self):
        leds = [LedWidget('/mobile_base/commands/led1'), LedWidget('/mobile_base/commands/led2')]

        return [[MonitorDashWidget(self.context), ConsoleDashWidget(self.context), self._motor_widget], leds]

    def dashboard_callback(self, msg):
        self._dashboard_message = msg
        self._last_dashboard_message_time = rospy.get_time()

        for status in msg.status:
            if status.name == "/Kobuki/Motor State":
                motor_state = int(status.values[0].value)
                self._motor_widget.update_state(motor_state)
