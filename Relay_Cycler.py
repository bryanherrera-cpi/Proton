import serial
import time

usb_port_name = "/dev/cu.usbserial-FT4XY8H4"
target_count = 5

serialPort = serial.Serial(
    port=usb_port_name, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)

cycle_count = 0
successfull_cycle_count = 0
response_delay = 0.5

def readSerial(port):
    message = ""
    byte = ""
    results = {
        "closed": "",
        "open": ""
    }
    count = 0
    while True:
        byte = str(port.read(), 'UTF-8')
        if byte == "\n":
            isContactStatus = "contactor 0:" in message
            if isContactStatus:
                if count == 0:
                    results["closed"] = [message.split('(')[1].split(')')[0].split(',')[0].replace(" ", ''), message.split('(')[1].split(')')[0].split(',')[1].replace(" ", '')]
                else:
                    results["open"] = [message.split('(')[1].split(')')[0].split(',')[0].replace(" ", ''), message.split('(')[1].split(')')[0].split(',')[1].replace(" ", '')]
                count += 1
            if count == 2:
                break
            message = ""
        message += byte
    return results

def validateCycle(data):
    closed = False
    opened = False
    if data["closed"][0] == "Closed" and data["closed"][1] == "Closed":
        closed = True
    if data["open"][0] == "Open" and data["open"][1] == "Open":
        opened = True
    return closed and opened

while cycle_count < target_count:
    print("Closing Relays...\n")
    serialPort.write(b'rc 0\r')

    time.sleep(response_delay)

    serialPort.write(b'r\r')

    time.sleep(response_delay)

    print("Opening Relays...\n")
    serialPort.write(b'ro\r')

    time.sleep(response_delay)
    
    serialPort.write(b'r\r')

    time.sleep(response_delay)

    #Read Serial Monitor Resonse
    response = readSerial(serialPort)

    time.sleep(response_delay)

    #Validate Open/Close Response
    cycleComplete = validateCycle(response)

    if cycleComplete:
        successfull_cycle_count += 1
    cycle_count += 1
    

    print(f"Cycles Compleded: {successfull_cycle_count}/{cycle_count}\n")

    time.sleep(1)

print("Target count reached. Stopping test.")