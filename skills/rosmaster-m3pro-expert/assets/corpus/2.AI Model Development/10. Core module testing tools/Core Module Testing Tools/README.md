# Core Module Testing Tools

## 1. Course Content

multi_brains provides a minimal test program for testing the core modules of the large language model functionality, used to quickly pinpoint the source of problems in abnormal situations.

## 2. Starting the Dify Service

## 3. Entering the Test Tool Path

```bash
cd ~/M3Pro_ws/src/multi_brains/test
ls
```

The test tools are as follows:

## 4. Testing Local Speech Synthesis Functionality

Test the local speech synthesis function for Chinese and English in sequence.

```bash
python3 test_PiperTTS.py
```

After running, the synthesized speech results for Chinese and English will be played in sequence.

## 5. Testing Local Speech Recognition Functionality

After running, the preset Chinese and English audio files will be tested in sequence.

```bash
python3 test_SenseVoiceSmall.py
```

After running, the speech recognition results for the test audio will be printed.

## 6. Testing if the robot can access Dify normally

When the program shows that the model service is unavailable, you can test if the robot's vehicle system can access Dify due to a network address error.

```bash
python3 test_dify_connection.py
```

If the robot displays the following information normally, it proves that the robot is connected to Dify correctly. Otherwise, Dify may not be started or the Dify program may have crashed and needs to be restarted.

## 7. Online Voice Services for Domestic Users

### 7.1 BaiLian Speech Recognition

If there is an error in online speech recognition, you can test the BaiLian speech recognition service separately.

```bash
python3 test_TongyiASR.py
```

After running, it will perform speech recognition testing on the preset test audio.

### 7.2 BaiLian Speech Synthesis

If there is an error in online speech recognition, you can test the BaiLian speech recognition service separately.

```bash
python3 test_TongyiTTS.py
```

After running, it will first perform speech synthesis on the default text, and then play the corresponding audio.

### 7.3 BaiLian Speech Synthesis

If there is an error in online speech recognition, you can test the BaiLian speech recognition service separately.

```bash
python3 test_baiduTTS.py
```

After running, it will first perform speech synthesis on the default text, and then play the corresponding audio.

## 8. Online Voice Services for International Users

### 8.1 iFlytek Speech Recognition Service

If online speech recognition encounters errors, you can test the Tongyi speech recognition service separately.

```bash
python3 test_TongyiASR.py
```

After running, it will perform speech recognition testing on the preset test audio.

### 8.2 iFlytek Speech Synthesis Service

If online speech synthesis encounters errors, you can test the Tongyi speech synthesis service separately.

```bash
python3 test_TongyiTTS.py
```

After running, it will first perform speech synthesis on the default text, and then play the corresponding audio.
