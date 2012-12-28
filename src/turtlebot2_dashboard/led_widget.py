import rospy
from functools import partial

from kobuki_msgs.msg import Led

from rqt_robot_dashboard.widgets import MenuDashWidget

class LedWidget(MenuDashWidget):
    def __init__(self, topic):
        self._pub = rospy.Publisher(topic, Led) 

        self._off_icon = ['bg-grey.svg', 'ic-breaker.svg']
        self._green_icon = ['bg-green.svg', 'ic-breaker.svg']
        self._orange_icon = ['bg-red.svg', 'ic-breaker.svg']
        self._red_icon = ['bg-red.svg', 'ic-breaker.svg']

        icons = [self._off_icon, self._green_icon, self._orange_icon, self._red_icon]
        super(LedWidget, self).__init__(topic, icons=icons)

        self.add_action('Off', partial(self.update_state, 0))
        self.add_action('Green', partial(self.update_state, 1))
        self.add_action('Orange', partial(self.update_state, 2))
        self.add_action('Red', partial(self.update_state, 3))

    def update_state(self, state):
        super(LedWidget, self).update_state(state)

        self._pub.publish(Led(state))

    def close(self):
        self._pub.unregister()
    
