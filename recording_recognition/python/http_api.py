import hashlib
import copy
import json
import requests
import logging as log


def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def submit_task(config, url=None, endpoint=None, token=None):
    this_token = token
    this_endpoint = endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(this_token)
    }
    data = copy.deepcopy(config)
    if url is not None:
        data['audio_type'] = 'url'
        data['url'] = url
    while True:
        try:
            response = requests.post(f"{this_endpoint}/submit", headers=headers, data=json.dumps(data))
            response_json = json.loads(response.text)
            log.warning(response_json)
            if response.status_code == 200:
                break
        except:
            log.error("submit failed. retry...")
    return response_json

    
def query_result(taskid, endpoint=None, token=None):
    this_token = token
    this_endpoint = endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(this_token)
    }
    while True:
        try:
            response = requests.get(f"{this_endpoint}/{taskid}/query", headers=headers)
            response_json = json.loads(response.text)
            log.warning(response_json)
            if response.status_code == 200:
                break
        except:
            log.error("query failed. retry...")
    return response_json


def upload_data(taskid, audio_path, chunk_size=1000000, endpoint=None, token=None):
    this_token = token
    this_endpoint = endpoint
    with open(audio_path, 'rb') as file:
        binary_data = file.read()

    for start in range(0, len(binary_data), chunk_size):
        data = binary_data[start:start + chunk_size]
        headers = {
            'Content-Type': 'application/octet-stream',
            "Authorization": "Bearer {}".format(this_token),
        }
        # upload until successful
        while True:
            try:
                response = requests.post(f"{this_endpoint}/{taskid}/upload", headers=headers, data=data)
                response_json = json.loads(response.text)
                log.warning(response_json)
                if response.status_code == 200:
                    break
            except:
                log.error("upload data failed. retry...")
    log.warning("upload data finished")
    return response_json


def upload_done(taskid, audio_path, endpoint=None, token=None):
    this_token = token
    this_endpoint = endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(this_token)
    }
    data = {
        "md5": "{}".format(get_md5(audio_path))
    }
    while True:
        try:
            response = requests.post(f"{this_endpoint}/{taskid}/uploaddone", headers=headers, data=json.dumps(data))
            response_json = json.loads(response.text)
            log.warning(response_json)
            if response.status_code == 200:
                break
        except:
            log.error("upload done failed. retry...")
    log.warning("upload done finished")
    return response_json


def check_result(result):
    if result['status'] == 1000:
        return True
    return False

