# 导入所需的模块和库
import argparse
import os
import time
from speech_box import SpeechBox

# 主程序代码


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser()

    parser.add_argument('--audio_device_index',
                        help='Index of input audio device.', type=int, default=-1)

    parser.add_argument(
        '--output_path', help='Absolute path to recorded audio for debugging.', default=None)

    parser.add_argument('--show_audio_devices', action='store_true')

    args = parser.parse_args()

    if args.show_audio_devices:
        SpeechBox.show_audio_devices()
    else:
        # sb = SpeechBox("input.wav", "output.wav")
        while True:
            # sb.run()
            SpeechBox("input.wav", "output.wav").run()
            # time.sleep(0.1)


# 包装主程序代码
if __name__ == "__main__":
    main()
