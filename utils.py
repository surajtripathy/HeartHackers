from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileType, FileName, Disposition, ContentId
from pymongo import MongoClient
from PIL import Image
import io
import urllib 
import serial
from biosppy import storage
import matplotlib.pyplot as plt
import numpy as np
import base64

SENDGRID_API_KEY = ""
DB_STRING = ""
TIME = 3600

def quality_indicator(arr):
    sample_rate = 100
    time_window = 10
    count = 0
    window_size = (sample_rate*time_window)
    times = len(arr) // (window_size)
    for i in range(1,times+1):
        data_arr = arr[(i-1)*(window_size):i*(window_size)]
        avg_val = np.average(data_arr)
        std_dev = np.std(data_arr)
        inside_sum = 0
        for j in range(len(data_arr)):
            inside_sum = inside_sum + ((data_arr[j] - avg_val)/std_dev)**4

        if inside_sum/(window_size) > 3:
            count+=1
    return (count*100)/times

def send_email(user, to_email):
    message = Mail(
        from_email='suraj.tripathy@stonybrook.edu',
        to_emails=to_email,
        subject=f"{user}'s detailed heart rate report",
        html_content = '''
            <p> Below is attached a report of your detailed ECG readings taken on Arduino sensor by HeartHackers 
            and the entire project can be accessed by a webapp. Thank you.
            <img src="cid:sendgrid-logo" alt="SendGrid logo">
        '''
    )
    filename = f"img_data\\{user}.png"
    with open(filename, 'rb') as f:
        data = f.read()
    message.attachment = Attachment(
        disposition='inline',
        file_name=filename,
        file_type='image/png',
        file_content=base64.b64encode(data).decode(),
        content_id='sendgrid-logo',
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e.message)

def save_image_to_db(user, filename):
    client = MongoClient(DB_STRING)
    db = client.image_data
    images = db.images
    im = Image.open(filename)
    image_bytes = io.BytesIO()
    im.save(image_bytes, format='PNG')
    image = {
        'data': image_bytes.getvalue(),
        'user': user
    }
    image_id = images.insert_one(image).inserted_id

def record_data(user, email_id):
    filename = f"data\\{user}.txt"
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM6'
    ser.open()
    file = open(filename, "w")
    for _ in range(TIME):
        file.write(ser.readline().decode('ascii').strip() + '\n')
    ser.close()
    file.close()

    signal, mdata = storage.load_txt(filename)
    qos = quality_indicator(signal)
    time_data = np.arange(signal.size)
    plt.plot(time_data, signal)
    plt.xlabel("time in seconds")
    plt.ylabel("ECG in milli Volts")
    plt.title(f"Quality of reading - {qos}\%")
    plt.savefig(f'img_data\{user}.png')
    save_image_to_db(user, filename=f"img_data\{user}.png")
    send_email(user, to_email=email_id)



    
