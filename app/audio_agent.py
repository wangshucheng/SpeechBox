import wave
import pyaudio
from scipy import signal
from scipy.io import wavfile
import speech_recognition as sr


def play(file_path):
    # 初始化音频输出设备
    p = pyaudio.PyAudio()

    print("start play audio")
    # 打开wav文件
    with wave.open(file_path, 'rb') as wf:

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # 播放音频
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        # 关闭音频输出设备
        stream.stop_stream()
        stream.close()
        p.terminate()

# 重采样


def resample(file_path, fs_new=16000):
    # 读取原始WAV文件,原始信号为x，采样率为fs
    fs, x = wavfile.read(file_path)

    # 将原始信号重采样为新的采样率fs_new
    x_resampled = signal.resample(x, int(len(x) * fs_new / fs))

    # 将重采样后的信号保存为WAV文件
    wavfile.write(file_path, fs_new, x_resampled)


# 1. speech_recognition 2. PvRecorder
# 创建Recognizer对象
r = sr.Recognizer()
drive_sample_rate = 44100


def record(file_path, sample_rate=16000):
    try:
        # 使用采样率为44100的麦克风录音
        with sr.Microphone(0, drive_sample_rate) as source:
            # with sr.Microphone() as source:
            print("start record audio")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        print("end record audio")
        # 将录音保存为WAV文件
        with open(file_path, "wb") as f:
            f.write(audio.get_wav_data())

        if drive_sample_rate != sample_rate:
            resample(file_path)

    except Exception as e:
        print("发生异常：", e)
        raise e
