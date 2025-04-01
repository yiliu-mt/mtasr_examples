# coding:utf-8
import argparse
import time
import wave
import json
import uuid
import logging
import websocket
from functools import partial
from threading import Thread

# 默认WebSocket地址
DEFAULT_URL = "wss://aibook-api.mthreads.com:62220/api/v1/asr"

# 默认鉴权token
DEFAULT_TOKEN = "YOUR_TOKEN"

# 默认待识别文件路径
DEFAULT_INPUT_FILE = 'demo.wav'

# 是否使能标点
ENABLE_PUNCTUATION = True

# 是否使能ITN
ENABLE_ITN = True

# 热词ID
VOCABULARY_ID = None

# 是否流式输出中间结果
SHOW_INTERMEDIATE_RESULT = True

# 输出nbest
NBEST = 1

# 是否输出词级别信息
SHOW_WORDS = True

# 其他配置
DOMAIN = "general"
LANGUAGE = "cn"
FORMAT = "pcm"
SHOW_CONFIDENCE = False
LM_ID = None
REMOVE_DISFLUENCY = False
ENABLE_SPEAKER_INFO = False
ENABLE_SEMANTIC_SENTENCE_DETECTION = False
SPECIAL_WORD_FILTER = None

class WsClient():
    def __init__(self, args):
        self.url = args.url
        self.appid = str(uuid.uuid4().hex)
        self.config_signal = {
            "header":{
                "appid": self.appid,
                "type":"StartTranscription"
            },
            "payload":{
                "enable_punctuation": args.enable_punctuation,
                "enable_itn": args.enable_itn,
                "vocabulary_id": args.vocabulary_id,
                "nbest": args.nbest,
                "show_words": args.show_words,
                "show_intermediate_result": args.show_intermediate_result,
                "format": FORMAT,
                "domain": DOMAIN,
                "language": LANGUAGE,
                "lm_id": LM_ID,
                "remove_disfluency": REMOVE_DISFLUENCY,
                "enable_speaker_info": ENABLE_SPEAKER_INFO,
                "show_confidence": SHOW_CONFIDENCE,
                "enable_semantic_sentence_detection": ENABLE_SEMANTIC_SENTENCE_DETECTION,
                "special_word_filter": SPECIAL_WORD_FILTER,
            }
        }
        self.end_signal = {
            "header":{
                "appid": self.appid,
                "type":"StopTranscription"
            }
        }
        self.ws_header = None

        if args.token is not None and len(args.token) > 0:
            self.url = '{}?token={}'.format(self.url, args.token)
        self.final_result = ""

        # Log设置
        self.logger = logging.getLogger("RunLog")
        self.logger.setLevel(logging.INFO)

    def on_open(self, ws, file_path):
        def run(*args):
            interval = 0.16   # 每一包160ms，发送一包后等待160ms继续发送下一包音频
            frame_size = int(interval * 2 * 16000)  # 160ms音频所占字节数：16000 * 2 * 160 / 1000 = 5120

            # 读取.wav音频文件
            # 得到音频的二进制数据
            with wave.open(file_path, 'rb') as wave_fp:
                nchannels, sampwidth, framerate, nframes = wave_fp.getparams()[:4]
                wave_bytes = wave_fp.readframes(nframes)
            assert nchannels == 1 and framerate == 16000 and sampwidth == 2, \
                "The input wave should be encoded as 16kHz, 16bit mono pcm"

            index = 0
            while index < len(wave_bytes):
                if index == 0:
                    # 首先发送配置
                    ws.send(json.dumps(self.config_signal))

                # 发送数据包
                ws.send(wave_bytes[index : index + frame_size], 2)
                index += frame_size

                # 注意：在这里我们没有等待160ms，这样可以快速得到结果
                # 为了模拟真实环境，您可将该行替换为：
                # time.sleep(interval)
                time.sleep(0.001)

            # 发送尾包
            ws.send(json.dumps(self.end_signal))

        Thread(target=run).start()

    def on_message(self, ws, message):
        if json.loads(message)['header']['status'] != 1000:
            print("Error occurs: {}".format(message))
            return

        print(message)
        if json.loads(message)['header']['type'] == 'SentenceEnd':
            self.final_result += json.loads(message)['payload']['result'][0]['text']

    def on_error(self, ws, error):
        print("error: ", error)

    def on_close(self, ws, close_status_code, close_msg):
        ws.close()
        print("### closed ###")

    def send(self, file_path):
        # start websocket-client
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            header=self.ws_header,
        )
        ws.on_open = partial(self.on_open, file_path=file_path)
        ws.run_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL, type=str, help="The endpoint to connect to")
    parser.add_argument("--token", default=DEFAULT_TOKEN, type=str, help="The authorization token")
    parser.add_argument("--input_file", default=DEFAULT_INPUT_FILE, type=str, help="The input file path")
    parser.add_argument("--enable_punctuation", type=lambda x: (str(x).lower() == 'true'), default=ENABLE_PUNCTUATION, help="Enable punctuation")
    parser.add_argument("--enable_itn", type=lambda x: (str(x).lower() == 'true'), default=True, help="Enable ITN")
    parser.add_argument("--vocabulary_id", type=str, default=VOCABULARY_ID, help="Use session-level hotword")
    parser.add_argument("--show_intermediate_result", type=lambda x: (str(x).lower() == 'true'), default=True, help="Output the intermediate result")
    parser.add_argument("--nbest", type=int, default=NBEST, help="Output the nbest results")
    parser.add_argument("--show_words", type=lambda x: (str(x).lower() == 'true'), default=True, help="Output the word-level information in the result")
    args = parser.parse_args()
    ws_client = WsClient(args)
    ws_client.send(args.input_file)
    print('整体识别结果:\n{}'.format(ws_client.final_result))

