#-------------------------------------------------------------#
#This script will logging ssh to multiple same devices, run commands in each to pull info,
#and store the result in separate file.
#Using the netmiko library for CLI interfacing.
#The steps:
#   1- Logging ssh (username - password).
#   2- Take the files name: 
#        - file contain the list of IP's.
#        - file contain the list fo commmand.
#   3- Run the command once for each ip.
#   4- Store the output in file.
#   5- Error Handling.
#   6- Support different type of devices, just change the device type depending on the devices
#      you are working on.
#-------------------------------------------------------------#



__author__ = "Alanoud Alfawzan"
__author_email__ = "alanoud.alfawzan@kaust.edu.sa"
 
#List of modules 
from netmiko import ConnectHandler
#To connect to the device based on device type.
from netmiko.ssh_exception import AuthenticationException
#Handling the Authentication error
import getpass
#Get user password
import datetime
#Print the current time
import os 
#Return the current working directory


#-------------------------------------------------------------#
User_name=input('User: \n')
Password= getpass.getpass('Password: \n')
now = datetime.datetime.now()
final_time=now.strftime('%H:%M:%S on %A, %B the %dth, %Y')


#-------------------------------------------------------------#
#To check the extention of the files, must end with .txt
def test_file_extension(file_name):
    extension=file_name[len(file_name)-4: len(file_name)]
    while extension !='.txt':
        print('!!! WRONG !!! \n Please your file name must end with .txt extension')
        file_name=input(' Enter your file name again: \n')
        extension=file_name[len(file_name)-4: len(file_name)]
    return file_name


#-------------------------------------------------------------#
#Open files, Readlines, Store values as list, Return the list
def Is_It_Existed(user_file):
    try:
        #Open the file based on you working directory
        open_files=open(os.path.dirname(os.path.abspath(__file__))+r'\\'+user_file ,'r')   
    except FileNotFoundError:
        print('Sorry The File Not Found')
        exit()
    return open_files
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
File_name_ip=input('Enter your IP file name with .txt extenstion:\n').strip()#Take the file name from user
Check_Extension_ip=test_file_extension(File_name_ip)#Check file location 
File_Existedip=Is_It_Existed(Check_Extension_ip)#Check file extention
IP_list=List_Of_Content(File_Existedip)#Return the file content in list

#Command file
File_name=input('Enter your command file name with .txt extenstion:\n').strip()
Check_Extension=test_file_extension(File_name)
File_Excited=Is_It_Existed(Check_Extension)
Command_list=List_Of_Content(File_Excited)
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
    for command in Command_list:
        #output=connect.send_command(command)
        #print(output)
        with open (os.path.dirname(os.path.abspath(__file__))+r'\\'+'Output.txt','a') as new_file:
            new_file.write('\n')
            new_file.write(IP+'#'+command+'\n')
            new_file.write(connect.send_command(command))
            new_file.write('\n')


print('*'*50)
print('All Done...\nHope It Was Good ^_^')
print('*'*50)









