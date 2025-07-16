from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import QtCore
from motion.core import RobotControl, LedLamp, Waypoint, InterpreterStates
from fake_motion import RobotControl, LedLamp, Waypoint
from core.design import Ui_MainWindow
from config import Config
from utils.logger import QtLogHandler, setup_logger
from math import degrees, radians

class RobotControlGui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.robot = RobotControl()
        self.lamp = LedLamp()
        self.init_ui()
        self.setup_logging()
        self.connect_all()
        

        self.robot.manualCartMode()

    def update_status(self, state: str):
        states = {
            'ON': {'code': '0100', 'label':'В работе'},
            'WAIT': {'code': '1000', 'label':'Ожидание'},
            'PAUSE':{'code': '0010', 'label':'Приостановлен'},
            'EMERGENCY':{'code': "0001", 'label':'Аварийная остановка'},
            'BLACKOUT':{'code': "0000", 'label':'Робот выключен'}
        }

        if state in states:
            self.lamp.setLamp(states[state]['code'])
            self.ui.state_data_label.setText(states[state]['label'])


    def connect_all(self):
        if self.robot.connect():
            self.logger.info('Робот включен')
            self.update_status('WAIT')
        else:
            self.logger.error('Робот не подключен')

    def setup_logging(self):
        self.logger = setup_logger(__name__)
        for handler in self.logger.handlers:
            if isinstance(handler, QtLogHandler):
                handler.log_signal.connect(self.append_log)
                break

    def append_log(self, text):
        self.ui.logs_plaintext.appendPlainText(text)
        scrollbar = self.ui.logs_plaintext.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.OnOff_button.clicked.connect(self.on_off_robot)
        self.ui.Pause_button.clicked.connect(self.pause_robot)
        self.ui.Emergency_button.clicked.connect(self.emergency_stop)
        self.ui.move_style.currentTextChanged.connect(self.update_move_variant)
        self.ui.Gripper_button.clicked.connect(self.gripper_switch)
        
        self.table_timer = QtCore.QTimer(self)
        self.table_timer.timeout.connect(self.update_status_table)
        self.table_timer.start(1000)  # обновление каждую секунду



        for i in range(1,7):
            getattr(self.ui, f'motor_{i}_minus').clicked.connect(lambda _, m=i: self.update_motor(m, -0.05))
            getattr(self.ui, f'motor_{i}_plus').clicked.connect(lambda _, m=i: self.update_motor(m, 0.05))

    def on_off_robot(self):
        # вариант с приводами
        if self.ui.OnOff_button.text() == 'Вкл':
            self.robot.engage()
            self.robot.moveToStart()
            self.ui.OnOff_button.setText('Выкл')
            self.logger.info('Приводы активированы')
            self.update_status('WAIT')
        elif self.ui.OnOff_button.text() == 'Выкл':
            self.robot.disengage()
            self.ui.OnOff_button.setText('Вкл')
            self.logger.info('Приводы отключены')
            self.update_status('BLACKOUT')

        # вариант с программами
        # if self.ui.OnOff_button.text() == 'Вкл':
        #     self.robot.play()
        #     self.ui.OnOff_button.setText('Выкл')
        #     self.logger.info('Приводы активированы')
        # elif self.ui.OnOff_button.text() == 'Выкл':
        #     self.robot.moveToStart()
        #     self.ui.OnOff_button.setText('Вкл')
        #     self.logger.info('Приводы отключены')
        
    def pause_robot(self):
        self.robot.pause()
        self.update_status('PAUSE')

    def emergency_stop(self):
        self.robot.stop()
        self.logger.critical("Аварийная остановка")
        self.update_status('EMERGENCY')

    
    def update_motor(self, motor_number, delta):
        idx = motor_number-1
        mode = self.robot.getRobotMode()
        bounds = self.config.MAX_AREA_CORDS.get(mode)

        if self.robot.getManipulability() == 0:
            self.logger.critical('Движение невозможно, критическая ситуация')
            self.emergency_stop()
            return
        
        if not bounds:
            self.logger.error(f'Нет данных о границах режима: {mode}')
            return
        
        min_b, max_b = bounds['min'], bounds['max']

        if mode == 'CARTESIAN_MODE':
            position = self.robot.getToolPosition()
        elif mode == 'JOINT_MODE':
            position = self.robot.getMotorPositionRadians()

        position[idx] = round(position[idx]+delta, 2)

        for i in range(len(position)):
            if not (min_b[i] <= position[i] <= max_b[i]):
                self.logger.critical(f'Превышение границ в координате {i+1}')
                self.emergency_stop()
                return
            
        self.update_status('ON')
        wp = Waypoint(position)
        if mode == 'CARTESIAN_MODE':
            self.robot.moveToPointL(wp)
        elif mode == 'JOINT_MODE':
            self.robot.moveToPointJ(wp)
        self.update_status('WAIT')
        self.logger.info(f'Текущие координаты: {position}')

    def update_status_table(self):
        temp = self.robot.getActualTemperature()
        tiks = self.robot.getMotorPositionTick()
        rads = self.robot.getMotorPositionRadians()
        degs = [round(degrees(i), 2) for i in rads]
 
        print(temp)

        for col in range(6):
            self.ui.tableWidget.setItem(0, col, QTableWidgetItem(str(tiks[col])))
            self.ui.tableWidget.setItem(1, col, QTableWidgetItem(str(rads[col])))
            self.ui.tableWidget.setItem(2, col, QTableWidgetItem(str(degs[col])))
            self.ui.tableWidget.setItem(3, col, QTableWidgetItem(str(f'{temp} C')))


    def gripper_switch(self):
        if self.ui.Gripper_button.text() == 'Схватить':
            self.robot.toolON()
            self.ui.Gripper_button.setText('Отпустить')
            self.logger.info('Гриппер включен')
        elif self.ui.Gripper_button.text() == 'Отпустить':
            self.robot.disengage()
            self.ui.Gripper_button.setText('Схватить')
            self.logger.info('Гриппер выключен')
    
    def update_move_variant(self):
        if self.ui.move_style.currentText() == 'Move J':
            for i in range(1,7):
                getattr(self.ui, f'motor_label_{i}').setText(f'Мотор {i}')

            if self.robot.manualJointMode():
                self.logger.info(self.robot.getRobotMode())

        if self.ui.move_style.currentText() == 'Move L':
            self.ui.motor_label_1.setText("X")
            self.ui.motor_label_2.setText("Y")
            self.ui.motor_label_3.setText("Z")
            self.ui.motor_label_4.setText("rx")
            self.ui.motor_label_5.setText("ry")
            self.ui.motor_label_6.setText("rz")

            if self.robot.manualCartMode():
                self.logger.info(self.robot.getRobotMode())

