#!/usr/bin/env python3

# Inspired by https://github.com/zeyus/Python3BlueBox

import array
import math
import time
import os
import sys

user_freq = [697.0, 770.0, 852.0, 941.0,
             1209.0, 1336.0, 1477.0, 1633.0]
user_tones = {
    '1': (user_freq[0], user_freq[4]),
    '2': (user_freq[0], user_freq[5]),
    '3': (user_freq[0], user_freq[6]),
    'A': (user_freq[0], user_freq[7]),
    '4': (user_freq[1], user_freq[4]),
    '5': (user_freq[1], user_freq[5]),
    '6': (user_freq[1], user_freq[6]),
    'B': (user_freq[1], user_freq[7]),
    '7': (user_freq[2], user_freq[4]),
    '8': (user_freq[2], user_freq[5]),
    '9': (user_freq[2], user_freq[6]),
    'C': (user_freq[2], user_freq[7]),
    '*': (user_freq[3], user_freq[4]),
    '0': (user_freq[3], user_freq[5]),
    '#': (user_freq[3], user_freq[6]),
    'D': (user_freq[3], user_freq[7]),
}
op_freq = [700.0, 900.0, 1100.0, 1300.0, 1300.0, 1500.0, 1700.0]

op_tones = {
    '1': (op_freq[0], op_freq[1]),
    '2': (op_freq[0], op_freq[2]),
    '3': (op_freq[1], op_freq[2]),
    '4': (op_freq[0], op_freq[3]),
    '5': (op_freq[1], op_freq[3]),
    '6': (op_freq[2], op_freq[3]),
    '7': (op_freq[0], op_freq[4]),
    '8': (op_freq[1], op_freq[4]),
    '9': (op_freq[2], op_freq[4]),
    '0': (op_freq[3], op_freq[4]),  # 0 or "10"
    'A': (op_freq[3], op_freq[4]),  # 0 or "10"
    'B': (op_freq[0], op_freq[5]),  # 11 or ST3
    'C': (op_freq[1], op_freq[5]),  # 12 or ST2
    'D': (op_freq[2], op_freq[5]),  # KP
    'E': (op_freq[3], op_freq[5]),  # KP2
    'F': (op_freq[4], op_freq[5]),  # ST
}

sr = 24000 #sample rate in Hz
dur = 0.1 #tone duration in seconds
length = int(sr * dur)
volume = .25

tone_set = user_tones

stream = open('./.dtmf.pcm', 'wb')

if len(sys.argv) != 3 :
    print('usage: {} <tone_commands> <out.mp3>'.format(str(sys.argv[0])))
    quit()

commands = str(sys.argv[1])

for command in commands :
    if command == ' ' :
        stream.write(array.array('f', [0] * length).tostring())
        continue
    try:
        tone = tone_set[command]
    except KeyError:
        print('Invalid sequence: \'{}\'. Ignoring'.format(command))
        continue
    stream.write(array.array('f',
                                (
                                    (
                                        volume * math.sin(2.0 * math.pi * i * tone[0] / float(sr)) + 
                                        volume * math.sin(2.0 * math.pi * i * tone[1] / float(sr))
                                    ) for i in range(length)
                                )
                            ).tostring()
                )

stream.close()
os.system('ffmpeg -f f32le -ar 24000 -ac 1 -i ./.dtmf.pcm -ac 2 -codec:a libmp3lame -b:a 48k -ar 24000 -write_xing 0 -y {}'.format(str(sys.argv[2])))