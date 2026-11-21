"""
import random
import math
def seed_reset(seed,target):
    rng = random.Random(seed)
    start = rng.uniform(0.0,target)
    return start

def step(action,position):
    impact = random.uniform(-0.2,0.2)
    position += action + impact
    return position

def end_judge(target,position):
    if abs(target - position) < 0.1:
        judge = True
    else:
        judge = False
    return judge
"""
# test_module.py

import random


def seed_reset(seed, target):
    """根据随机种子生成可复现的初始位置。"""
    rng = random.Random(seed)
    start = rng.uniform(0.0, target)

    return start


def step(action, position, disturbance=0.0):
    """执行动作并叠加环境随机扰动。"""
    new_position = position + action + disturbance

    return new_position


def end_judge(target, position):
    """判断当前位置是否进入目标范围。"""
    return abs(target - position) < 0.1

