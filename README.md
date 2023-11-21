# MT ASR interface for developers

This repository contains the implementation of a gRPC client to require the result of the streaming result from mthreads.

## Usage

1. Install dependencies

```
pip install mtasr
```

2. ASR Demos

The ASR examples are in `egs/`. 

**Note: You may need to change the URL in the demo script to access the ASR server**

In the examples, it read the audio in demo.wav and get the recognized result from ASR server. 

You can replace the audio file or create your own applications.

    1. Real-time streaming ASR

    ```
    python egs/realtime_asr_demo.py
    ```

    2. One-sentence streaming ASR

    ```
    python egs/one_sentence_asr_demo.py
    ```

