from module_a.gui import RobotGui
from motion.core import RobotControl, LedLamp, Waypoint, InterpreterStates

from fake_api.fake_motion import RobotControl, LedLamp, Waypoint
from fake_api.fake_motion_program import MotionProgram
import time

class RobotAutoGui(RobotGui):
  def __init__(self):
    super().__init__()
    self.init_autoui()
    self.programm = []
    
  def init_autoui(self):
    self.ui.start_programm_button.clicked.connect(self.start_programm)
    # self.ui.pause_programm_button.clicked.connect(self.pause_programm)
    # self.ui.stop_programm_button.clicked.connect(self.stop_programm)
    self.ui.clear_programm_button.clicked.connect(self.clear_programm)
    self.ui.add_coordinate_auto.clicked.connect(self.add_coordinate)
    self.ui.add_griper_status_auto.clicked.connect(self.add_gripper)
    
  # def pause_programm(self):
  #   self.robot.pause()
  # def stop_programm(self):
  #   self.robot.stop()
  
  def start_programm(self):
    self.logger.info('Робот начал выполнение программы')
    if self.ui.cycle_programm_chekbox.isChecked():
      cycles = self.ui.cycles_amount.value()
      for i in range(cycles):
        self.logger.info(f'Начинается выполнение цикла {i+1}.')
        self.perform_programm()
        self.logger.info(f'Выполнение цикла {i+1} завершено. Выполнено {i+1}/{cycles} циклов.')
    else:
      self.perform_programm()
    self.logger.info('Робот закончил выполнение программы')
    
    
  def perform_programm(self):
    self.update_status('ON')
    for el in self.programm:
      if type(el) is str:
        if el == 'GRIPPER_ON':
          self.robot.toolON()
          self.logger.info('Гриппер включен')
        elif el == 'GRIPPER_OFF':
          self.robot.toolOFF()
          self.logger.info('Гриппер выключен')
      else:
        if self.robot.getManipulability() == 0:
            self.logger.critical('Движение невозможно, критическая ситуация')
            self.emergency_stop()
            return
        self.robot.moveToPointL(el)
        self.logger.info(f'Текущие координаты: {self.robot.getToolPosition()}')
      # time.sleep(1)
      self.update_status('WAIT')
    
    
  def clear_programm(self):
    self.programm = []
    self.ui.listWidget.clear()
    self.logger.info('Программа очищена')
    
    
  def add_coordinate(self):
    coordinate = []
    for row in range(self.ui.cords_auto.rowCount()):
      for column in range(self.ui.cords_auto.columnCount()):
        if self.ui.cords_auto.item(row, column) == None:
          self.logger.error('Коордитана не заполнена или заполнена неправильно')
          return
        coordinate.append(float(self.ui.cords_auto.item(row, column).data(2)))
        
    bounds = self.config.MAX_AREA_CORDS.get('CARTESIAN_MODE')
    
    if not bounds:
        self.logger.error(f'Нет данных о границах режима: CARTESIAN MODE')
        return
      
    min_b, max_b = bounds['min'], bounds['max']
      
    for i in range(len(coordinate)):
      if not (min_b[i] <= coordinate[i] <= max_b[i]):
          self.logger.info(f'Превышение границ в координате {i+1}. Чтобы добавить координату в программу перемещения убедитесь, что она соответствует границам рабочей зоны')
          return
    
    coordinate = Waypoint(coordinate)
    print(type(coordinate))
    self.programm.append(coordinate)
    self.logger.info(f'Точка {coordinate} добавлена в программу')
    self.ui.listWidget.addItem(f'Точка {coordinate}')
      
    
  def add_gripper(self):
    if self.ui.gripper_status_for_auto.currentText() == 'Включить гриппер':
      self.ui.listWidget.addItem(f'Включение гриппера')
      self.logger.info(f'Действие "Включение гриппера" добавлено в программу')
      self.programm.append('GRIPPER_ON')
    elif self.ui.gripper_status_for_auto.currentText() == 'Выключить гриппер':
      self.ui.listWidget.addItem(f'Выключение гриппера')
      self.logger.info(f'Действие "Выключение гриппера" добавлено в программу')
      self.programm.append('GRIPPER_OFF')