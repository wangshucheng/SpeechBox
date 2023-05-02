import wave
import pyaudio

# 打开wav文件
with wave.open('audio.wav', 'rb') as wf:
    # 初始化音频输出设备
    p = pyaudio.PyAudio()
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
