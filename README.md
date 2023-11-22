# MT ASR demos for developers

This repository contains the implementation of a gRPC client to require the result of the streaming result from mthreads.

Supported languages: 

- Python

## Python Usage

### Install dependencies

```
pip install mtasr
```

### Run demos

The ASR examples are in `egs/`. 

> ***Note: You may need to change the URL and token in the demo script to access the ASR server.***
>
> If the authorization is required, please use your token in the examples.

In the examples, it read the audio in demo.wav and get the recognized result from ASR server. 

You can replace the audio file or create your own applications.

1. Real-time streaming ASR

    ```
    python egs/realtime_asr_demo.py
    ```

    During sending audio data, 

    During receiving ASR result, *test_on_sentence_changed* and *test_on_sentence_end* return the recognized *result* which is a dictionary.

    For *test_on_sentence_changed*, *result* only contains the recognized content:

        [{'sentence': '你好'}]

    For *test_on_sentence_end*, *result* contains the text and the word-level information:

        [{'sentence': '你好欢迎使用摩尔线程语音识别', 'wordpieces': [{'word': '你', 'start': 860, 'end': 960}, {'word': '好', 'start': 1060, 'end': 1160}, {'word': '欢', 'start': 1380, 'end': 1480}, {'word': '迎', 'start': 1500, 'end': 1600}, {'word': '使', 'start': 1660, 'end': 1760}, {'word': '用', 'start': 1820, 'end': 1920}, {'word': '摩', 'start': 2020, 'end': 2120}, {'word': '尔', 'start': 2180, 'end': 2280}, {'word': '线', 'start': 2460, 'end': 2560}, {'word': '程', 'start': 2620, 'end': 2720}, {'word': '语', 'start': 3100, 'end': 3240}, {'word': '音', 'start': 3240, 'end': 3280}, {'word': '识', 'start': 3340, 'end': 3440}, {'word': '别', 'start': 3500, 'end': 3600}]}]


2. One-sentence streaming ASR

    ```
    python egs/one_sentence_asr_demo.py
    ```

    the result is similar to that of the realtime ASR.
