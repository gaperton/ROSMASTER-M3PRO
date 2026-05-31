# `multi_brains` Framework Source Code Analysis

## 1. Course Content

- This section analyzes the core functions of the `multi_brains` package architecture.
- In later lessons, each newly introduced action function is explained separately.

> [!TIP]
> This is a code-analysis lesson for users who want a deeper understanding of how the functions work. If you only want to experience the functions, you can skip this section.

## 2. Source Code Package Structure

### 2.1 Package File Structure

```text
|-- config
|   |-- map_mapping.yaml
|   |-- multi_brains_setting.yaml
|   `-- README.MD
|-- language
|   |-- en.yaml
|   `-- zh.yaml
|-- launch
|   `-- llm_agent_control.launch.py
|-- multi_brains
|   |-- action_service.py
|   |-- asr_detect.py
|   |-- __init__.py
|   |-- model_service.py
|   `-- utils
|-- package.xml
|-- resource
|   `-- multi_brains
|-- setup.cfg
|-- setup.py
|-- system_vioce
|   |-- en
|   |-- notify.mp3
|   |-- test_en.wav
|   |-- test_zh.wav
|   `-- zh
`-- test
    |-- test_copyright.py
    |-- test_dify_connection.py
    |-- test_flake8.py
    |-- test_pep257.py
    |-- test_PiperTTS.py
    |-- test_SenseVoiceSmall.py
    |-- test_TongyiASR.py
    |-- test_TongyiTTS.py
    |-- test_xunfeiASR.py
    `-- test_xunfeiTTS.py
```

`config`

Stores configuration file templates.

`multi_brains`

Main source-code folder.

`asr_detect.py`

Speech recognition program file.

`model_service.py`

Model service program file. It calls model interfaces and implements the model inference architecture.

`action_service.py`

Action service program file. It receives action lists requested by the model service and controls robot movement.

`launch`

Stores ROS 2 node launch files.

`language`

Stores language-specific log text.

`system_vioce`

Stores system audio files. The directory name is kept as it appears in the package.

## 3. Speech Recognition Function

Source code path:

```text
~/M3Pro_ws/src/multi_brains/multi_brains/asr_detect.py
```

### 3.1 Dynamic Recording with Voice Activity Detection

The speech recognition module uses voice activity detection (VAD) to record only valid speech:

1. Continuously reads audio frames and performs voice activity detection.
2. If speech is detected, adds the audio frames to the buffer.
3. If continuous silence exceeds the threshold, 90 frames or about 1.5 seconds, ends the recording.
4. After recording ends, removes the trailing silent portion and saves the valid speech as a WAV file.
5. If no valid speech is detected, no file is saved.

```python
def listen_for_speech(self):
        ''' Dynamic recording with VAD'''
        self.record_flag = True
        PRE_SPEECH_FRAMES = 5 #150ms voice start compensation
        PRINT_EVERY_N_FRAMES = 5
        recording_active = False
        silence_counter = 0
        print_counter = 0
        audio_buffer = []
        pre_speech_buffer = deque(maxlen=PRE_SPEECH_FRAMES)
        stream = self.pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.frame_bytes,
        )
        self.play_audio(self.notify_audio)
        try:
            while not self.stop_event.is_set():
                frame = stream.read(self.frame_bytes, exception_on_overflow=False)
                is_speech = self.vad.is_speech(frame, self.sample_rate)
                print_counter += 1
                if print_counter >= PRINT_EVERY_N_FRAMES:
                    print("1-1-1" if is_speech else "-----")
                    print_counter = 0
                if not recording_active:
                    # ---- IDLE ----
                    pre_speech_buffer.append(frame)
                    if is_speech:
                        # RECORDING
                        recording_active = True
                        audio_buffer.extend(pre_speech_buffer)
                        pre_speech_buffer.clear()
                        audio_buffer.append(frame)
                        silence_counter = 0
                else:
                    # ---- RECORDING ----
                    audio_buffer.append(frame)
                    if is_speech:
                        silence_counter = max(0, silence_counter - 1)
                    else:
                        silence_counter += 1
                        if silence_counter >= self.MAX_SILENCE_FRAMES:
                            break
        finally:
            stream.stop_stream()
            stream.close()
            self.record_flag = False
        if recording_active and audio_buffer:
            with wave.open(self.user_speech_dir, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(self.pyaudio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b"".join(audio_buffer))
            return True
        return False
```

### 3.2 ASR Speech Recognition

The `recognize` method of the speech engine performs speech recognition. The speech engine is provided by instantiated objects of `Tongyi_ASR`, `SenseVoiceSmall_ASR`, and `XUNFEI_ASR`.

```python
def kws_handler(self) -> None:
        ''' Wake-up handling function'''
        if self.stop_event.is_set():
            self.logger.info("Wake-up processing thread interrupted; no user speech will be handled.")
            return
        if self.listen_for_speech():
            asr_result = self.asr_engine.recognize(self.user_speech_dir) # Perform ASR conversion
            if not asr_result[0]:
                self.logger.error(
                    Fore.RED
                    + f"Speech recognition failed because the audio segment is empty or the speech model is unavailable. ASR_OUT: {asr_result[1]}"
                    + Fore.RESET
                )
            else:
                if len(asr_result[1]) > self.asr_threashold:
                    self.logger.info(Fore.GREEN + "ASR Result: " + asr_result[1] + Fore.RESET)
                    self.asr_result_queue.put([asr_result[1], 'text_request', False]) # Put the ASR result into the queue
                else:
                    self.logger.info(
                        Fore.YELLOW
                        + "The voice recognition result is too short. The wake-up may have been accidental: "
                        + asr_result[1]
                        + Fore.RESET
                    )
```

## 4. Model Service Function

Source code path:

```text
~/M3Pro_ws/src/multi_brains/multi_brains/model_service.py
```

Core function behavior:

- Checks the `llm_handler_queue` queue in a separate thread for model requests.
- When an element is pushed into the queue, calls the Dify access interface `chat` function with different parameters based on the request type.
- After receiving the AI agent response from Dify, parses the response for speech playback and sends the action list to the action service for execution.

```python
def handle_llm_thread(self) -> None:
        '''Handle model request'''
        while True:
            if not self.llm_handler_queue.empty(): # The queue is not empty; process model requests.
                if not self.text_chat_mode and self.asr_detect.record_flag:
                    continue
                request_query = self.llm_handler_queue.get()
                if self.debug_mode:
                    self.get_logger().info(f"Processing LLM request: {request_query}")
                if request_query[1] == 'text_request':
                    '''text request'''
                    result = self.dify_llmclient.chat(request_query[0], robot_feedback=request_query[2])
                elif request_query[1] == 'image_request':
                    '''vision + text request'''
                    result = self.dify_llmclient.chat(
                        request_query[0],
                        image_path=self.image_cache_path,
                        robot_feedback=request_query[2],
                    )
                if result[0]:
                    if not self.text_chat_mode and self.asr_detect.record_flag:
                        continue
                    split_result = self.extract_actions(result[1])
                    if split_result is None:
                        continue
                    action_list, llm_response, decision_plan = self.extract_actions(result[1])
                    if decision_plan is not None:
                        self.get_logger().info(
                            Fore.YELLOW
                            + self.syslog.get_text("system_log_3", decision_plan=decision_plan)
                            + Fore.RESET
                        )
                    self.get_logger().info(
                        Fore.YELLOW + f'"action": {action_list}, "response": {llm_response}' + Fore.RESET
                    )
                    if not self.text_chat_mode: # Voice reply
                        if self.tts_engine.synthesize(llm_response, self.tts_out_path):
                            self.play_audio(self.tts_out_path)
                        else:
                            self.get_logger().error(
                                Fore.RED + "Speech synthesis failed. Check whether the TTS model is available." + Fore.RESET
                            )
                    else: # Text reply
                        if decision_plan is not None:
                            self.text_pub.publish(
                                String(data=self.syslog.get_text("system_log_3", decision_plan=decision_plan))
                            )
                        self.text_pub.publish(String(data=f'"action": {action_list}, "response": {llm_response}'))
                    if action_list != []:
                        self.send_action_service(action_list, llm_response)
                else:
                    self.get_logger().error(
                        Fore.RED
                        + f"The model request failed. Check whether Dify or the AI model is running normally. Error Log: {result[1]}"
                        + Fore.RESET
                    )
            else:
                time.sleep(1.0) # Sleep for 1 second when there are no requests.
```

## 5. Action Service Function

The action service contains the implementation of the basic action functions the robot can perform. It receives action-list requests and executes the corresponding actions. It also supports interruption and resumed operation after the robot is awakened again.

The core callback function is `execute_callback`.

It accepts a string representing the action list.

```python
def execute_callback(self, goal_handle):
        """action execution callback function"""
        actions = goal_handle.request.actions
        feedback_result = None
        if self.debug_mode:
            self.get_logger().info(self.actionlog.get_text("debug_log_1", actions=actions))
        self.action_runing = True
        for action in actions:
            if self.interrupt_event.is_set():
                break
            match = re.match(r"(\w+)\((.*)\)", action)
            action_name, args_str = match.groups()
            args = [arg.strip() for arg in args_str.split(",")] if args_str else []
            if not hasattr(self, action_name):
                self.get_logger().error(Fore.RED + f"action_service: {action} is invalid action, skip execution" + Fore.RESET)
            else:
                method = getattr(self, action_name)
                feedback_result = method(*args)
        if not self.interrupt_event.is_set(): # Provide feedback to the Dify agent on action execution results.
            msg = LlmRequest()
            if feedback_result == False:
                # Action failed
                msg.llm_request = self.actionlog.get_text("action_feedback_2", action_name=actions)
                msg.robot_feedback = True
                self.llm_request_pub.publish(msg)
            elif feedback_result == True:
                # Action executed successfully
                msg.llm_request = self.actionlog.get_text("action_feedback_1", action_name=actions)
                msg.robot_feedback = True
                self.llm_request_pub.publish(msg)
            elif feedback_result == None:
                # No operation, no feedback
                if self.debug_mode:
                    self.get_logger().info(self.actionlog.get_text("system_log_1"))
            if self.debug_mode:
                self.get_logger().info(msg.llm_request)
        if self.debug_mode:
            self.get_logger().info(self.actionlog.get_text("system_log_2"))
        self.action_runing = False
        self.interrupt_event.clear()
        goal_handle.succeed()
        result = Rot.Result()
        result.success = True
        return result
```

## 6. Interruption Function

The robot supports interruption at any stage. Interruptions are divided into recording-stage interruptions, dialogue-stage interruptions, and action-stage interruptions. The following sections explain how interruption works in each stage.

### 6.1 Recording-Stage Interruption

If you make a mistake while recording, or if you are not satisfied with the recorded content, you can interrupt the previous recording and start recording again by waking the robot during the recording process.

- The logic is implemented in the `asr_detect_run` method in `asr.py`.
- Each time the robot is awakened, if a wake-up recording thread is already running, the thread is interrupted through the `stop_event` thread event and the program waits for it to end.
- After the stop event flag is cleared, a new recording thread is started.

```python
def asr_detect_run(self):
        while True:
            # Process only the most recent wake-up request to prevent duplicates.
            if self.wakeup_event.wait(timeout=0.1):
                self.wakeup_event.clear()
                self.extern_wakeup.set()
                self.publisher.wakeup_pub.publish(Bool(data=True))
                self.logger.info("I'm here")
                self.wake_up_voice() # Respond to the user
                if self.current_thread and self.current_thread.is_alive(): # Interrupt the previous wake-up handling thread
                    self.stop_event.set()
                    self.current_thread.join() # Wait for the current thread to finish
                    self.stop_event.clear() # Clear the event
                self.current_thread = threading.Thread(target=self.kws_handler)
                self.current_thread.daemon = True
                self.current_thread.start()
            time.sleep(0.5)
```

### 6.2 Dialogue-Stage Interruption

If you are not satisfied with the robot's spoken response or do not want it to continue speaking, use the wake word to interrupt speech playback and start recording a new voice command. At this point, you can give a new command within the current task cycle, or say "End current task" to end the current task and start a new task cycle.

- The logic is implemented in the `wakeup_callback` and `play_audio` methods of the `CustomActionServer` class in `action_service.py`.
- `wakeup_callback` handles wake-up processing. In `asr.py`, every detected wake-up signal is published through topic communication, and `wakeup_callback` subscribes to and processes that signal.
- Each time wake-up occurs, the callback checks whether `pygame.mixer` is playing audio. If audio is playing, it uses the `self.stop_event` thread event to notify the playback thread to stop.
- If an action is running after wake-up is detected, the `self.interrupt_flag` flag is set for later action interruption.

```python
def wakeup_callback(self, msg):
    if msg.data:
        if pygame.mixer.music.get_busy():
            self.stop_event.set()
        if self.action_runing:
            self.interrupt_flag = True
            self.stop()
            self.pubSix_Arm(self.init_joints)
```

When `play_audio` is playing audio, it checks whether `self.asr_detect.extern_wakeup` is set. If it is set, the function immediately stops the currently playing audio.

```python
def play_audio(self, file_path: str) -> None:
    '''Play audio'''
    self.asr_detect.extern_wakeup.clear()
    with self.pygame_lock:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if self.asr_detect.extern_wakeup.is_set():
                pygame.mixer.music.stop()
                self.asr_detect.extern_wakeup.clear()
                break
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
```

### 6.3 Action-Stage Interruption

If the robot is interrupted while executing an action, it stops the current action and returns to its initial posture. Action interruption can be divided into two types: normal action interruption and action interruption with subprocesses.

#### 6.3.1 Normal Action Interruption

- Chassis movement and robotic arm movement are controlled by publishing velocity topics and robotic arm joint-angle topics.
- The `_execute_action` chassis-control function continuously checks the `self.interrupt_event` interruption flag. If the flag is set, chassis movement stops immediately.
- Similarly, the `pubSix_Arm` robotic-arm control function checks the `self.interrupt_event` interruption flag. It publishes robotic-arm joint-angle topics only when the flag is not set.

```python
def _execute_action(self, twist, num=1, durationtime=3.0):
    for _ in range(num):
        start_time = time.time()
        while (time.time() - start_time) < durationtime:
            if self.interrupt_flag:
                self.stop()
                return
            self.publisher.publish(twist)
            time.sleep(0.1)

def pubSix_Arm(self, joints, id=6, angle=180.0, runtime=2000):
    arm_joint = ArmJoints()
    arm_joint.joint1 = joints[0]
    arm_joint.joint2 = joints[1]
    arm_joint.joint3 = joints[2]
    arm_joint.joint4 = joints[3]
    arm_joint.joint5 = joints[4]
    arm_joint.joint6 = joints[5]
    arm_joint.time = runtime
    if not self.interrupt_flag:
        self.TargetAngle_pub.publish(arm_joint)
```

#### 6.3.2 Interrupting Actions with Subprocesses

Some actions, such as robotic arm gripping and AprilTag sorting, start external programs in subprocesses. The following example uses the robotic arm gripping function `grasp_obj`.

Before robotic arm gripping is complete, the program waits continuously in the `while not self.grasp_obj_future.done():` loop. During this process, if the `self.interrupt_event` flag is detected, the corresponding `__reset_grasp_obj()` function is called first. This recursively ends the subprocess tree, then the action stops.

```python
def grasp_obj(self, x1, y1, x2, y2) -> None:
        """grasp_obj: grasp an object.

        x1, y1, x2, y2: target object bounding-box coordinates.
        """

        def __reset_grasp_obj():
            kill_process_tree(self.grasp_obj_process_1.pid)
            kill_process_tree(self.grasp_obj_process_2.pid)
            kill_process_tree(self.grasp_obj_process_3.pid)
            self.grasp_obj_future = Future()

        cmd_1 = ['ros2', 'run', 'largemodel_arm', 'grasp_desktop']
        cmd_2 = ['ros2', 'run', 'largemodel_arm', 'KCF_follow']
        cmd_3 = ['ros2', 'run', 'M3Pro_KCF', 'ALM_KCF_Tracker_Node']
        self.grasp_obj_process_1 = subprocess.Popen(cmd_1)
        time.sleep(5.0) # Wait for grasp_desktop to finish starting up.
        self.grasp_obj_process_2 = subprocess.Popen(cmd_2)
        self.grasp_obj_process_3 = subprocess.Popen(cmd_3)
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        while not self.object_position_pub.get_subscription_count():
            time.sleep(0.5)
        self.object_position_pub.publish(Int16MultiArray(data=[x1, y1, x2, y2]))
        while not self.grasp_obj_future.done():
            if self.interrupt_event.is_set():
                __reset_grasp_obj()
                self.pubSix_Arm(self.init_joints)
                return None
            time.sleep(0.1)
        result = self.grasp_obj_future.result()
        if not self.interrupt_event.is_set():
            if result.data == "grasp_obj_done":
                res = True
            else:
                res = False
        __reset_grasp_obj()
        if self.interrupt_event.is_set():
            time.sleep(0.5)
            self.pubSix_Arm(self.init_joints) # Retract the robotic arm.
        return res
```
