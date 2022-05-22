from PyQt5 import QtWidgets

from desktop_plugin.UI.password_enter.password_enter_dialog import password_enter_dialog


class password_enter_dialog_controller(QtWidgets.QDialog):

    def __init__(self):
        super(password_enter_dialog_controller, self).__init__()
        self.__ui = password_enter_dialog()
        self.__ui.setupUi(self)
        self.password = ''

    def OKButton_Clicked(self):
        self.password = self.__ui.lineEdit.text()
        self.close()
