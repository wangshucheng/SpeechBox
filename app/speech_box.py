
import pyaudio
import pvporcupine
import numpy as np
import scipy.signal as signal
import os
import math
from threading import Thread
from pvrecorder import PvRecorder
import audio_agent as AAgent
import baidu_agent as BAgent
import chat_agent as CAgent
import pyttsx3_agent as PAgent

ACCESS_KEY = '2y5T87KZaY0yWS+8OJFnlFyMttTCX027dQ7dKCxnKclB2nx4Cvbf4A=='
KEYWORD = 'computer'

current_path = os.path.dirname(os.path.abspath(__file__))

# 设置采样率为 44100 16000
sample_rate = 44100

porcupine = pvporcupine.create(keywords=[KEYWORD],
                               sensitivities=[1],
                               access_key=ACCESS_KEY)

input_rate = sample_rate
output_rate = porcupine.sample_rate
frame_length = porcupine.frame_length
input_frame_length = math.ceil(frame_length / (output_rate / input_rate))

pa = pyaudio.PyAudio()


def close():

    # 终止PyAudio
    pa.terminate()

    porcupine.delete()


class SpeechBox(Thread):
    def __init__(
            self,
            audio_input_path,
            audio_output_path):

        super(SpeechBox, self).__init__()

        self._audio_input_path = audio_input_path
        self._audio_output_path = audio_output_path

        self._history = []

    # 难点，理解重采样，采样率和帧长度的关系，
    # 根据输入输出的采样率和输出帧长度，确定输入帧长度，然后使用重采样库计算
    def get_next_audio_frame(self):
        pcm = self._audio_stream.read(input_frame_length)

        # 将音频数据从字节流转换为numpy数组
        audio = np.frombuffer(pcm, dtype=np.int16)

        # 重采样音频数据
        resampled_audio = signal.resample(
            audio, int(len(audio) * 16000 / 44100))

        resampled_audio = np.round(resampled_audio).astype(np.int16)

        return resampled_audio

    def run(self):
        self.reset()
        try:
            print("请唤醒...KEYWORD:"+KEYWORD)
            while True:
                keyword_index = porcupine.process(self.get_next_audio_frame())
                if keyword_index >= 0:
                    # Insert detection event callback here
                    print('Keyword Detected')

                    self._audio_stream.stop_stream()
                    self._audio_stream.close()

                    AAgent.play(current_path+"/audio/hi.wav")
                    self.ask()
                    break
        except Exception as e:
            print("发生异常：", e)
            raise e

    def reset(self):
        self._audio_stream = pa.open(
            rate=sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=0,  # 一定要指定好输入设备,
            frames_per_buffer=input_frame_length)

    def ask(self):
        print("请提问...")
        AAgent.record(self._audio_input_path)
        text = BAgent.asr(self._audio_input_path)

        print("ask chatglm: " + text)
        text, self._history, temp = CAgent.ask(text, self._history)
        if text != None and text != "":
            print("answer me: " + text)

            # BAgent.tts(text, self._audio_output_path)
            # AAgent.play(self._audio_output_path)
            PAgent.tts(text)

    @classmethod
    def show_audio_devices(cls):
        devices = PvRecorder.get_audio_devices()

        for i in range(len(devices)):
            print('index: %d, device name: %s' % (i, devices[i]))
