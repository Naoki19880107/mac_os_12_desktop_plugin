from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from desktop_plugin.Service.weather.weather_requests import weather_requests


class weatherThread(QThread):
    paint_trigger = pyqtSignal(str)

    def __init__(self):
        super(weatherThread, self).__init__()
        self.__is_running = False

    def run(self) -> None:
        self.__is_running = True
        while True:
            if self.__is_running:

                self.paint_trigger.emit(weather_requests.getWeather())
                sleep(3600)
            else:
                break

    def quit(self) -> None:
        self.__is_running = False
        super(weatherThread, self).quit()

