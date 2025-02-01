###pip install psutil wmi

import psutil
import wmi

def get_process_paths(pids):
    process_paths = {}
    c = wmi.WMI()
    for pid in pids:
        try:
            process = psutil.Process(int(pid))
            # الحصول على مسار الملف الرئيسي للعملية
            exe_path = process.exe()
            process_paths[pid] = exe_path
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            process_paths[pid] = "Process not found or access denied"
    return process_paths

def read_pids_from_file(filename):
    with open(filename, 'r') as f:
        pids = [line.strip() for line in f.readlines()]
    return pids

def write_process_paths_to_file(process_paths, filename):
    with open(filename, 'w') as f:
        for pid, path in process_paths.items():
            f.write(f"PID: {pid} - Path: {path}\n")

def main():
    pids_filename = 'pids.txt'
    output_filename = 'pidsPaths.txt'
    pids = read_pids_from_file(pids_filename)
    process_paths = get_process_paths(pids)
    write_process_paths_to_file(process_paths, output_filename)

if __name__ == '__main__':
    main()