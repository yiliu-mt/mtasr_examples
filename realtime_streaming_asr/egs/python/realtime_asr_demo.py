# coding:utf-8
import time
import wave
import json
import uuid
import logging
import websocket
from functools import partial
from threading import Thread

URL = "ws://api.mthreads.com/api/v1/asr"

# 鉴权token
TOKEN = None
# TOKEN = "YOUR_TOKEN"

# 在此使用您的音频
FILE_PATH = "demo.wav"
# FILE_PATH = "YOUR_WAV_FILE_PATH.wav"

# 相关配置
DOMAIN = "general"
LANGUAGE = "cn"
FORMAT = "pcm"
VOCABULARY_ID = None
LM_ID = None
ENABLE_PUNCTUATION = True
ENABLE_ITN = True
REMOVE_DISFLUENCY = False
ENABLE_SPEAKER_INFO = False
NBEST = 1
SHOW_CONFIDENCE = False
SHOW_WORDS = True
SHOW_INTERMEDIATE_RESULT = True
ENABLE_SEMANTIC_SENTENCE_DETECTION = False
SPECIAL_WORD_FILTER = None

# 保存所有识别结果
final_result = ""

class WsClient():
    def __init__(self):
        self.url = URL
        self.appid = TOKEN if TOKEN is not None else str(uuid.uuid4().hex)
        self.config_signal = {
            "header":{
                "appid": self.appid,
                "type":"StartTranscription"
            },
            "payload":{
                "format": FORMAT,
                "domain": DOMAIN,
                "language": LANGUAGE,
                "vocabulary_id": VOCABULARY_ID,
                "lm_id": LM_ID,
                "enable_punctuation": ENABLE_PUNCTUATION,
                "enable_itn": ENABLE_ITN,
                "remove_disfluency": REMOVE_DISFLUENCY,
                "enable_speaker_info": ENABLE_SPEAKER_INFO,
                "nbest": NBEST,
                "show_words": SHOW_WORDS,
                "show_confidence": SHOW_CONFIDENCE,
                "show_intermediate_result": SHOW_INTERMEDIATE_RESULT,
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
        if TOKEN is not None:
            self.ws_header = {"Authorization": TOKEN}
                    
        # Log设置
        self.logger = logging.getLogger("RunLog")
        self.logger.setLevel(logging.INFO)
    
    def on_open(self, ws, file_path):
        def run(*args):
            interval = 0.16   # 每一包160ms，发送一包后等待160ms继续发送下一包音频
            frame_size = 5120  # 160ms音频所占字节数：16000 * 2 * 160 / 1000 = 5120

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
        global final_result
        print(message)
        if json.loads(message)['header']['type'] == 'SentenceEnd':
            final_result += json.loads(message)['payload']['result'][0]['text']

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
    ws_client = WsClient()
    ws_client.send(FILE_PATH)
    print('整体识别结果:\n{}'.format(final_result))

