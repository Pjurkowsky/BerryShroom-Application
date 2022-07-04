import serial, time
from GSM7BIT import gsm_decode

ser = serial.Serial(

    port='/dev/ttyUSB0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=2,
)


def cmd_send(x):
    ser.write(x + '\r')
    out = ''
    time.sleep(3)
    while ser.inWaiting() > 0:
        out += ser.read(1)
    return out


response = cmd_send('AT+CUSD=1,"AA180C3702",15')
coded_message_start = response.find('"', 30) + 1
coded_message_end = response.find('"', coded_message_start)
coded_message = response[coded_message_start:coded_message_end]
message = gsm_decode(coded_message)

print(message)
