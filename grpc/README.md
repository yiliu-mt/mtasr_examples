# [Deprecated] gRPC client demo

The gPRC client provides a low-level ASR client and returns the raw ASR results.

Supported languages:

- [Python](https://github.com/yiliu-mt/mtasr_examples/tree/main/grpc/egs/python)
- [C++](https://github.com/yiliu-mt/mtasr_examples_cpp)

## Python Examples

Python examples can be found in `egs/python`.

### Install Dependencies

```bash
pip install mtasr
```

### Run Demos

> ***Note: You may need to change the URL and token in the demo script to access the ASR server.***
>
> If authorization is required, please use your token in the examples.

In these examples, the script reads audio from `demo.wav` and retrieves the recognized result from the ASR server.

You can replace the audio file or create your own applications.

1. Real-time Streaming ASR

    ```bash
    python egs/python/realtime_asr_demo.py
    ```

    While sending audio data, you can control the sending speed. To get results as soon as possible, use the example script. To simulate practical applications, change `time.sleep(0.001)` to `time.sleep(chunk_size)`. This change makes the sending process wait 160ms before sending the next audio chunk, mimicking practical applications.

    During the receipt of ASR results, you can create multiple self-defined callbacks to handle the results returned by the ASR server:

    - `test_on_start` and `test_on_completed` are called when recognition starts and completes.
    
    - `test_on_sentence_changed` and `test_on_sentence_end` are called when the recognized result of a sentence changes or finishes.

    - `test_on_error` is called when an error occurs.

    In `test_on_sentence_changed` and `test_on_sentence_end`, the recognized result is returned as a dictionary in *result*.

    For `test_on_sentence_changed`, *result* only contains the recognized content:

        [{'sentence': '你好'}]

    For `test_on_sentence_end`, *result* includes the text and word-level information:

        [{'sentence': '你好欢迎使用摩尔线程语音识别', 'wordpieces': [{'word': '你', 'start': 860, 'end': 960}, {'word': '好', 'start': 1060, 'end': 1160}, ... (and so on) ...]}]

2. One-sentence Streaming ASR

    ```bash
    python egs/one_sentence_asr_demo.py
    ```

    The result is similar to that of the real-time ASR.
