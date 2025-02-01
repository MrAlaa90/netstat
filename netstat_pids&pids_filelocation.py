import subprocess
import re
import psutil
import wmi

def execute_netstat():
    # تنفيذ الأمر netstat -ano
    command = "netstat -ano"
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    return output

def parse_netstat_output(output):
    # تحليل النتائج
    lines = output.split('\n')
    # تخطي السطور الأولى (العناوين)
    lines = lines[4:]
    pids = []
    for line in lines:
        line = line.strip()
        if line:
            columns = line.split()
            if len(columns) > 1:
                pid = columns[-1]  # استخراج الـ PID من العمود الأخير
                pids.append(pid)
    return pids

def write_pids_to_file(pids, filename):
    # كتابة الـ PIDs إلى ملف
    with open(filename, 'w') as f:
        for pid in pids:
            f.write(pid + '\n')
            
###########################################

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
    output = execute_netstat()
    pids = parse_netstat_output(output)
    write_pids_to_file(pids, 'pids.txt')
    pids_filename = 'pids.txt'
    output_filename = 'pidsPaths.txt'
    pids = read_pids_from_file(pids_filename)
    process_paths = get_process_paths(pids)
    write_process_paths_to_file(process_paths, output_filename)

if __name__ == '__main__':
    main()