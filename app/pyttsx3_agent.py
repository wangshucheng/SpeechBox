# ubuntu完美安装espeak支持中文和粤语 不再报错:Full dictionary is not installed for 'zh'
# https://blog.csdn.net/qq_24406903/article/details/89811732

import pyttsx3

engine = pyttsx3.init()

# 获取语音包
# voices = engine.getProperty('voices')
# for voice in voices:
#     print('id = {}\tname = {} \n'.format(voice.id, voice.name))
# 设置使用的语音包
engine.setProperty('voice', 'zh')  # 开启支持中文
# engine.setProperty('voice', voices[0].id)

# 改变语速  范围为0-200   默认值为200
rate = engine.getProperty('rate')  # 获取当前语速
engine.setProperty('rate', rate)

# 设置音量  范围为0.0-1.0  默认值为1.0
engine.setProperty('volume', 0.7)


def tts(prompt):
    # 预设要朗读的文本数据
    engine.say(prompt)
    # 朗读
    engine.runAndWait()

# tts("开始播放")
