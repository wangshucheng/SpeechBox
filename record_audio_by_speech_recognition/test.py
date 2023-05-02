import speech_recognition as sr

# 创建Recognizer对象
r = sr.Recognizer()

names = sr.Microphone.list_microphone_names()
for i in range(len(names)):
    print('index: %d, device name: %s' % (i, names[i]))

try:
    # 使用采样率为44100的麦克风录音
    with sr.Microphone(0, 44100) as source:
        print("请说话...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # 将录音保存为WAV文件
    with open("audio2.wav", "wb") as f:
        f.write(audio.get_wav_data())
except Exception as e:
    print("发生异常：", e)