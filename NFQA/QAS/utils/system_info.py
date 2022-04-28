import platform as pf
import psutil
from datetime import datetime
import time


def get_system_info():
    sys_info = {}

    system_info = pf.uname()

    boot_time = psutil.boot_time()

    boot_time = datetime.fromtimestamp(boot_time)
    now_time = datetime.fromtimestamp(time.time())
    run_time = now_time - boot_time

    now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
    boot_time = boot_time.strftime("%Y-%m-%d %H:%M:%S")

    sys_info["system"] = system_info.system
    sys_info["node"] = system_info.node
    sys_info["release"] = system_info.release
    sys_info["version"] = system_info.version
    sys_info["machine"] = system_info.machine
    sys_info["processor"] = system_info.processor
    sys_info["run_time"] = run_time
    sys_info["now_time"] = now_time
    sys_info["boot_time"] = boot_time

    return sys_info
