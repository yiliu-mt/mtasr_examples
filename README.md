# MT ASR Demos for Developers

This repository contains the implementation of different ASR clients.

## Real-Time Streaming ASR

This is the official API that contains the whole ASR pipeline.

### Features

* Inverse text normalization (ITN)
* Chinese punctuation
* Session-level hotwords (optional when starting a ASR connection)

[WebSocket client](https://github.com/yiliu-mt/mtasr_examples/tree/main/realtime_streaming_asr)


## gRPC

The gRPC interface only calls ASR WITHOUT any other functions.

[gRPC client](https://github.com/yiliu-mt/mtasr_examples/tree/main/grpc)
