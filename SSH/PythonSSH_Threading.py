import paramiko
import time
import datetime
import re
import threading

def ssh_conn(ip):
    # Change exception message
    try:
        # Set time value to use
        date_time = datetime.datetime.now().strftime("%Y-%m-%d")
        date_time_s = datetime.datetime.now().strftime("%I:%M:%S %p")

        # Use paramiko ssh client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username='admin', password='password', look_for_keys=False, timeout=None)

        # Invoke the shell for interactive terminal
        connection = ssh.invoke_shell()
        connection.send("\n")
        connection.send("terminal length 0\n")

        # hold the script 1 second before it execute another script
        time.sleep(1)
        connection.send("\n")
        connection.send("show ip eigrp neighbor\n")
        time.sleep(3)

        # Receive buffer output
        file_output = connection.recv(9999).decode(encoding='utf-8')

        hostname = (re.search('(.+)#', file_output)).group().strip('#')

        # Write output to a file
        outFile = open(hostname + "-" + str(date_time) + ".txt", "w")
        outFile.writelines(file_output[678:-19])
        outFile.close()

        # Closing the connection
        ssh.close()

        # Print information if the task is done
        if re.search('% Invalid input detected', file_output):
            print("* There was at least one IOS syntax error on device %s" % hostname)
        else:
            print("{} is done, it was started at {}" .format(hostname, date_time_s))




    except paramiko.AuthenticationException:
        print("User or password incorrect, Please try again!!!")

def SSH_Thread():
    thread_instance = []
    list_ip = ["172.16.0.21", "172.16.0.22"]
    for ip in list_ip:
        trd = threading.Thread(target=ssh_conn, args=(ip.strip("\n"),))
        trd.start()
        thread_instance.append(trd)

    for trd in thread_instance:
        trd.join()


if __name__ == '__main__':
    SSH_Thread()
