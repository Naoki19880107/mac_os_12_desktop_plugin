import json
import subprocess

from desktop_plugin.Tool.PathHelper import PathHelper


class Memory:
    @staticmethod
    def get_physical_memory() -> tuple[int, str]:
        command = "system_profiler SPHardwareDataType -json"
        result = json.loads(subprocess.check_output(command, shell=True).strip().decode('utf-8'))
        memory_list = str(result['SPHardwareDataType'][0]['physical_memory']).split(" ")
        return int(memory_list[0]), memory_list[1]

    @staticmethod
    def get_unused_memory() -> tuple[int, str]:
        command = "top -l 1 | head -n 10 | grep PhysMem"
        result = subprocess.check_output(command, shell=True).strip().decode('utf-8').split(',')[1].replace(' unused.','')
        result = result.replace("\t", '').replace("\n", '')
        unit = result[-1]
        unused_Memory = int(result.replace(unit, ''))
        if unit == 'M':
            unused_Memory = int(unused_Memory / 1000)
            unit = 'G'
        return unused_Memory,unit

    @staticmethod
    def clear_memory(password:str) -> bool:
        command = PathHelper.getCurrentPath()+"/purge"
        ret = subprocess.run('echo %s|sudo -S %s' % (password, command),shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if ret.returncode == 0:
            return True
        else:
            return False


