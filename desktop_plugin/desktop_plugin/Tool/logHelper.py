import logging  # 引入logging模块
import os
import time

from desktop_plugin.Tool.PathHelper import PathHelper


class logHelper:
    __fh:logging.FileHandler = None

    @staticmethod
    def getLogger() -> logging.Logger:
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)  # Log等级总开关
        if not logHelper.__fh:
            # 第二步，创建一个handler，用于写入日志文件
            rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
            log_path = PathHelper.getCurrentPath()
            log_path = log_path + '/Logs/'
            if not os.path.exists(PathHelper.getCurrentPath() + "/Logs/"):
                os.mkdir(PathHelper.getCurrentPath() + "/Logs/")
            log_name = log_path + rq + '.log'
            logfile = log_name
            fh = logging.FileHandler(logfile, mode='w')
            fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
            logHelper.__fh = fh
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        logHelper.__fh.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        logger.addHandler(logHelper.__fh)
        return logger
