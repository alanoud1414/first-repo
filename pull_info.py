'''
##########################################################################################
- This script will logging ssh to multiple same devices, run commands in each to pull info,
  and store the result in separate file / print it in CMD.
- Using the netmiko library.
The steps:
   1- Full the ip.txt file with list of Switches IP's.
   2- Full the ip.txt file with list of Switches IP's.
   3- writing your Username and Password.
   4- Choose the way of output result.
   5- Support different type of devices, just change the device 
      type depending on the devices you are working on.

- Functions:

    ConnectHandler() -- To connect to the device based on device type.
    AuthenticationException() -- Handling the Authentication error.
    getpass() -- Get user password.
    datetime() -- Print the current time.
    strftime() -- To specify the format of the time.
    List_Of_Content() -- Extract all files content and save it inside empty list.
    dirname() -- Returns the directory component of a pathname.
    abspath() -- Return an absolute path.
##########################################################################################'''
__author__ = "Alanoud Alfawzan"
__author_email__ = "alanoud.alfawzan@kaust.edu.sa"
 
from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException
import getpass
import datetime
import os 




#-------------------------------------------------------------#
User_name=input('User: \n')
Password= getpass.getpass('Password: \n')
now = datetime.datetime.now()
final_time=now.strftime('%H:%M:%S on %A, %B the %dth, %Y')



#-------------------------------------------------------------#
#Extract all files content and save it inside empty list   
def List_Of_Content(file):
    list_of_content=[]
    read_file=file.readlines()
    for line in read_file:
        first_line=line.strip()
        list_of_content.append(first_line)
    return list_of_content

  
#-------------------------------------------------------------#
#IP file
File_name_ip= open (os.path.dirname(os.path.abspath(__file__))+'\\'+'ip.txt','r')
IP_list=List_Of_Content(File_name_ip)
#Command file
File_name=open (os.path.dirname(os.path.abspath(__file__))+'\\'+'command.txt','r')
Command_list=List_Of_Content(File_name)
out_put=int(input('Please Choose (1) to Show The Output on CMD or Choose (2) to Create New File:\n'))
#-------------------------------------------------------------#




# Start excuting, and connecting to the switches
for IP in IP_list:
    print('Now Will Gother Information From IP :'+IP)
    print(final_time)#print the current time 
    Device={'host':IP,'username':User_name,'password':Password,'device_type':'cisco_ios'}#take info pass it to ConnectHandler 
    
    try:#To check the Authentication is correct

        connect=ConnectHandler(**Device)
    except AuthenticationException:
        print("Authentication Failed, Verify Your Credentials On: "+IP)
        print('1- Wrong Username.')
        print('2- Wrong Password.')
        exit()

    # to save the output in .txt file / to show the result in CMD
    if out_put == 1:
        print('Now Will Gather Information From IP :'+IP)
        for command in Command_list:
            output=connect.send_command(command)
            print(output)
    elif out_put == 2:
        print('Now Will Gather Information From IP :'+IP)
        for command in Command_list:
            with open (os.path.dirname(os.path.abspath(__file__))+r'\\'+'Output.txt','a') as new_file:
                new_file.write('\n')
                new_file.write(IP+'#'+command+'\n')
                new_file.write(connect.send_command(command))
                new_file.write('\n')
    else:
        print('sorry you enter wrong value'.title())
        print('Run the programm again'.title())
        exit()


print('*'*50)
print('All Done...\nHope It Was Good ^_^')
print('*'*50)









