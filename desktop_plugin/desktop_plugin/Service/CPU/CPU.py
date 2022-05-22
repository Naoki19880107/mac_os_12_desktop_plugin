import os
import subprocess

from desktop_plugin.Tool.PathHelper import PathHelper


class CPU:
    @staticmethod
    def getCPUName() -> str:
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command, shell=True).strip().decode('utf-8').split('CPU')[0]

    @staticmethod
    def getcpuidle() ->float:
        command = "top -l 1 | head -n 10 | grep CPU"
        result = subprocess.check_output(command, shell=True).strip().decode('utf-8').split('sys,')[1].replace('% idle','')
        result = result.replace("\t",'').replace("\n",'')
        return 100 - float(result)

    @staticmethod
    def getcputemp() -> str:
        command = PathHelper.getCurrentPath()+"/osx-cpu-temp -c"
        return subprocess.check_output(command,shell=True).strip().decode('utf-8')

