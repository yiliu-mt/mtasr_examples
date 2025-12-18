# Recording Recognition

This is a demo for the recording file recognition client using HTTP API. It supports using an audio URL or uploading a file as the source.

Supported languages:

- Python

## Python Example

Python examples are available in the `python` directory.

### Install Dependencies

To install the required dependencies, use the following command:

```bash
pip install requests
```

### Run Demo

The example submits an audio file for recognition and queries the result. Various options are listed in the very beginning of the example. You can change options as you like.

> ***Note:*** To access the server, you may need to modify the URL and authorization token in the demo script.

#### Using Audio URL

Submit a recognition task using an audio URL:

``` sh
python python/recording_recognition.py \
    --url https://aibook-api.mthreads.com:62220/api/v1/asr \
    --token "<token>" \
    --audio_type url \
    --audio_url "<audio_url>"
```

#### Using File Upload

Submit a recognition task by uploading a local audio file:

``` sh
python python/recording_recognition.py \
    --url https://aibook-api.mthreads.com:62220/api/v1/asr \
    --token "<token>" \
    --audio_type upload \
    --input_file python/demo.wav
```

### Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--url` | `https://aibook-api.mthreads.com:62220/api/v1/asr` | API endpoint URL |
| `--token` | - | Authorization token |
| `--audio_type` | `url` | Audio submission method: `url` or `upload` |
| `--input_file` | `demo.wav` | Path to the audio file (for upload mode) |
| `--audio_url` | - | URL of the audio file (for url mode) |
| `--enable_punctuation` | `true` | Enable punctuation in the result |
| `--enable_itn` | `true` | Enable ITN (Inverse Text Normalization) |
| `--vocabulary_id` | `None` | Hotword vocabulary ID |

### API Workflow

The recording recognition uses HTTP API with the following workflow:

1. **Submit Task**: Send a POST request to `/submit` with the configuration and audio URL (for URL mode) or just the configuration (for upload mode).

2. **Upload Audio** (upload mode only):
   - Send audio data in chunks to `/<task_id>/upload`
   - Call `/<task_id>/uploaddone` when upload is complete with MD5 checksum

3. **Query Result**: Poll `/<task_id>/query` until the recognition is complete (status code 1000).

### Output Example

The output of the demo will look something like this:

```
{'status_text': 'success', 'task_id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'}
{'status': 1000, 'status_text': 'success', 'result': [{'text': '你好欢迎使用摩尔线程语音识别。', 'words': [...]}]}
```
