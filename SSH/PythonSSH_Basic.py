import paramiko
import time
import datetime
import re


def ssh_conn(ip):
    # Change exception message
    try:
        # Set time value to use
        date_time = datetime.datetime.now().strftime("%Y-%m-%d")

        # Use paramiko ssh client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username='admin', password='password', look_for_keys=False, timeout=None)

        # Invoke the shell for interactive terminal
        connection = ssh.invoke_shell()
        connection.send("terminal length 0\n")

        # hold the script 1 second before it execute another script
        time.sleep(1)
        connection.send("\n")
        connection.send("show ip ospf\n")
        time.sleep(3)

        # Receive buffer output
        file_output = connection.recv(9999).decode(encoding='utf-8')

        hostname = (re.search('(.+)#', file_output)).group().strip('#')

        """
        if re.search('% Invalid command', file_output):
            print("* There was at least one IOS syntax error on device %s" % hostname)
        else:
            print("\nDONE for device %s" % hostname)
        """

        # Print the output interactively to the CLI
        print(file_output)

        # Write output to a file
        outFile = open(hostname + "-" + str(date_time) + ".txt", "w")
        outFile.writelines(file_output[678:-19])
        outFile.close()

        # Closing the connection
        ssh.close()

        # Print information if the task is done
        print("%s is done" % hostname)


    except paramiko.AuthenticationException:
        print("User or password incorrect, Please try again!!!")

if __name__ == '__main__':
    ssh_conn("10.23.0.5")