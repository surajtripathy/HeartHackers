# HeartHackers
This project was submitted at the CEWIT Hackathon 2023 by team HeartHackers.

### Motivation
Accessing affordable healthcare in several countries can be a significant challenge, as obtaining an ECG scan can often take a considerable amount of time. Additionally, waiting for a doctor to review the results can further prolong the process. To address this issue, we propose a cost-effective alternative that utilizes readily available hardware such as an Arduino and an ECG sensor. We leverage a pre-trained model at a specific sampling rate to generate inferences and visualizations, which we store in a database. The user can then receive their inferences via email. 


### File description
The project is based on a Arduino hooked up with an ECG sensor which pushes readings to a serial port COM5 at a particular baud rate(9600)

The main flask based application on receiving a request from the user with username and corresponding email id starts reading the serial port and after a particular sampling time generates inferences and visualizations and sends them via mail and stores it in MongoDB for future reference.

- main_app.py - Flask based webapp to take user and mail to initiate ecg sensor and send inferences and visualizations via email and store it in MongoDB 
- utils.py - Functions for IO, sampling, QoS
