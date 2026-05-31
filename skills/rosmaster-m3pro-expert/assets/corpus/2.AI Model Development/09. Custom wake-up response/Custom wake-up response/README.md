# Custom Wake-Up Response

## 1. Course Content

Add audio files to the `multi_brains` audio library to customize the voice response played after wake-up.

> [!NOTE]
> This section is only for users who need custom voice responses. It does not affect normal use.
>
> If you do not need custom responses, skip this section.

## 2. Prepare Audio Files

- You can download and prepare voice-response audio files yourself.
- You can also generate speech using the built-in `generate_voice` command. Speech generation uses the speech synthesis model from the Bailian platform, so configure `ALIYUN_API_KEY` first, as described in **02 - Configuring API-KEY**.
- Preconfigure the Bailian API key.

![Figure: page 0: figure 12](_page_0_Figure_12.jpeg)

Run the command in the terminal:

```bash
generate_voice --text Hello
```

`--text` is the startup parameter. Replace `Hello` with the text you want to synthesize into speech.

The audio file is saved automatically in `~/generate_voices/`.

> [!NOTE]
> Other optional startup parameters:
>
> - `--voice`: Speaker, default `Cherry`
> - `--language_type`: Language, default Chinese
> - `--save_path`: Audio file save path, default `~/generate_voices/`
> - `--config_file`: Configuration file path, default `~/M3Pro_ws/multi_brains_file/multi_brains_setting.yaml`
> - `--text`: Text to synthesize into audio, default empty
> - `--model`: Speech synthesis model, default `qwen3-tts-flash`

For available speakers and speech synthesis models, refer to the dynamic notices on the [Bailian official website](https://bailian.console.aliyun.com/?spm=5176.29619931.J_SEsSjsNv72yRuRFS2VknO.2.74cd10d73l2Pw5&tab=doc#/doc/?type=model&url=2879134).

Reference model:

### Speech Synthesis: Qwen

## Model Availability

Qwen3-TTS-Flash is recommended.

Qwen3-TTS-Flash offers 49 voices and supports multiple languages and dialects.

Qwen-TTS offers up to 7 voices and supports only Chinese and English.

International (Singapore) / China (Beijing)

| Model                                                                       | Version  |
|-----------------------------------------------------------------------------|----------|
| qwen3-tts-flash  Capabilities are identical to qwen3- tts-flash-2025-09-18. | Stable   |
| qwen3-tts-flash-2025-11-27                                                  | Snapshot |
| qwen3-tts-flash-2025-09-18                                                  | Snapshot |

Reference voices:

| Name    | `voice` parameter |
|---------|-------------------|
| Cherry  | Cherry            |
| Serena  | Serena            |
| Ethan   | Ethan             |
| Chelsie | Chelsie           |
| Momo    | Momo              |
| Vivian  | Vivian            |
| Moon    | Moon              |

Supported languages:

Chinese, English, Spanish, Russian, Italian, French, Korean, Japanese, German, Portuguese

## 3. Load Audio Files

`multi_brains` system audio path:

```text
~/M3Pro_ws/src/multi_brains/system_vioce
```

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

The `zh` directory stores Chinese response voices and is suitable for domestic users. Place prepared audio files in this directory:

![Picture: page 4: picture 3](_page_4_Picture_3.jpeg)

The `en` directory stores English response voices and is suitable for international users. Place prepared audio files in this directory:

![Picture: page 4: picture 5](_page_4_Picture_5.jpeg)

When the `multi_brains` program starts, it automatically loads audio files from the corresponding directory and randomly plays custom response voices when the user wakes the system.
