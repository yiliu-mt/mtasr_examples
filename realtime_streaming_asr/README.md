# Real-time Streaming ASR

This is a demo for the real-time streaming ASR client using WebSocket.

Supported languages:

- C++

- Python

## C++ Example

C++ example is [here](https://github.com/yiliu-mt/mtasr_examples_cpp)

## Python Example

Python examples are available in the `python` directory.

### Install Dependencies

To install the required dependencies, use the following command:

```bash
pip install websocket-client
```

### Run Demo

The example reads an audio and call the ASR service. Various options are listed in the very beginning of the example. You can change options as you like.

> ***Note:*** To access the server, you may need to modify the URL and authorization token in the demo script. Set the token to `None` if no authorization is needed.
>
> The authorization methods are different for the cloud service and the local AI Box. **You should always specify the mode you are using.** The default is the **cloud** mode.

Use this to run the demo:

``` sh
# For cloud service
python python/realtime_asr_demo.py --mode cloud --url wss://api.mthreads.com/api/v1/asr --token <token> --input_file python/demo.wav
# For local AI Box
python python/realtime_asr_demo.py --mode local --url wss://127.0.0.1/api/v1/asr --token <token> --input_file python/demo.wav
```

You should use the correct URL of the service. In the script, you can control the speed of audio data transmission as per your requirement. The default script uses `time.sleep(0.001)` for rapid transmission. To simulate more realistic application scenarios, you can change this to `time.sleep(interval)`, where 'interval' represents the time in seconds (e.g., 0.16 for 160ms) between sending audio chunks.

Serveral call-back functions are called during the WebSocket communication:

- `on_open`: Indicates readiness for connection.
- `on_message`: Messages are received from the server
- `on_close`: Signals disconnection from the server and readiness to close the connection.
- `on_error`: Executed when an error occurs during the connection.

The demo will output the messages received from the server and the final result. You can modify the callback functions as needed to utilize the returned messages.

### Output Example

The output of the demo will look something like this:

    {"header":{"task_id":"eb7f61ba","type":"TranscriptionStarted","status":1000,"status_text":"Success"},"payload":{"index":1}}
    {"header":{"task_id":"eb7f61ba","type":"SentenceBegin","status":1000,"status_text":"success"},"payload":{"index":1}}
    {"header":{"task_id":"eb7f61ba","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你。","words":[]}]}}
    {"header":{"task_id":"eb7f61ba","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你好欢迎使。","words":[]}]}}
    {"header":{"task_id":"eb7f61ba","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你好欢迎使用摩尔。","words":[]}]}}
    {"header":{"task_id":"eb7f61ba","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你好欢迎使用摩尔线程。","words":[]}]}}
    {"header":{"task_id":"eb7f61ba","type":"SentenceChanged","status":1000,"status_text":"success"},"payload":{"index":1,"result":[{"text":"你好欢迎使用摩尔线程语音识别。","words":[]}]}}
    {"header":{"task_id":"eb7f61ba","type":"SentenceEnd","status":1000,"status_text":"success"},"payload":{"index":1,"start_time":860,"end_time":4180,"result":[{"text":"你好欢迎使用摩尔线程语音识别。","words":[{"text":"你","start_time":860,"end_time":960},{"text":"好","start_time":1180,"end_time":1280},{"text":"欢","start_time":1420,"end_time":1520},{"text":"迎","start_time":1540,"end_time":1640},{"text":"使","start_time":1700,"end_time":1800},{"text":"用","start_time":1860,"end_time":1960},{"text":"摩","start_time":2060,"end_time":2160},{"text":"尔","start_time":2220,"end_time":2320},{"text":"线","start_time":2460,"end_time":2560},{"text":"程","start_time":2700,"end_time":2800},{"text":"语","start_time":3100,"end_time":3200},{"text":"音","start_time":3220,"end_time":3320},{"text":"识","start_time":3380,"end_time":3480},{"text":"别","start_time":3540,"end_time":3640}]}]}}
    {"header":{"task_id":"eb7f61ba","type":"TranscriptionCompleted","status":1000,"status_text":"success"}}
    ### closed ###
    整体识别结果:
    你好欢迎使用摩尔线程语音识别。

## Hotwords

We support hotwords when doing real-time ASR. You can use our HTTP interface to add, remove and modify/update a hotword list. You can also view the details of a hotword and and list all the available lists you've ever added.

Assume you are using an AI Box, and the IP address is 127.0.0.1. You should replace \<token\> with your own token.

### Add

``` sh
curl http://127.0.0.1/api/v1/vocabularies \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d  '{
  "name":"MT",
  "description":"语音识别热词示例",
  "words":[
    "张三",
    "李四",
    "王五"
  ]
}'
```

The output looks like:

``` sh
{"status_text":"success","vocabulary_id":"c48a8333-8589-4785-aa14-570219a3a467"}
```

The vocabulary id can be used in the recognition.


### Remove

The \<vocabulary_id\> should be replaced with the target vocabulary id.

``` sh
curl http://127.0.0.1/api/v1/vocabularies/<vocabulary_id> \
   -H "Authorization: Bearer <token>" \
  -X DELETE
```

The output looks like:

``` sh
{"status_text":"success","vocabulary_id":"c48a8333-8589-4785-aa14-570219a3a467"}
```

### Modify

You can update the name, description and the hotword list of the target vocabulary id.

Update the name:

``` sh
curl http://127.0.0.1/api/v1/vocabularies/<vocabulary_id> \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name":"MT_update"
  }'
```

Update the description:

``` sh
curl http://127.0.0.1/api/v1/vocabularies/<vocabulary_id> \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "description":"语音识别热词更新版"
  }'
```

Update the hotword list:

``` sh
curl http://127.0.0.1/api/v1/vocabularies/<vocabulary_id> \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "words": [
        "朱元璋",
        "朱允炆",
        "朱棣"
    ]
  }'
```

The output looks like:

``` sh
{"status_text":"success","vocabulary_id":"c48a8333-8589-4785-aa14-570219a3a467"}
```

### View the details

``` sh
curl http://127.0.0.1/api/v1/vocabularies/<vocabulary_id> \
   -H "Authorization: Bearer <token>" \
   -X GET
```

The output looks like:

``` sh
{"status_text":"success","vocabulary":{"vocabulary_id":"c48a8333-8589-4785-aa14-570219a3a467","user_id":"liuyi","name":"MT_update","description":"语音识别热词更新版","words":["朱元璋","朱允炆","朱棣"],"version":1,"create_time":"2024-04-01T07:41:03.966959","update_time":"2024-04-01T07:41:39.164577"}}
```

### List all

Replace \<x\> and \<y\> with the desired page size and the target page (start from 1). The target page is 1 and the page size is 10 by default.

``` sh
curl http://127.0.0.1/api/v1/vocabularies?page_size=<x>&page=<y> \
   -H "Authorization: Bearer <token>" \
   -X GET
```

The output looks like:

``` sh
{"status_text":"success","vocabulary_count":2,"vocabulary_ids":["c48a8333-8589-4785-aa14-570219a3a467","18075a54-d625-4075-b46d-20b889a27a85"]}
```

### Python demo

We have shown how to manipulate the hotword lists using the Linux command *curl*. Here we also provide a Python demo to show how to do the same job. Details are in the code.

``` sh
python hotword/demo.py --url http://127.0.0.1/api/v1 --token <token> --hotword_list hotword/hotword_list.txt
```

### ASR with hotwords

You can activate the hotword using the vocab-id. The Python demo provides an interface to activate the hotword.

``` sh
# For local AI Box
python python/realtime_asr_demo.py \
    --mode local \
    --url wss://127.0.0.1/api/v1/asr \
    --token <token> \
    --input_file hotword/hotword_demo.wav \
    --vocabulary_id <vocab_id>
```

The hotword list is:
    
    明思宗
    朱由检
    明光宗
    朱常洛

Before using the hotword, the result is:

    明思宗朱有俭是崇祯皇帝，他是明代第16位皇帝是明光宗朱长洛之子。

After using the hotword, the result is:

    明思宗朱由检是崇祯皇帝，他是明代第16位皇帝是明光宗朱常洛之子。

