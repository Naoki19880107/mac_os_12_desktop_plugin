import Foundation
from CoreServices import LaunchServices
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QWidget, QAction, QMenu, QApplication


from desktop_plugin.Service.Memory.Memory import Memory
from desktop_plugin.Tool.ImagePlus import ImagePlus
from desktop_plugin.Tool.PathHelper import PathHelper
from desktop_plugin.UI.password_enter.password_enter_dialog_controller import password_enter_dialog_controller


class Tray(QSystemTrayIcon):
    def __init__(self, parent: QWidget = None):
        super(QSystemTrayIcon, self).__init__(parent)
        icon = QIcon(
            ImagePlus.PixmapToRound(QPixmap(PathHelper.getCurrentPath() + "/Resource/MacMemoryToolIcon.png"), 160))
        self.setIcon(icon)
        self.__create_menu()
        self.__launch_service_Shared_File_List_Handle(False)

    def __create_menu(self):
        aAction = QAction('开机自启', self)
        aAction.setCheckable(True)
        aAction.triggered.connect(self.__action)
        a_Clear_Memory = QAction('整理内存', self)
        a_Clear_Memory.triggered.connect(self.__clear_memory)
        aQuit = QAction('退出', self)
        aQuit.triggered.connect(self.__quit)
        menu = QMenu(None)
        menu.addAction(aAction)
        menu.addAction(a_Clear_Memory)
        menu.addAction(aQuit)
        self.setContextMenu(menu)

    def __action(self):
        if self.contextMenu().actions()[0].isChecked():
            loginItems: LaunchServices.LSSharedFileListRef = LaunchServices.LSSharedFileListCreate(None,
                                                                                                   LaunchServices.kLSSharedFileListSessionLoginItems,
                                                                                                   None)
            if len(PathHelper.getCurrentPath().split('.app')) > 1:
                url: LaunchServices.CFURLRef = Foundation.NSURL.alloc().initFileURLWithPath_(PathHelper.getCurrentPath().split('.app')[0] + '.app')
            else:
                url:LaunchServices.CFURLRef = Foundation.NSURL.alloc().initFileURLWithPath_(PathHelper.getCurrentPath())
            LaunchServices.LSSharedFileListInsertItemURL(loginItems, LaunchServices.kLSSharedFileListItemLast, None,
                                                         None, url, None, None)
        else:
            self.__launch_service_Shared_File_List_Handle(True)

    def __launch_service_Shared_File_List_Handle(self,is_del:bool):
        loginItems: LaunchServices.LSSharedFileListRef = LaunchServices.LSSharedFileListCreate(None,
                                                                                               LaunchServices.kLSSharedFileListSessionLoginItems,
                                                                                               None)
        loginItemsArrayRef: Foundation.CFArrayRef = LaunchServices.LSSharedFileListCopySnapshot(loginItems, None)
        items, _ = loginItemsArrayRef
        for item in items:
            itemRef: LaunchServices.LSSharedFileListItemRef = item
            if 'desktop_plugin' in str(LaunchServices.LSSharedFileListItemResolve(itemRef, 0, None, None)[1]):
                if is_del:
                    LaunchServices.LSSharedFileListItemRemove(loginItems, itemRef)
                else:
                    self.contextMenu().actions()[0].setChecked(True)
                break

    def __quit(self):
        QApplication.instance().quit()

    def __clear_memory(self):
        self.__password_enter_dialog_controller = password_enter_dialog_controller()
        self.__password_enter_dialog_controller.setModal(True)
        self.__password_enter_dialog_controller.exec_()
        if self.__password_enter_dialog_controller.password:
            ret:bool = Memory.clear_memory(self.__password_enter_dialog_controller.password)
            if not ret:
                QtWidgets.QMessageBox.critical(None, '错误','\n\n密码错误！\n\n')
                self.__clear_memory()
