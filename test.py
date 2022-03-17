#!/usr/bin/python3
# -*- coding: UTF-8 -*-

'''
7955.135064
f0cde10c18090000 9998899990000
0300000000000000 3
68e129da01000000 7955145064
0000000000000000 0
0000000000000000 0
0000000000000000 0

21213.710170
f04cfc3400000000 888950000
0200000000000000 2
9aeb1b3c01000000 5303430042
4b04000000000000 1099
0600000000000000 6
d0c253b403000000 15910290128

他有推广关系
21213720170 = 5303430042 + 15910290128

2651.705021
c09a930c00000000 211000000
0100000000000000 1 
cdf50d9e00000000 2651715021
0000000000000000 0
0000000000000000 0
0000000000000000 0


reward.nAmount          持币金额
reward.nRank            持币排名
reward.nStakeReward     持币收益
reward.nAchievement     下级金额之和
reward.nPower           
reward.nPromotionReward 推广收益

总收益等于= nStakeReward(持币收益) + nPromotionReward(推广收益)
'''

import struct
def DefiReward(data):
    buf = bytearray.fromhex(data)
    amount, = struct.unpack('<q',buf[:8])
    rank, = struct.unpack('<q',buf[8:16])
    stake_reward, = struct.unpack('<q',buf[16:24])
    achievement, = struct.unpack('<q',buf[24:32])
    power, = struct.unpack('<q',buf[32:40])
    promotion_reward, = struct.unpack('<q',buf[40:48])
    return amount,rank,stake_reward,achievement,power,promotion_reward

data = 'f04cfc340000000002000000000000009aeb1b3c010000004b040000000000000600000000000000d0c253b403000000'
print(DefiReward(data))
#print(ret)
#print(5303430042 + 15910290128)