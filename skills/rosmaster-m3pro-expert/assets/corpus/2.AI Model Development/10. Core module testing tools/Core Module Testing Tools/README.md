# Core Module Testing Tools

## 1. Course Content

`multi_brains` provides minimal test programs for testing the core modules of the large language model function. These tools help quickly locate the source of abnormal behavior.

## 2. Start the Dify Service

Start Dify before testing modules that need to access the Dify service.

## 3. Enter the Test Tool Path

```bash
cd ~/M3Pro_ws/src/multi_brains/test
ls
```

The test tools are listed in this directory.

## 4. Test Local Speech Synthesis

Run the following command to test local speech synthesis for Chinese and English:

```bash
python3 test_PiperTTS.py
```

After it runs, the synthesized Chinese and English speech results are played in sequence.

## 5. Test Local Speech Recognition

Run the following command to test the preset Chinese and English audio files:

```bash
python3 test_SenseVoiceSmall.py
```

After it runs, the speech recognition results for the test audio are printed.

## 6. Test Whether the Robot Can Access Dify

If the program reports that the model service is unavailable, use this test to check whether the robot system can access Dify. A network address error may prevent access.

```bash
python3 test_dify_connection.py
```

If the robot displays normal connection information, it is connected to Dify correctly. Otherwise, Dify may not be started, or the Dify program may have crashed and needs to be restarted.

## 7. Online Voice Services for Domestic Users

### 7.1 Bailian Speech Recognition

If online speech recognition reports an error, test the Bailian speech recognition service separately.

```bash
python3 test_TongyiASR.py
```

After it runs, the preset test audio is used for speech recognition testing.

### 7.2 Bailian Speech Synthesis

If online speech synthesis reports an error, test the Bailian speech synthesis service separately.

```bash
python3 test_TongyiTTS.py
```

After it runs, the default text is synthesized first, then the corresponding audio is played.

### 7.3 Baidu Speech Synthesis

If the Baidu online speech synthesis service reports an error, test it separately.

```bash
python3 test_baiduTTS.py
```

After it runs, the default text is synthesized first, then the corresponding audio is played.

## 8. Online Voice Services for International Users

### 8.1 iFlytek Speech Recognition

If online speech recognition reports an error, test the iFlytek speech recognition service separately.

```bash
python3 test_xunfeiASR.py
```

After it runs, the preset test audio is used for speech recognition testing.

### 8.2 iFlytek Speech Synthesis

If online speech synthesis reports an error, test the iFlytek speech synthesis service separately.

```bash
python3 test_xunfeiTTS.py
```

After it runs, the default text is synthesized first, then the corresponding audio is played.
