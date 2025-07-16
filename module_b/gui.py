from module_a.gui import RobotGui
from motion.core import RobotControl, LedLamp, Waypoint, InterpreterStates
from motion.robot_control.motion_program import MotionProgram, PoseTransformer

from fake_api.fake_motion import RobotControl, LedLamp, Waypoint
from fake_api.fake_motion_program import MotionProgram

class RobotAutoGui(RobotGui):
  def __init__(self):
    super().__init__()
    self.motion_programm = MotionProgram(self.robot.__req)
    self.init_autoui()
    
    
  def init_autoui(self):
    self.ui.start_programm_button.ckicked(self.start_programm)
    self.ui.pause_programm_button.ckicked(self.pause_programm)
    self.ui.stop_programm_button.ckicked(self.stop_programm)
    self.ui.reset_programm_button.ckicked(self.reset_programm)
    self.ui.add_coordinate_auto.clicked(self.add_coordinate)
    self.ui.add_griper_status_auto.clicked(self.add_gripper)
    
  def start_programm(self):
    self.robot.play()
  def pause_programm(self):
    self.robot.pause()
  def stop_programm(self):
    self.robot.stop()
  def reset_programm(self):
    self.robot.reset()
    
    
  def add_coordinate(self):
    coordinate = []
    for row in range(self.ui.cords_auto.rowCount()):
      for column in range(self.ui.cords_auto.columnCount()):
        coordinate.append(self.ui.cords_auto.item(row, column))
      
    
  def add_gripper(self):
    if self.ui.gripper_status_for_auto.currentText() == 'Включить гриппер':
      pass
    elif self.ui.gripper_status_for_auto.currentText() == 'Выключить гриппер':
      pass