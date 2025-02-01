import subprocess
import re

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

def main():
    output = execute_netstat()
    pids = parse_netstat_output(output)
    write_pids_to_file(pids, 'pids.txt')

if __name__ == '__main__':
    main()
    
    ###python netstat_pids.py