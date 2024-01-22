# Real-time Streaming ASR

This is a demo for the real-time streaming ASR client using WebSocket.

Supported languages:

- C++

- Python

## C++ Example

TBD

## Python Example

Python examples are available in the `egs/python` directory.

### Install Dependencies

To install the required dependencies, use the following command:

```bash
pip install websocket-client
```

### Run Demo

> ***Note:*** To access the server, you may need to modify the URL and token in the demo script. If authorization is required, replace 'TOKEN' with your actual token. Set it to `None` if no authorization is needed.

The example reads audio from `demo.wav` and call the ASR service. Various options are listed in the very beginning of the example. You can change options as you like.

To run the demo:

```bash
python egs/python/realtime_asr_demo.py
```

Control the speed of audio data transmission as per your requirement. The default script uses `time.sleep(0.001)` for rapid transmission. To simulate more realistic application scenarios, you can change this to `time.sleep(interval)`, where 'interval' represents the time in seconds (e.g., 0.16 for 160ms) between sending audio chunks.

Serveral call-back functions are called during the WebSocket communication:

- `on_open`: Indicates readiness for connection.
- `on_message`: Messages are received from the server
- `on_close`: Signals disconnection from the server and readiness to close the connection.
- `on_error`: Executed when an error occurs during the connection.

The demo will output the messages received from the server and the final result. You can modify the callback functions as needed to utilize the returned messages.

### Output Example

The output of the demo will look something like this:

    {"header":{"task_id":"d3dad63f","type":"TranscriptionStarted","status":1000,"status_text":"Success"},"payload":{"index":1}}
    {"header":{"task_id":"d3dad63f","type":"SentenceBegin","status":1000,"status_text":"success"},"payload":{"index":1}}
    {"header":{"task_id":"d3dad63f","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你好","words":[]}]}}
    {"header":{"task_id":"d3dad63f","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你好欢迎使","words":[]}]}}
    {"header":{"task_id":"d3dad63f","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你好欢迎使用摩尔","words":[]}]}}
    {"header":{"task_id":"d3dad63f","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你好欢迎使用摩尔线程","words":[]}]}}
    {"header":{"task_id":"d3dad63f","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你好欢迎使用摩尔线程语音识别","words":[]}]}}
    {"header":{"task_id":"d3dad63f","type":"SentenceEnd","status":1000,"status_text":"success"},"payload":{"index":1,"start_time":860,"end_time":3600,"result":[{"text":"你好欢迎使用摩尔线程语音识别","words":[{"text":"你","start_time":860,"end_time":960},{"text":"好","start_time":1060,"end_time":1160},{"text":"欢","start_time":1380,"end_time":1480},{"text":"迎","start_time":1500,"end_time":1600},{"text":"使","start_time":1660,"end_time":1760},{"text":"用","start_time":1820,"end_time":1920},{"text":"摩","start_time":2020,"end_time":2120},{"text":"尔","start_time":2180,"end_time":2280},{"text":"线","start_time":2460,"end_time":2560},{"text":"程","start_time":2620,"end_time":2720},{"text":"语","start_time":3100,"end_time":3240},{"text":"音","start_time":3240,"end_time":3280},{"text":"识","start_time":3340,"end_time":3440},{"text":"别","start_time":3500,"end_time":3600}]}]}}
    {"header":{"task_id":"d3dad63f","type":"TranscriptionCompleted","status":1000,"status_text":"success"}}
    ### closed ###
    整体识别结果:
    你好欢迎使用摩尔线程语音识别
