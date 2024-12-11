


# Created by Karthik P S (for Nymble)
# Contact: Karthikreddyr02@gmail.com

import serial
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 2400
TIMEOUT = 5
DATA_TO_SEND = """Finance Minister Arun Jaitley Tuesday hit out at former RBI governor Raghuram Rajan for predicting that the next banking crisis would be triggered by MSME lending, saying postmortem is easier than taking action when it was required. Rajan, who had as the chief economist at IMF warned of impending financial crisis of 2008, in a note to a parliamentary committee warned against ambitious credit targets and loan waivers, saying that they could be the sources of next banking crisis. Government should focus on sources of the next crisis, not just the last one. In particular, government should refrain from setting ambitious credit targets or waiving loans. Credit targets are sometimes achieved by abandoning appropriate due diligence, creating the environment for future NPAs," Rajan said in the note." Both MUDRA loans as well as the Kisan Credit Card, while popular, have to be examined more closely for potential credit risk. Rajan, who was RBI governor for three years till September 2016, is currently."""

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

def send_data():
    chara = ""
    sent_bytes = 0
    print("Sending data to MCU...")
    for count, char in enumerate(DATA_TO_SEND):
        ser.write(char.encode('utf-8'))
        sent_bytes += 1
        chara += char
        if count == len(DATA_TO_SEND) - 1:
            time.sleep(1)
        if ser.in_waiting > 0:
            try:
                speed_data = ser.readline().decode('utf-8', errors='ignore').strip()
                if speed_data:
                    print(speed_data)
            except UnicodeDecodeError:
                print("Error decoding MCU response")
    print("All data sent. Ready to receive data from MCU...\n")
    return sent_bytes

def receive_data():
    received_data = b""
    total_received_bytes = 0
    start_receive_time = time.time()
    last_activity_time = time.time()
    last_report_time = time.time()
    TIMEOUT_THRESHOLD = 3.0
    no_data = True
    print("Waiting for responses from MCU...")
    while True:
        if ser.in_waiting > 0:
            received_char = ser.read(1)
            if received_char:
                received_data += received_char
                no_data = False
                total_received_bytes += 1
                last_activity_time = time.time()
        if time.time() - last_activity_time > TIMEOUT_THRESHOLD and no_data == False:
            break
        
        if time.time() - last_report_time >= 1:
            elapsed_time = time.time() - start_receive_time
            if elapsed_time > 0:
                speed_bps = (total_received_bytes * 8) / elapsed_time
                print(f"SpeedRx: {speed_bps:.2f} bps")
            total_received_bytes = 0
            start_receive_time = time.time()
            last_report_time = time.time()

    try:
        decoded_data = received_data.decode('utf-8', errors='ignore')
        print(decoded_data)
    except Exception as e:
        print(f"Error decoding received data: {e}")

if __name__ == "__main__":

    send_data()
    receive_data()
    ser.close()
