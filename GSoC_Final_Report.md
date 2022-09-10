# GSoC Final Report

![Untitled](/GSoC_Final_Report/images/Untitled.png)

# Anomaly detection and recovery with a Deep-learning-based approach

### (Project associated with GNSS-SDR)

### Contributor: Seonwoo Kim / Mentor: Luis Esteve Elfau

## Introduction:

GNSS systems and software are directly exposed to various threats. Especially in this project, I focused on detecting spoofing attacks using Deep-learning based approach. Since the GNSS-SDR receiver records various property logs in terms of the received signal, we can get more information over the naive PVT data. Based on the instruction from my mentor, I went through related materials and now working on the TEXBAT dataset. The dataset was designed for the general use of developing methods of detecting or mitigating spoofing attacks. According to the knowledge I got from the related papers, I focused on two signal processing blocks(tracking, and observables). And I found out that the C/N0 value constantly shows an outstanding deviation when spoofing happens. I implement more research on this variable and tried a naive Autoencoder model(with LSTM) on this data. Additionally, I tried a statistical method using the Bollinger band to detect the attack moment.

## Objectives:

Develop a spoofing-detection model which can be applied to GNSS-SDR

## Key Skills:

GNSS, Network-Spoofing, Pandas, Numpy, Geojson, Keras, Tensorflow, C++, Python

## Deliveries(link):

- Extract from the bin file : [https://drive.google.com/drive/folders/13-jZOEQsWxXss04g2HMTHZNyb0Px-pMa?usp=sharing](https://drive.google.com/drive/folders/13-jZOEQsWxXss04g2HMTHZNyb0Px-pMa?usp=sharing)
- Graphs of extracted observables : [https://drive.google.com/drive/folders/1Q5OBJr1BatXJFdhs3lIylh445pgUkmyo?usp=sharing](https://drive.google.com/drive/folders/1Q5OBJr1BatXJFdhs3lIylh445pgUkmyo?usp=sharing)
- Github repository for the code : https://github.com/seki5405/gnss_spoof_detector.git

## TImeline:

![Untitled](/GSoC_Final_Report/images/Untitled%201.png)

---

## Description of Work:

### Dataset Analysis

The TEXBAT dataset was presented in 2012 for simulating GNSS receiver under spoofing attack. There are six high-fidelity digital recordings of live static and dynamic GPS L1 C/A spoofing tests conducted by the Radionavigation Laboratory of the University of Texas at Austin. Each scenario is revealing obvious anomalies that future GPS receivers could be designed to detect.

The dataset is composed of 8 different scenarios. 

![Scenario description (ds1 to ds6)](/GSoC_Final_Report/images/Untitled%202.png)

Scenario description (ds1 to ds6)

Additional 2 data based on different scenarios were also released after 4 years.

- The 7th scenario is based on the cleanStati.bin dataset. It’s power-matched time push scenario much like ds3.bin but more subtle because it employs carrier phase alignment between the spoofing and authentic signals.
- The 8th scenario is identical to the ds7.bin scenario but it also includes unpredictable low-rate security code. This is called Zero-delay security code estimation and replay attack.

I explored the dataset and extract observations as below;

- Extracted observables & PVT([LINK](https://drive.google.com/drive/folders/1sEhqObv1yJpL33siQ6Hi36jN-0CZydet))
    
    Each signal processing block has different variables and it’s possible to extract the variables by setting ‘dump’ option in `conf` file. I extracted variables from Acquisition, Tracking, Observable, PVT modules. After that I implemented EDA to find useful variables. For the analysis, I put the spoofing data’s plot with clean data’s plot to compare them visually.
    
    [파일 목록 캡쳐 화면!!!]
    
- Graph from the extracted observables ([LINK](https://drive.google.com/drive/folders/1Q5OBJr1BatXJFdhs3lIylh445pgUkmyo))
    
    From EDA, I found some notable observables; C/N0, Doppler Shift, Pseudorange, Prompt_i, Prompt_q.
    
    - cn0_db_hz : C/N0 estimation, in dB-Hz.
        
        ![Untitled](/GSoC_Final_Report/images/Untitled%203.png)
        
        C/N0 is the one of the most frequently used variables to find anomaly in GNSS. So I investigated from the beginning. As I expected, C/N0 showed notable difference between spoofed and clean data. In normal status, C/N0 tends to be stable while it fluctuates unexpectedly in case of spoofing attack.
        
    - carrier_doppler_hz : Doppler shift, in Hz.
        
        ![Case 1 : Slight fluctuation during linear decrease/increase](/GSoC_Final_Report/images/Untitled%204.png)
        
        Case 1 : Slight fluctuation during linear decrease/increase
        
        ![Case 2 : Abrupt extreme jump/drop](/GSoC_Final_Report/images/Untitled%205.png)
        
        Case 2 : Abrupt extreme jump/drop
        
        Carrier_doppler_hz(Doppler Shift) is the value which typically shows gradual increase/decrease in stationary status since the only satellite move makes gradual change. It also cannot show abrupt jump or drop in case of movement. However, I observed abrupt jump/drop from the spoofed signal(case 2). Also slight fluctuation was also observed from the stationary status.
        
    - Pseudorange : Difference between the time of reception and the time of transmissinon.
        
        ![Untitled](/GSoC_Final_Report/images/Untitled%206.png)
        
        Since the Pseudorange is calculated as Doppler Shift multiplied by the negative of carrier wavelength, it’s supposed to be static. However, the abrupt jump/drop was observed in spoofed scenarios.
        

### Code

Code developed during the summer is separated from gnss-sdr repository. The repository is composed of three things(folders): 

- ipynb files: Includes all analyzed and approaches ([LINK](https://github.com/seki5405/gnss_spoof_detector.git))
- monitoring-client: Modified based on the existing monitoring-client
    - Changed processing variables(2→6)
        
        ![Untitled](/GSoC_Final_Report/images/Untitled%207.png)
        
    - Implement additional socket communication to detector module
        
        ![Untitled](/GSoC_Final_Report/images/Untitled%208.png)
        
    - Data extraction&transmission from the monitoring-client to python file
        - Save data for each channel to `line` and combine it to `log`
            
            ![Untitled](/GSoC_Final_Report/images/Untitled%209.png)
            
        - Transmit `log` to detector(collector) module
            
            ![Untitled](/GSoC_Final_Report/images/Untitled%2010.png)
            
- spoof_detector
    - `[collector.py](http://collector.py)` : Save the streamed data for the future utilization
        
        ![Untitled](/GSoC_Final_Report/images/Untitled%2011.png)
        
        ![Untitled](/GSoC_Final_Report/images/Untitled%2012.png)
        
    - Autoencoder(`train.ipynb`)
        
        ![Untitled](/GSoC_Final_Report/images/Untitled%2013.png)
        
    - `detector.py` : Load the trained model and determine the occurance of spoofing
        
        ![Untitled](/GSoC_Final_Report/images/Untitled%2014.png)
        
        ![Untitled](/GSoC_Final_Report/images/Untitled%2015.png)
        

### Variables

I chose 4 variables from tracking module based on the observation I found during EDA. The variables show visible difference in their pattern and the amplitude.

- prompt_i : Value of the Prompt correlator in the In-phase component.
- prompt_q : Value of the Prompt correlator in the Quadrature component.
- cn0_db_hz : C/N0 estimation, in dB-Hz.
- carrier_doppler_hz : Doppler shift, in Hz.

### Autoencoder

Initially developed LSTM based autoencoder based on the thought that the streamed consecutive data will be well processed with RNN type models. But changed to use Linear autoencoder at last because LSTM based model requires a lot of calculation which is not proper to process streamed data. Also, the Linear model also worked well on detecting spoofing attacks.

![Linear Autoencoder model structure](/GSoC_Final_Report/images/Untitled%2016.png)

Linear Autoencoder model structure

Before feeding the data, I preprocessed data by normalizing and getting `diff()`(Getting offset from the previous timestep).

![Normalization using StandardScaler()](/GSoC_Final_Report/images/Untitled%2017.png)

Normalization using StandardScaler()

And here’re the preprocessed data with comparison with CleanStatic data.

![Prompt_i](/GSoC_Final_Report/images/Untitled%2018.png)

Prompt_i

![Prompt_q](/GSoC_Final_Report/images/Untitled%2019.png)

Prompt_q

![cn0_db_hz](/GSoC_Final_Report/images/Untitled%2020.png)

cn0_db_hz

![carrier_doppler_hz](/GSoC_Final_Report/images/Untitled%2021.png)

carrier_doppler_hz

As we can see, there’s a starting of attack at around 1200th timestep. And we can observe some weird patterns.

I trained the autoencoder model with `cleanStatic` scenario which is normal. The autoencoder model is trained to generate the output of which label is its input. So the model is trained to generate the input for the normal data, which shows higher Mean Squared Error for the abnormal(Spoofed) data.

![Mean Squared Error equation](/GSoC_Final_Report/images/Untitled%2022.png)

Mean Squared Error equation

Typically, the model shows more than 50 of MSE(Mean Squared Error) for the Spoofed timestep.

![MSE graph for cleanStatic dataset, from this, I set the threshold to 50.](/GSoC_Final_Report/images/Untitled%2023.png)

MSE graph for cleanStatic dataset, from this, I set the threshold to 50.

![MSE graph of 8 channels from the 3rd scenario. The model triggers alerts if the error goes over 50.](/GSoC_Final_Report/images/Untitled%2024.png)

MSE graph of 8 channels from the 3rd scenario. The model triggers alerts if the error goes over 50.

### Communication between monitoring client - detector

Since the model was developed with Python, I implemented socket communication between the monitoring-client and the detector. On top of the original visualization of monitoring-client, I added construction of log data which consists of data from 8 channels which is implemented in `gnss_synchro_udp_source.cc`. Plus, `main.cc` connects to `detector.py` (`collector.py`) after setting up the socket configuration. And repeatedly transmit the log.

### Detector

The detector is designed to work in real time. It receives streamed data from the monitoring-client and parse it into different channel data. The parsed data is preprocessed and fed to the pre-trained model. Based on the gap between the prediction and the input, it can get MSE(Mean Squared Error) for each channel. If the MSE value goes over the designated threshold(50 in the experiment), it will trigger alarm message.

![Triggered alert messages (detector.py)](/GSoC_Final_Report/images/Untitled%2025.png)

Triggered alert messages (detector.py)

### Subsidiary: Bollingerband

While considering the streamed data processing, came up with an idea of using statistical method called Bollingerband. It consists of Moving average line and it’s upper band and lower band which maintain equal offset from the moving average line.  It doesn’t require any training of Deep Neural network.

Used `cn0_db_hz` to check its performance, and it worked well but parameter optimization seems to be necessary.

![Spoofed signal](/GSoC_Final_Report/images/Untitled%2026.png)

Spoofed signal

![Normal signal](/GSoC_Final_Report/images/Untitled%2027.png)

Normal signal

## How to run the code:

- Installation(monitoring-client)
    - You may need to rebuild the monitoring-client.
    - The basic instructions are same with the origin. [Here](https://gnss-sdr.org/docs/tutorials/monitoring-software-receiver-internal-status/)’s the link of the tutorial.
    - Copy `gnss_synchro_udp.source.cc` and `main.cc` from our repository.
        
        (It contains socket communication and log processing)
        
- Execution order
    - The monitoring-client is supposed to connect with `detector.py`.
    - So it’s mandatory to run `detector.py` first and monitoring-client after that.
    - Lastly, if you run `gnss-sdr`, it will start streaming.
    
    ```jsx
    # needs to run the commands in the working directory
    > python3 detector.py
    > ./monitoring-client 1234
    > gnss-sdr --config_file=./sample.conf
    ```
    

## Results:

- Measurement method
    
    To evaluate the model’s performance, I feed the spoofed signal data by running gnss-sdr with monitor on. While running gnss-sdr, detector receives the data and split the data based on channels. The splitted data goes through the autoencoder model, and the model triggers an alert if the error between the output and input is over 50 (This was the threshold I set based on the experiemental result). I calculate the accuracy of channels by channel by checking if the alert is triggered.
    
- Measurement result
    
    
    | Scenario | #1 | #2 | #3 | #4 | #7 | #8 |
    | --- | --- | --- | --- | --- | --- | --- |
    | Alert Triggered | 7/8 | 8/8 | 6/8 | 5/8 | 0/8 | 8/8 |
    | Accuracy(%) | 87.5 | 100 | 75 | 62.5 | 0 | 100 |
    
     Considering that the triggered alert in any channel notify users to check if there is an spoofing attack, the model works in all scenarios except the 7th scenario.
    
    The scenario tries to match the power-level with the clean input which may work on C/N0. From that, I figure out that C/N0 is the key factor to detect spoofing attack.
    

### Conclusion:

The autoencoder model looked reliable to detect spoofing attack. It doesn’t detect clearly for the seventh scenario but worked well with other scenarios. It means that the model generally works well to raise an alert for spoofing attack. However, due to the processing speed of `detector.py`, it doesn’t work robustly in real time. It seems that multi-threading or extra sampling might help solving this.  

- Future Work:
    - Prove the concept in the real world environment : It may require additional setup to spoofing signal leakage while receiving the real-time signal.
    - Using more variables : The monitor module can process only limited amount of variables. Because of that, I couldn’t help excluding some variables I chose during EDA. If adding more variables by editing the `monitoring_client`, it may enhance the model’s performance.
    - Multiprocessing : The `detector` prototype is working with a single thread and there seems to some amount of delay in visualizing. Multiprocessing with separated visual expression may helps.

### Bibliography:

1. T. E. Humphreys et al., “The Texas Spoofing Test Battery: Toward a Standard for Evaluating GPS Signal Authentication Techniques,” 2012.
2. T. Humphreys et al., “TEXBAT DATA SETS 7 AND 8.”, utexas.
3. A. Lemmenes, et al., “Detailed Analysis of the TEXBAT Datasets Using a High Fidelity Software GPS Receiver,” *Proceedings of the 29th International Technical Meeting of The Satellite Division of the Institute of Navigation (ION GNSS+ 2016)*, Nov. 2016.
4. Harshad Sathaye, “Anti-Spoofing Techniques for GNSS Receivers”, 2021, https://harshadsathaye.com/gsoc21/#ftnt2
5. A. Ranganathan et al., “SPREE: a spoofing resistant GPS receiver”, Mobicom 16, Oct. 2016.
6.  S. Semanjski et al., “Use of Supervised Machine Learning for GNSS Signal Spoofing Detection with Validation on Real-World Meaconing and Spoofing Data—Part I,” *Sensors*, vol. 20, no. 4, p. 1171, Feb. 2020.
7.  S. Semanjski et al., “Use of Supervised Machine Learning for GNSS Signal Spoofing Detection with Validation on Real-World Meaconing and Spoofing Data—Part II,” *Sensors*, vol. 20, no. 7, p. 1806, Mar. 2020.
8. A. Shafique et al., “Detecting Signal Spoofing Attack in UAVs Using Machine Learning Models,” *IEEE Access*, vol. 9, pp. 93803–93815, 2021.
9. Z. Chen, C. K. Yeo, B. S. Lee and C. T. Lau, "Autoencoder-based network anomaly detection," *2018 Wireless Telecommunications Symposium (WTS)*, 2018, pp. 1-5.
