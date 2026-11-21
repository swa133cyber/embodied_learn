# strategy_module.py

# 开环策略使用的预设动作序列
REFERENCE_ACTION_SEQUENCE = tuple(
    1.0 * (0.8 ** i) for i in range(25)
)


def open_loop_strategy(step_index, action_sequence):
    """根据当前步数返回预设动作。"""

    if step_index >= len(action_sequence):
        return 0.0

    return action_sequence[step_index]


def closed_loop_strategy(position, target, kp):
    """根据当前位置和目标位置计算动作。"""

    error = target - position
    action = kp * error

    return action