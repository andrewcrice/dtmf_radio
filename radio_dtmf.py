#!/usr/bin/env python3

import os

#make commands
tones = [('1','radio_on'),
         ('2','radio_off'),
         ('3','tune_to_freq'),
         ('4','save_this_as_preset'),
         ('5','tune_to_preset')
        ]

command_prefix = 'DBCA '

for seq, fname in tones :
    os.system('./dtmf.py \'' + command_prefix + seq + '\' ./commands/' + fname + '.mp3')

#make frequencies
for freq in range(879, 1079, 2) :
    os.system('./dtmf.py \'' + '{:04d}'.format(freq) + '\' ./commands/freq' + '{:04d}'.format(freq) + '.mp3')