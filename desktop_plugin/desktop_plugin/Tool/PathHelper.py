import os
import sys
from pathlib import Path


class PathHelper:
    @staticmethod
    def getCurrentPath() -> str:
        if getattr(sys, 'frozen', False):
            absPath = os.path.dirname(os.path.abspath(sys.executable))
        else:
            absPath = os.getcwd()
        return absPath
