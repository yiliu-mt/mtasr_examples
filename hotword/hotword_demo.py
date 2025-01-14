import argparse
import requests
import json
import time
from recording_recognition.python.http_api import *


DEFAULT_URL = "https://api.mthreads.com/asr-dev-apis/api/v1"
DEFAULT_TOKEN = "your_token_here"
DEFAULT_HOTWORD_LIST = "demo/hotword_list.txt"
audio_path = 'demo/hotword_test.wav'

def read_hotword_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        word_list = [line.strip() for line in f]
    return word_list


def add_vocab(endpoint, token, word_list):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    data = {
        "name": "test",
        "description": "热词测试",
        "words": word_list
    }
    response = requests.post(f"{endpoint}/vocabularies", headers=headers, data=json.dumps(data))
    try:
        print("Add vocabulary: code {}".format(response.status_code))
        print(response.text)
        if response.status_code != 200:
            return None
        return json.loads(response.text)['vocabulary_id']
    except:
        return None


def delete_vocab(endpoint, token, vocab_id):
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.delete(f"{endpoint}/vocabularies/{vocab_id}", headers=headers)
    try:
        print("Delete vocabulary {}: code {}".format(vocab_id, response.status_code))
        print(response.text)
    except:
        pass


def update_vocab(endpoint, token, vocab_id, name=None, description=None, word_list=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }
    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if word_list is not None:
        data["words"] = word_list
    response = requests.post(f"{endpoint}/vocabularies/{vocab_id}", headers=headers, data=json.dumps(data))
    try:
        print("Update vocabulary {}: code {}".format(vocab_id, response.status_code))
        print(response.text)
        if response.status_code != 200:
            return None
        return json.loads(response.text)['vocabulary_id']
    except:
        return None


def list_vocab(endpoint, token, vocab_id):
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.get(f"{endpoint}/vocabularies/{vocab_id}", headers=headers)
    try:
        print("List vocabulary {}: code {}".format(vocab_id, response.status_code))
        print(response.text)
    except:
        pass


def list_all_vocabularies(endpoint, token):
    params = {
        "page_size": "20",
        "page": "0"
    }
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.get(f"{endpoint}/vocabularies", headers=headers, params=params)
    try:
        print("List all vocabularies: code {}".format(response.status_code))
        print(response.text)
        return json.loads(response.text)["vocabulary_list"]
    except:
        return None


def test_wav(endpoint, token, path, vocab_id):
    config = {
        "domain": "general",
        "language": "cn",
        "audio_type": "url",
        "format": "wav",
        "lm_id": None,
        "vocabulary_id": vocab_id,
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default=DEFAULT_URL, help="the endpoint of the hotword service")
    parser.add_argument("--token", type=str, default=DEFAULT_TOKEN, help="the authorization token")
    parser.add_argument("--hotword_list", type=str, default=DEFAULT_HOTWORD_LIST, help="the target hotword list")
    args = parser.parse_args()
    # Add a hotword list
    word_list = read_hotword_file(args.hotword_list)
    #create a list
    vocab_id = add_vocab(args.url, args.token, word_list)
    # update a list
    # update the name
    vocab_id = update_vocab(args.url, args.token, vocab_id, name="test_new")
    # update the description
    vocab_id = update_vocab(args.url, args.token, vocab_id, description="热词测试更新")
    # update with a new hotword list
    vocab_id = update_vocab(args.url, args.token, vocab_id, word_list=word_list)

    # show the detail of a vocabulary id
    list_vocab(args.url, args.token, vocab_id)

    # list all vocabularies
    list_all_vocabularies(args.url, args.token)

    # test wav
    print("without hotword")
    test_wav(args.url + '/asr', args.token, audio_path, None)
    print("with hotword")
    test_wav(args.url + '/asr', args.token, audio_path, vocab_id)

    # delete a list
    delete_vocab(args.url, args.token, vocab_id)


if __name__ == '__main__':
    main()

