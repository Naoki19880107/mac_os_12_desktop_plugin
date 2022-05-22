import json

from PyQt5 import QtWidgets, QtCore, QtGui

from desktop_plugin.Service.CPU.CPU import CPU
from desktop_plugin.Service.Memory.Memory import Memory
from desktop_plugin.Service.lunar.lunar import Lunar
from desktop_plugin.Thread.HardwareInfo_Thread import HardwareInfo_Thread
from desktop_plugin.Service.OSVersion.OSVersion import OSVersion
from desktop_plugin.UI.Tray.Tray import Tray
from desktop_plugin.UI.desktop_plugin.desktop_plugin_ui import desktop_plugin_ui
from desktop_plugin.Thread.weatherThread import weatherThread


class desktop_plugin_controller_controller(QtWidgets.QMainWindow):

    def __init__(self):
        super(desktop_plugin_controller_controller, self).__init__()
        self.__desktop_plugin_ui = desktop_plugin_ui()
        self.__desktop_plugin_ui.setupUi(self)
        self.__desktop_plugin_ui.system_version_output_label.setText(OSVersion.getVersion())
        self.__desktop_plugin_ui.system_version_name_output_label.setText(
            OSVersion.getVersionName(OSVersion.getVersion()))
        self.__desktop_plugin_ui.cpu_output_label.setText(CPU.getCPUName())
        self.__tray = Tray(self)
        self.__tray.show()
        self.__timer_calendar = QtCore.QTimer(parent=self)
        self.__timer_calendar.timeout.connect(self.__show_Info)
        self.__timer_calendar.start(1000)
        self.__HardwareInfo_Thread = HardwareInfo_Thread(Memory.get_physical_memory())
        self.__HardwareInfo_Thread.paint_trigger.connect(self.__paint_HardwareInfo)
        self.__HardwareInfo_Thread.start()
        self.__weather_Thread = weatherThread()
        self.__weather_Thread.paint_trigger.connect(self.__paint_weather)
        self.__weather_Thread.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.__timer_calendar.stop()
        # self.__HardwareInfo_Thread.quit()
        self.__HardwareInfo_Processing.join()
        self.__lunar_Thread.quit()
        self.__weather_Thread.quit()

    def __show_Info(self):
        self.__desktop_plugin_ui.time_label.setText('')
        datetime: QtCore.QDateTime = QtCore.QDateTime.currentDateTime()
        self.__desktop_plugin_ui.time_label.setText(datetime.toString("hh:mm:ss"))
        self.__desktop_plugin_ui.date_label.setText(datetime.toString("yyyy年MM月dd日") + "\n" + Lunar.getLunar())
        self.__desktop_plugin_ui.calendarWidget.setSelectedDate(QtCore.QDate.currentDate())

    def __paint_weather(self,weather:str):
        self.__desktop_plugin_ui.weather_label.setText(weather)

    def __paint_HardwareInfo(self,hardware_info_str:str):
        hardware_info:tuple[int,str,int] = tuple(json.loads(hardware_info_str))
        idle_percent,temp,used_memory_percent = hardware_info
        self.__desktop_plugin_ui.cpu_idle_progressBar.setValue(idle_percent)
        self.__desktop_plugin_ui.cpu_temp_output_label.setText(temp)
        self.__desktop_plugin_ui.memory_progressBar.setValue(used_memory_percent)
