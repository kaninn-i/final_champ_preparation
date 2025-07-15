from module_a.gui import RobotControlGui
import sys
from PyQt5.QtWidgets import QApplication



def main():
    app = QApplication(sys.argv)
    window = RobotControlGui()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()