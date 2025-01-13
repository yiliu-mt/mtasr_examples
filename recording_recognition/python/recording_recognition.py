import time
from http_api import *


endpoint = "https://api.mthreads.com/asr-dev-apis/api/v1/asr"
token = "your_token"

config = {
    "domain": "general",
    "language": "cn",
    "audio_type": "url",
    "format": "wav",
    "lm_id": None,
    "vocabulary_id": None,
    "enable_punctuation": True,
    "enable_itn": True,
    "remove_disfluency": False,
    "enable_speaker_info": False,
    "show_confidence": False,
    "show_words": False,
    "enable_semantic_sentence_detection": False,
    "max_single_segment_time": -1,
    "max_sentence_length": 5,
    "min_paragraph_length": -1,
    "max_paragraph_length": -1,
    "special_word_filter": None,
    "callback": None,
    "enable_query": False,
    "first_channel_only": False,
    "channel_split": True,
}

chunk_size = 1024 * 1024 * 1 # 1M
audio_url = 'your_audio_url'
audio_path = 'your_audio_path'

def check_result(result):
    if result['status'] == 1000:
        return True
    return False

# upload using URL
try:
    config['audio_type'] = 'url'
    response = submit_task(config, url=audio_url, endpoint=endpoint, token=token)
    while True:
        result = query_result(response['task_id'], endpoint=endpoint, token=token)
        if check_result(result):
            break
        time.sleep(1)
except Exception as e:
    print("Error: {}".format(e))


# # upload using bianry
try:
    config['audio_type'] = 'upload'
    config["format"] = "wav"
    # each chunk consists of 10 MB data
    chunk_size = 1024 * 1024 * 10
    response = submit_task(config, endpoint=endpoint, token=token)
    task_id = response['task_id']
    response = upload_data(task_id, audio_path, chunk_size, endpoint=endpoint, token=token)
    response = upload_done(task_id, audio_path, endpoint=endpoint, token=token)
    while True:
        result = query_result(task_id, endpoint=endpoint, token=token)
        if check_result(result):
            break
        time.sleep(1)
except Exception as e:
    print("Error: {}".format(e))
