# **Core Module Testing Tools**

#### **[Core Module Testing](#page-0-0) Tools**

- <span id="page-0-0"></span>[1. Course](#page-0-1) Content
- [2. Starting](#page-0-2) the Dify Service
- [3. Entering](#page-0-3) the Test Tool Path
- 4. Testing Local Speech Synthesis [Functionality](#page-0-4)
- 5. Testing Local Speech Recognition [Functionality](#page-1-0)
- [6. Testing](#page-1-1) if the robot can access Dify normally
- 7. Online Voice Services for [Domestic Users](#page-1-2)
  - 7.1 BaiLian Speech [Recognition](#page-1-3)
  - 7.2 BaiLian Speech [Synthesis](#page-2-0)
  - 7.3 BaiLian Speech [Synthesis](#page-2-1)
- <span id="page-0-1"></span>8. Online Voice Services for [International](#page-2-2) Users
  - 8.1 [iFlytek Speech](#page-2-3) Recognition Service
  - 8.2 [iFlytek Speech](#page-3-0) Synthesis Service

### **1. Course Content**

<span id="page-0-2"></span>multi\_brains provides a minimal test program for testing the core modules of the large language model functionality, used to quickly pinpoint the source of problems in abnormal situations.

# **2. Starting the Dify Service**

# **3. Entering the Test Tool Path**

```
cd ~/M3Pro_ws/src/multi_brains/test
ls
```

<span id="page-0-3"></span>The test tools are as follows:

### **4. Testing Local Speech Synthesis Functionality**

<span id="page-0-4"></span>Test the local speech synthesis function for Chinese and English in sequence.

```
python3 test_PiperTTS.py
```

After running, the synthesized speech results for Chinese and English will be played in sequence.

## **5. Testing Local Speech Recognition Functionality**

<span id="page-1-0"></span>After running, the preset Chinese and English audio files will be tested in sequence.

```
python3 test_SenseVoiceSmall.py
```

After running, the speech recognition results for the test audio will be printed.

# **6. Testing if the robot can access Dify normally**

<span id="page-1-1"></span>When the program shows that the model service is unavailable, you can test if the robot's vehicle system can access Dify due to a network address error.

```
python3 test_dify_connection.py
```

If the robot displays the following information normally, it proves that the robot is connected to Dify correctly. Otherwise, Dify may not be started or the Dify program may have crashed and needs to be restarted.

# **7. Online Voice Services for Domestic Users**

#### **7.1 BaiLian Speech Recognition**

<span id="page-1-3"></span><span id="page-1-2"></span>If there is an error in online speech recognition, you can test the BaiLian speech recognition service separately.

```
python3 test_TongyiASR.py
```

After running, it will perform speech recognition testing on the preset test audio.

#### **7.2 BaiLian Speech Synthesis**

<span id="page-2-0"></span>If there is an error in online speech recognition, you can test the BaiLian speech recognition service separately.

```
python3 test_TongyiTTS.py
```

After running, it will first perform speech synthesis on the default text, and then play the corresponding audio.

#### **7.3 BaiLian Speech Synthesis**

<span id="page-2-1"></span>If there is an error in online speech recognition, you can test the BaiLian speech recognition service separately.

```
python3 test_baiduTTS.py
```

After running, it will first perform speech synthesis on the default text, and then play the corresponding audio.

# **8. Online Voice Services for International Users**

#### **8.1 iFlytek Speech Recognition Service**

<span id="page-2-3"></span><span id="page-2-2"></span>If online speech recognition encounters errors, you can test the Tongyi speech recognition service separately.

```
python3 test_TongyiASR.py
```

After running, it will perform speech recognition testing on the preset test audio.

#### **8.2 iFlytek Speech Synthesis Service**

<span id="page-3-0"></span>If online speech synthesis encounters errors, you can test the Tongyi speech synthesis service separately.

```
python3 test_TongyiTTS.py
```

After running, it will first perform speech synthesis on the default text, and then play the corresponding audio.