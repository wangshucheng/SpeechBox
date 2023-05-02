import pyaudio
import pvporcupine
import numpy as np
import scipy.signal as signal
import math

ACCESS_KEY = '2y5T87KZaY0yWS+8OJFnlFyMttTCX027dQ7dKCxnKclB2nx4Cvbf4A=='

# 设置采样率为 44100 16000
sample_rate = 44100

porcupine = pvporcupine.create(keywords=['ok google'],
                               sensitivities=[1],
                               access_key=ACCESS_KEY)
# porcupine = pvporcupine.create(keyword_paths=['samel__en_windows_2021-10-26-utc_v1_9_0.ppn'])

input_rate = sample_rate
output_rate = porcupine.sample_rate
frame_length = porcupine.frame_length
input_frame_length = math.ceil(frame_length / (output_rate / input_rate))

pa = pyaudio.PyAudio()

audio_stream = pa.open(
    rate=sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    input_device_index=0,  # 一定要指定好输入设备,
    frames_per_buffer=input_frame_length)


def close():
    audio_stream.stop_stream()
    audio_stream.close()

    # 终止PyAudio
    pa.terminate()

    porcupine.delete()

# 难点，理解重采样，采样率和帧长度的关系，
# 根据输入输出的采样率和输出帧长度，确定输入帧长度，然后使用重采样库计算
def get_next_audio_frame():
    pcm = audio_stream.read(input_frame_length)

    # 将音频数据从字节流转换为numpy数组
    audio = np.frombuffer(pcm, dtype=np.int16)

    # 重采样音频数据
    resampled_audio = signal.resample(audio, int(len(audio) * 16000 / 44100))

    resampled_audio = np.round(resampled_audio).astype(np.int16)

    return resampled_audio


while True:
    keyword_index = porcupine.process(get_next_audio_frame())
    if keyword_index >= 0:
        # Insert detection event callback here
        print('Keyword Detected')
        close()
        break
