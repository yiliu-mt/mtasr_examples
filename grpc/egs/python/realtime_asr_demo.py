import time
import json
import wave
import uuid
import mtasr


# change the url if necessary
url = "api.mthreads.com:53966"
# enter your token here
token = ""

# 在此使用您的音频
file_path = "demo.wav"

# The final result that concatenates all sentences together
final_result = ""

def slice_data(data, chunk_size):
    data_len = len(data)
    offset = 0
    while offset + chunk_size < data_len:
        yield data[offset: offset + chunk_size]
        offset += chunk_size
    else:
        yield data[offset: data_len]


class RealTimeASR():
    def __init__(self, url, token):
        self.url = url
        self.client = mtasr.RealTimeClient(
            url=self.url,
            token=token,
            req_id=uuid.uuid4().hex,
            nbest=1,
            on_start=self.test_on_start,
            on_sentence_changed=self.test_on_sentence_changed,
            on_sentence_end=self.test_on_sentence_end,
            on_completed=self.test_on_completed,
            on_error=self.test_on_error
        )

    def test_on_start(self, message, **_kwargs):
        print("test_on_start: {}".format(message))

    def test_on_sentence_changed(self, message, result, **_kwargs):
        print("test_on_chg: {}. Result: {}".format(message, json.dumps(result, ensure_ascii=False)))

    def test_on_sentence_end(self, message, result, **_kwargs):
        global final_result
        print("test_on_sentence_end: {}. Result: {}".format(message, json.dumps(result, ensure_ascii=False)))
        # concatenate all sentences
        if len(result[0]['sentence']) > 0:
            final_result += result[0]['sentence'] + '。'

    def test_on_completed(self, message, *args):
        print("on_completed: {}".format(message))

    def test_on_error(self, message, *args):
        print("on_error: {}".format(message))

    def send(self, file_path):
        with wave.open(file_path, 'rb') as wave_fp:
            nchannels, sampwidth, framerate, nframes = wave_fp.getparams()[:4]
            wave_bytes = wave_fp.readframes(nframes)
        assert framerate == 16000 and sampwidth == 2, "Only support 16K 16bit wav"

        # each chunk contains 160ms
        chunk_size = 0.160
        num_bytes = int(chunk_size * 16000 * 2)
        index = 0
        while index < len(wave_bytes):
            self.client.send(wave_bytes[index:index + num_bytes])
            index += num_bytes

            # Note: If you want to simulate the process of a practical application,
            # you can change the following line to:
            # time.sleep(chunk_size)
            time.sleep(0.001)
        self.client.stop()

    def close(self):
        self.client.close()


if __name__ == '__main__':
    client = RealTimeASR(url, token)
    client.send(file_path)
    client.close()
    print('整体识别结果:\n{}'.format(final_result))

