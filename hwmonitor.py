#import libraries (psutil for monitoring PC and pyserial for sending data throught serial interface
import psutil
import serial

#pySerial settings
ser = serial.Serial("COM4", 9600, timeout = 1)                                           #make instance of Serial

#system info that doesnt need to be refreshed
coreCount = psutil.cpu_count(logical = False)                   #get number of PHYSICAL cores
cores = "(" + str(coreCount) + "C)"                             #make it as a string with () and "C"
totalMem = int(round(psutil.virtual_memory().total / 1073741824.0))    #get total memory size, which is divided by 1073741824 (GIGI constant, actual binary size) and rounded up (so it wont work properly with systems that have less than 1GB RAM)
if totalMem < 10:
    totalMemStr = " (" + str(totalMem) + "GB)"                   #if RAM is less that 10GB, put artificial character (space) before actual text (keeps arduino code simpler)
else:
    totalMemStr = "(" + str(totalMem) + "GB)"                    #if RAM is more or equal than 10GB, write it without space (i defined 5 characters per information (if not stated else) INCLUDING parenthesis "()")

while(1):                                                       #infinite loop, we dont want to stop this program.. and dont worry, it will not consume lot of resources, read next line to understand why
    cpu = psutil.cpu_percent(interval=1.2)                      #get usage of CPU in percentage with interval of 1.2s (that actually slow our entire code to be executed once in 1.2s so thats why ^ works). 1.2s is set due to Arduinos serial buffer being pretty slow and it takes a lot of time to read from it.. also it takes time to redraw the OLED and NOTHING below 1.2s will properly work (at least on Arduino UNO)
    mem = psutil.virtual_memory().percent                       #get usage of RAM in percentage
    sdd = 100-psutil.disk_usage("C:").percent                   #get used space of C: disk (in my case SSD); since we get USED space, we need to substract it from 100(%) and we got FREE space
    hdd = 100-psutil.disk_usage("D:").percent                   #   XXX    the same here, i have 2 drives (SSD and HDD)
                                                                #we need to parse floats (decimal numbers from psutil) to strings
    if cpu < 10:
        cpuStr = "  " + str(cpu)                                #if CPU usage is under 10%, put 2 artificial characters (spaces) before the value.. as i mentioned, i set every information to be 5 characters including parenthesis and/or decimal places, so we need to fill resot of the space with spaces (also, its prettier)
    elif cpu < 100:
        cpuStr = " " + str(cpu)                                 #here the same, but only 1 space. because 98.5 have only 4 characters.. 
    else:
        cpuStr = str(cpu)                                       #100.0 is 5 characters so there is no need to put spaces in before..

    if mem < 10:
        memStr = "  " + str(mem)                                #the same as in CPU
    elif mem < 100:
        memStr = " " + str(mem)
    else:
        memStr = str(mem)

    if hdd < 10:                                                #   XXX
        hddStr = "  " + str(hdd)                                #   XXX
    elif hdd < 100:                                             #   XXX
        hddStr = " " + str(hdd)                                 #   XXX
    else:                                                       #   XXX
        hddStr = str(hdd)                                       #   XXX

    if sdd < 10:
        sddStr = "  " + str(sdd)
    elif sdd < 100:
        sddStr = " " + str(sdd)
    else:
        sddStr = str(sdd)
    
    serialDataStr = cpuStr + memStr + sddStr + hddStr + cores + totalMemStr        #now we concenate all strings together by using "+" operand. By this, well got one long string of data
    serialDataBytes = serialDataStr.encode("UTF-8")             #since we want to send string as series of BYTES, we wncode it to UTF-8 standart. This will put "b" before string, indicating that values are 1B each 

    print(serialDataBytes)                                      #here we print our serial string, used for debugging, can be commented out
    ser.write(serialDataBytes)                                  #send our long encoded string throught serial interface

ser.close()                                                     #this will never execute, because while loop will go forever. But i like to leave it here to prevent some bugs and bad stuff that could happen, also for you, if you want to include some way of getting out of the COM port
