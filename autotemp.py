import wmi,time
import os
import queue
from pyrw import rwe

rew = rwe.ReadWriteEverything()
def maxspeed():
    rew.callRWECommand('''>WEC 0xBD 0x4E
    Write EC Byte 0xBD = 0x4E
    >RwExit''')

def autospeed():
    rew.callRWECommand('''>WEC 0xBD 0x52
    Write EC Byte 0xBD = 0x52
    >RwExit''')

w = wmi.WMI(namespace="root\OpenHardwareMonitor")

taskkillcmd = 'taskkill /F /IM OpenHardwareMonitor.exe'
os.system(taskkillcmd)
OHMstartcmd = 'START OpenHardwareMonitor.exe'
os.system(OHMstartcmd)
time.sleep(3)

checkinterval = 1  # every seconds
averagecount = 60  # count average for x count
crittemp = 75
lowtemp = 67
state = 'auto'
autospeed()

cpu1average= []
cpu2average= []
cpu3average= []
cpu4average= []
gpuaverage= []

def checkTemp():
    global state
    while True:
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType==u'Temperature':
                if sensor.name == 'CPU Core #1':
                    cpu1temp = sensor.Value
                if sensor.name == 'CPU Core #2':
                    cpu2temp = sensor.Value
                if sensor.name == 'CPU Core #3':
                    cpu3temp = sensor.Value
                if sensor.name == 'CPU Core #4':
                    cpu4temp = sensor.Value
                if sensor.name == 'GPU Core':
                    gputemp = sensor.Value

        time.sleep(checkinterval)
        cpu1average.append(cpu1temp)
        cpu2average.append(cpu2temp)
        cpu3average.append(cpu3temp)
        cpu4average.append(cpu4temp)
        gpuaverage.append(gputemp)
        if len(cpu1average) < averagecount and len(cpu1average) > 0:
            pass
        else:
            cpu1average.pop(0)
            cpu2average.pop(0)
            cpu3average.pop(0)
            cpu4average.pop(0)
            gpuaverage.pop(0)
        print(cpu1average)
        print(cpu2average)
        print(cpu3average)
        print(cpu4average)
        print(gpuaverage)
        print()
        cpu1avg = sum(cpu1average)/len(cpu1average)
        cpu2avg = sum(cpu2average)/len(cpu2average)
        cpu3avg = sum(cpu3average)/len(cpu3average)
        cpu4avg = sum(cpu4average)/len(cpu4average)
        gpuavg = sum(gpuaverage)/len(gpuaverage)
        print('CPU Core #1: ' + ' Temp: ' + str(cpu1temp) + ' average temp in '+ str(checkinterval*averagecount) +' seconds: ' + str(cpu1avg))
        print('CPU Core #2: ' + ' Temp: ' + str(cpu2temp) +  ' average temp in '+ str(checkinterval*averagecount) +' seconds: ' + str(cpu2avg))
        print('CPU Core #3: ' + ' Temp: ' + str(cpu3temp) +  ' average temp in '+ str(checkinterval*averagecount) +' seconds: ' + str(cpu3avg))
        print('CPU Core #4: ' + ' Temp: ' + str(cpu4temp) + ' average temp in '+ str(checkinterval*averagecount) +' seconds: ' + str(cpu4avg))
        print('GPU Core:    '+' Temp: ' +str(gputemp)+ ' average temp in '+ str(checkinterval*averagecount) +' seconds: ' + str(gpuavg))
        print()
        # print('CPU Core #1: ' + 'Temp: ' + str(cpu1temp) + ' Load: ' + str(cpu1load))
        # print('CPU Core #2: ' + 'Temp: ' + str(cpu2temp) + ' Load: ' + str(cpu2load))
        # print('CPU Core #3: ' + 'Temp: ' + str(cpu3temp) + ' Load: ' + str(cpu3load))
        # print('CPU Core #4: ' + 'Temp: ' + str(cpu4temp) + ' Load: ' + str(cpu4load))
        # print('GPU: '+'Temp: ' +str(gputemp)+' Load: '+ str(gpuload))
        # print('Used RAM ' +str(usedRAM))

        if cpu1avg > crittemp or cpu2avg > crittemp or cpu3avg > crittemp or cpu4avg > crittemp or gpuavg > crittemp:
            print('Average temp is over ' + str(crittemp))
            if state != 'max':
                maxspeed()
                state = 'max'
                print('Turning ON the fans!')
            else:
                print('Fans are already ON!')
        elif cpu1avg < lowtemp and cpu2avg < lowtemp and cpu3avg < lowtemp and cpu4avg < lowtemp and gpuavg < lowtemp:
            print('Average temp is below ' + str(lowtemp))
            if state != 'auto':
                autospeed()
                state = 'auto'
                print('Turning OFF the fans!')
            else:
                print('Fans are already OFF!')

checkTemp()