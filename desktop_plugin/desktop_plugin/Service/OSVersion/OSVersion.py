import subprocess


class OSVersion:
    @staticmethod
    def getVersion() -> str:
        p = subprocess.Popen("sw_vers", stdout=subprocess.PIPE)
        result = str(p.communicate()[0], encoding='utf-8').split('ProductVersion:')[1].split('BuildVersion:')[0]
        result = result.replace("\t",'').replace("\n",'')
        return result

    @staticmethod
    def getVersionName(version:str) -> str:
        version_name_dict = {
                         '12':'macOS Monterey',
                         '11':'macOS Big Sur',
                         '10.15':'macOS Catalina',
                         }
        if version[0:2] in version_name_dict.keys():
            return version_name_dict[version[0:2]]
        elif version[0:5] in version_name_dict.keys():
            return version_name_dict[version[0:5]]
        else:
            return ''
