from module_a.gui import RobotGui
from module_b.gui import RobotAutoGui
import sys
from PyQt5.QtWidgets import QApplication



def main():
    app = QApplication(sys.argv)
    # window = RobotGui()
    window = RobotAutoGui()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()