# coding:utf-8
import argparse
import time
from http_api import *

# 默认API地址
DEFAULT_URL = "https://aibook-api.mthreads.com:62220/api/v1/asr"

# 默认鉴权token
DEFAULT_TOKEN = None

# 默认音频来源
DEFAULT_AUDIO_TYPE= 'upload'

# 默认待识别文件路径
DEFAULT_INPUT_FILE = "demo.wav"

# 默认音频URL
DEFAULT_AUDIO_URL = "https://mt-ai-speech-public.tos-cn-beijing.volces.com/%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%A5%B3%E5%A3%B0.mp3"

# 音频格式
FORMAT = "wav"

# 领域
DOMAIN = "general"

# 语言
LANGUAGE = "cn"

# 语言模型ID
LM_ID = None

# 热词ID
VOCABULARY_ID = None

# 是否使能标点
ENABLE_PUNCTUATION = True

# 是否使能ITN
ENABLE_ITN = True

# 是否去除语气词
REMOVE_DISFLUENCY = False

# 是否使能说话人信息
ENABLE_SPEAKER_INFO = False

# 是否显示置信度
SHOW_CONFIDENCE = False

# 是否显示词级别信息
SHOW_WORDS = False

# 是否使能语义断句
ENABLE_SEMANTIC_SENTENCE_DETECTION = False

# 单段最大时长
MAX_SINGLE_SEGMENT_TIME = -1

# 最大句子长度
MAX_SENTENCE_LENGTH = 5

# 最小段落长度
MIN_PARAGRAPH_LENGTH = -1

# 最大段落长度
MAX_PARAGRAPH_LENGTH = -1

# 特殊词过滤
SPECIAL_WORD_FILTER = None

# 回调地址
CALLBACK = None

# 是否使能查询
ENABLE_QUERY = False

# 是否只处理第一声道
FIRST_CHANNEL_ONLY = False

# 是否声道分离
CHANNEL_SPLIT = True

# 分片大小（10MB）
CHUNK_SIZE = 1024 * 1024 * 10


def build_config(args):
    """构建请求配置"""
    config = {
        "domain": DOMAIN,
        "language": LANGUAGE,
        "audio_type": args.audio_type,
        "format": FORMAT,
        "lm_id": LM_ID,
        "vocabulary_id": args.vocabulary_id,
        "enable_punctuation": args.enable_punctuation,
        "enable_itn": args.enable_itn,
        "remove_disfluency": REMOVE_DISFLUENCY,
        "enable_speaker_info": ENABLE_SPEAKER_INFO,
        "show_confidence": SHOW_CONFIDENCE,
        "show_words": SHOW_WORDS,
        "enable_semantic_sentence_detection": ENABLE_SEMANTIC_SENTENCE_DETECTION,
        "max_single_segment_time": MAX_SINGLE_SEGMENT_TIME,
        "max_sentence_length": MAX_SENTENCE_LENGTH,
        "min_paragraph_length": MIN_PARAGRAPH_LENGTH,
        "max_paragraph_length": MAX_PARAGRAPH_LENGTH,
        "special_word_filter": SPECIAL_WORD_FILTER,
        "callback": CALLBACK,
        "enable_query": ENABLE_QUERY,
        "first_channel_only": FIRST_CHANNEL_ONLY,
        "channel_split": CHANNEL_SPLIT,
    }
    return config


def recognize_by_url(args):
    """通过URL方式提交识别任务"""
    config = build_config(args)
    config['audio_type'] = 'url'

    try:
        response = submit_task(config, url=args.audio_url, endpoint=args.url, token=args.token)
        while True:
            result = query_result(response['task_id'], endpoint=args.url, token=args.token)
            if check_result(result):
                break
            time.sleep(1)
    except Exception as e:
        print("Error: {}".format(e))


def recognize_by_upload(args):
    """通过上传文件方式提交识别任务"""
    config = build_config(args)
    config['audio_type'] = 'upload'

    try:
        response = submit_task(config, endpoint=args.url, token=args.token)
        task_id = response['task_id']
        response = upload_data(task_id, args.input_file, CHUNK_SIZE, endpoint=args.url, token=args.token)
        response = upload_done(task_id, args.input_file, endpoint=args.url, token=args.token)
        while True:
            result = query_result(task_id, endpoint=args.url, token=args.token)
            if check_result(result):
                break
            time.sleep(1)
    except Exception as e:
        print("Error: {}".format(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="录音文件识别示例")
    parser.add_argument("--url", default=DEFAULT_URL, type=str, help="API地址")
    parser.add_argument("--token", default=DEFAULT_TOKEN, type=str, help="鉴权token")
    parser.add_argument("--audio_type", choices=["url", "upload"], default=DEFAULT_AUDIO_TYPE, type=str, help="音频提交方式")
    parser.add_argument("--input_file", default=DEFAULT_INPUT_FILE, type=str, help="待识别音频文件路径")
    parser.add_argument("--audio_url", default=DEFAULT_AUDIO_URL, type=str, help="待识别音频URL")
    parser.add_argument("--enable_punctuation", type=lambda x: (str(x).lower() == 'true'), default=ENABLE_PUNCTUATION, help="是否使能标点")
    parser.add_argument("--enable_itn", type=lambda x: (str(x).lower() == 'true'), default=ENABLE_ITN, help="是否使能ITN")
    parser.add_argument("--vocabulary_id", type=str, default=VOCABULARY_ID, help="热词ID")
    args = parser.parse_args()

    if args.token is None:
        raise RuntimeError("Token is not specified")
    if args.audio_type == "url":
        recognize_by_url(args)
    else:
        recognize_by_upload(args)
