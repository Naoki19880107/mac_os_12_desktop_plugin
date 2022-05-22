import os

from PyQt5.QtWidgets import QApplication

from desktop_plugin.UI.desktop_plugin.desktop_plugin_controller import desktop_plugin_controller_controller
from desktop_plugin.UI.desktop_round_plugin.desktop_round_plugin_controller import \
    desktop_round_plugin_controller_controller


def init():
    try:
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)
        desktop_plugin_controller_Controller = desktop_round_plugin_controller_controller()
        desktop_plugin_controller_Controller.show()
        app.exec_()
    except Exception:
        init()


def print_file_name(path_str: str):
    for sub_path_str in os.listdir(path_str):
        if os.path.isdir(path_str + "/" + sub_path_str):
            print_file_name(path_str + "/" + sub_path_str)
        else:
            if not ("__pycache__" in path_str) and (sub_path_str != ".DS_Store"):
                if ".py" in sub_path_str:
                    print_str = ("'" + path_str + "/" + sub_path_str + "',")
                    # print_str = "'" + sub_path_str.replace(".py", "") + "',"
                    print(print_str)


if __name__ == "__main__":
    init()
    # print_file_name(os.getcwd())
