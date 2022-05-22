import json
from time import sleep
from PyQt5.QtCore import pyqtSignal, QThread

from desktop_plugin.Service.CPU.CPU import CPU
from desktop_plugin.Service.Memory.Memory import Memory


class HardwareInfo_Thread(QThread):
    paint_trigger = pyqtSignal(str)

    def __init__(self, all_memory):
        super(HardwareInfo_Thread, self).__init__()
        self.__all_memory = all_memory
        self.__is_running = False

    def run(self) -> None:
        self.__is_running = True
        while True:
            if self.__is_running:
                self.paint_trigger.emit(
                    json.dumps((int(CPU.getcpuidle()), CPU.getcputemp(),
                                int((self.__all_memory[0] - Memory.get_unused_memory()[0]) / self.__all_memory[
                                    0] * 100))))
                sleep(1)
            else:
                break

    def quit(self) -> None:
        self.__is_running = False
        super(Memory_Thread, self).quit()
