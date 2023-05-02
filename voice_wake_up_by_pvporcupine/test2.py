import struct
import pyaudio
import pvporcupine

import faulthandler
# 在import之后直接添加以下启用代码即可
faulthandler.enable()
# 后边正常写你的代码

ACCESS_KEY = '2y5T87KZaY0yWS+8OJFnlFyMttTCX027dQ7dKCxnKclB2nx4Cvbf4A=='

# 设置采样率为 44100 16000
sample_rate = 44100

porcupine = pvporcupine.create(keywords=['ok google'],
                               sensitivities=[1],
                               access_key=ACCESS_KEY,)
# porcupine = pvporcupine.create(keyword_paths=['samel__en_windows_2021-10-26-utc_v1_9_0.ppn'])

pa = pyaudio.PyAudio()
print(porcupine.sample_rate)
print(porcupine.frame_length)
audio_stream = pa.open(
    rate=sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    input_device_index=0,  # 一定要指定好输入设备,
    frames_per_buffer=porcupine.frame_length)


def close():
    audio_stream.stop_stream()
    audio_stream.close()

    # 终止PyAudio
    pa.terminate()


def get_next_audio_frame():
    pcm = audio_stream.read(porcupine.frame_length,
                            exception_on_overflow=False)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    return pcm


while True:
    keyword_index = porcupine.process(get_next_audio_frame())
    if keyword_index >= 0:
        # Insert detection event callback here
        print('Keyword Detected')
        close()
        break
