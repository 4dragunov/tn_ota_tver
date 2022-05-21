#its a new version

from machine import ADC, Pin
import time, utime
import machine
import dht
import urequests
import network

import ujson
import app.secrets as secrets


file = open('config.json')
config_datas = ujson.load(file)
url = secrets.URL
uId1 = config_datas['sensor1']['id']
uId2 = config_datas['sensor2']['id']
uId3 = config_datas['sensor3']['id']
uId4 = config_datas['sensor4']['id']
uId5 = config_datas['sensor5']['id']
uId6 = config_datas['sensor6']['id']
print(uId1)



adc1 = ADC(Pin(36))
adc1.atten(ADC.ATTN_11DB)
imp1 = Pin(19, Pin.OUT)
imp1.off()
rev1 = Pin(13, Pin.OUT) 
rev1.off()

adc2 = ADC(Pin(39))
adc2.atten(ADC.ATTN_11DB)
imp2 = Pin(18, Pin.OUT)
imp2.off()
rev2 = Pin(9, Pin.OUT)
rev2.off()

adc3 = ADC(Pin(34))
adc3.atten(ADC.ATTN_11DB)
imp3 = Pin(5, Pin.OUT)
imp3.off()
rev3 = Pin(10, Pin.OUT)
rev3.off()

adc4 = ADC(Pin(35))
adc4.atten(ADC.ATTN_11DB)
imp4 = Pin(17, Pin.OUT)
imp4.off()
rev4 = Pin(15, Pin.OUT)
rev4.off()

adc5 = ADC(Pin(32))
adc5.atten(ADC.ATTN_11DB)
imp5 = Pin(16, Pin.OUT)
imp5.off()
rev5 = Pin(2, Pin.OUT)
rev5.off()

adc6 = ADC(Pin(33))
adc6.atten(ADC.ATTN_11DB)
imp6 = Pin(4, Pin.OUT)
imp6.off()
rev6 = Pin(0, Pin.OUT)
rev6.off()

def average(data_list):
    try:
        for i in range(len(data_list) - 1):
            for j in range(len(data_list) - i - 1):
                if data_list[j] > data_list[j + 1]:
                    data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]

        result = []
        med = len(data_list) // 2
        zero_delta = abs(data_list[med] - data_list[med + 1])
        for i in range(med, len(data_list) - 1):
            if data_list[i + 1] - data_list[i] <= zero_delta:
                result.append(data_list[i])

        for i in range(1, med):
            if data_list[i] - data_list[i - 1] <= zero_delta:
                result.append(data_list[i])
        if sum(result) != 0:
            avg_result = sum(result) / len(result)
        else:
            avg_result = 0
        print('average result is ', avg_result)
        return avg_result
    except:
        return data_list[0]


def sendData(data, sensor_uId):
    response_data = urequests.post(url, json={"value": data, "sensor": sensor_uId})
    print(response_data.status_code)
    if response_data.status_code != 201:
        print(response_data.status_code)
        machine.reset()


def measure(adc, imp, rev):
    dataList = []

    imp.on()
    time.sleep(0.1)
    for _ in range(50):
        dataList.append(adc.read_u16())
        time.sleep(0.1)

    val = average(dataList)
    imp.off()
    time.sleep(0.5)
    reverse(rev)
    print('measure result is ', val)
    return round(val, 0)


def reverse(rev):
    rev.on()
    time.sleep(0.2)
    rev.off()
    time.sleep(0.5)


def connect():
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config_datas['wifi']['ssid'], config_datas['wifi']['password'])
    while not sta_if.isconnected():
        pass
    print('OK - network config:', sta_if.ifconfig())


def temp():
    try:
        sensor = dht.DHT22(Pin(14))
        sensor.measure() 
        
        #sensor.humidity()
        return sensor.temperature()
    except:
        return -100


def main():
    import gc
    print('main start')
    print('main while True')
    while True:
        try:
            print('main for i in range 100')
            for i in range(1000):
                #print('main measure ', i)
                time.sleep(1)
                data1 = measure(adc1, imp1, rev1)
                print(data1)
                sendData(data1, 'l1')
                time.sleep(1)
                data2 = measure(adc2, imp2, rev2)
                sendData(data2, 'l2')
                time.sleep(1)
                data3 = measure(adc3, imp3, rev3)
                sendData(data3, 'l3')
                time.sleep(1)
                data4 = measure(adc4, imp4, rev4)
                sendData(data4, 'l4')
                time.sleep(1)
                data5 = measure(adc5, imp5, rev5)
                sendData(data5, 'l5')
                time.sleep(1)
                data6 = measure(adc6, imp6, rev6)
                sendData(data6, 'l6')
                time.sleep(1)
                
                t = temp()
                sendData(t, 't1')
                
                
                #print('main measure OK', i)
                #print('main send data ', i, data)
                
                #sendData(data1, uId1)
                print('data1 send complete ', i, data1)
                
                
                print('data2 send complete ', i, data2)
                time.sleep(4)
                gc.collect()
            machine.reset()

        except:
            print('main error')
            time.sleep(1)
            machine.reset()


main()


