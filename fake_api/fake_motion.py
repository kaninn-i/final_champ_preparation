import time
import random
from math import radians

class Waypoint:
    def __init__(self, coords):
        self.coords = coords
        print(f"[FAKE] Waypoint создан: {coords}")

    def __repr__(self):
        return f"Waypoint({self.coords})"


class LedLamp:
    def __init__(self, ip='192.168.2.101', port=8890):
        self.status = "0000"
        print(f"[FAKE] LedLamp создана для IP {ip}:{port}")

    def setLamp(self, status):
        if len(status) != 4 or not all(c in "01" for c in status):
            print("[FAKE][ERROR] Некорректный формат статуса лампы")
            return
        self.status = status
        print(f"[FAKE] Лампа установлена в состояние: {status}")


class RobotControl:
    def __init__(self, ip='192.168.2.100', port='5568:5567', login='*', password='*'):
        print(f"[FAKE] RobotControl инициализирован для IP {ip}:{port}")
        self.connected = False
        self.joint_mode = False
        self.cart_mode = False
        self.tool_on = False
        self.position = [0.0] * 6

    def connect(self):
        self.connected = True
        print("[FAKE] Соединение с роботом установлено")
        return True

    def engage(self):
        print("[FAKE] Приводы активированы")
        return True

    def disengage(self):
        print("[FAKE] Приводы отключены")
        return True

    def manualCartMode(self):
        self.cart_mode = True
        self.joint_mode = False
        print("[FAKE] Включен режим картезианского управления")
        return True

    def manualJointMode(self):
        self.joint_mode = True
        self.cart_mode = False
        print("[FAKE] Включен режим суставного управления")
        return True

    def setJointVelocity(self, velocity):
        print(f"[FAKE] Суставная скорость установлена: {velocity}")
        return True

    def setCartesianVelocity(self, velocity):
        print(f"[FAKE] Картезианская скорость установлена: {velocity}")
        return True

    def moveToStart(self):
        print("[FAKE] Робот перемещён в стартовую позицию")
        return True

    def moveToPointJ(self, waypoint_list, rotational_velocity=3.18, rotational_acceleration=6.37):
        print(f"[FAKE] Движение к точке (Joint): {waypoint_list}")
        self.position = waypoint_list[-1].coords if waypoint_list else self.position
        return True

    def moveToPointL(self, *args, **kwargs):
        print("[FAKE] Линейное движение (MoveL) выполнено")
        return True

    def moveToPointC(self, *args, **kwargs):
        print("[FAKE] Круговое движение (MoveC) выполнено")
        return True

    def play(self):
        print("[FAKE] Программа запущена")
        return "PROGRAM_RUNNING"

    def pause(self):
        print("[FAKE] Программа на паузе")
        return "PAUSED"

    def stop(self):
        print("[FAKE] Программа остановлена")
        return "STOPPED"

    def reset(self):
        print("[FAKE] Программа сброшена")
        return "RESET"

    def toolON(self):
        self.tool_on = True
        print("[FAKE] Инструмент включён")
        return True

    def toolOFF(self):
        self.tool_on = False
        print("[FAKE] Инструмент выключен")
        return True

    def getRobotMode(self):
        return "JOINT_MODE" if self.joint_mode else "CARTESIAN_MODE" if self.cart_mode else "UNKNOWN"

    def getRobotState(self):
        return "CONNECTED" if self.connected else "DISCONNECTED"

    def getActualStateOut(self):
        return "PROGRAM_READY"

    def getMotorPositionTick(self):
        print("[FAKE] Возврат текущей позиции моторов в тиках")
        return [int(p * 1000) for p in self.position]

    def getToolPosition(self):
        print("[FAKE] Возврат текущей позиции инструмента")
        return self.position

    def getMotorPositionRadians(self):
        print("[FAKE] Возврат текущей позиции моторов в радианах")
        return self.position

    def getManipulability(self):
        value = round(random.uniform(0.3, 1.0), 2)
        print(f"[FAKE] Манипулируемость: {value}")
        return value

    def getActualTemperature(self):
        temp = round(random.uniform(30.0, 60.0), 1)
        print(f"[FAKE] Температура моторов: {temp} °C")
        return temp
