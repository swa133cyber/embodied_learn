# open_closed_loop_different_environment.py

import random
from pathlib import Path

from embodied_learning.controllers.strategy_module import (
    open_loop_strategy,
    closed_loop_strategy,
    REFERENCE_ACTION_SEQUENCE,
)

from embodied_learning.environments.test_module import (
    seed_reset,
    step,
    end_judge,
)

from embodied_learning.environments.data_processing import (
    save_episode_results,
    print_summary,
)


# =========================
# 实验参数
# =========================

TARGET = 5.0
KP = 0.2

MAX_ACTION = 1.0
MAX_STEPS = 25

TEST_SEEDS = list(range(10))

DISTURBANCE_RANGE = (-0.05, 0.05)

OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "outputs"
    / "day05_strategy_comparison.csv"
)


def clip_action(action):
    """限制动作范围，避免动作过大。"""
    return max(-MAX_ACTION, min(MAX_ACTION, action))


def run_episode(strategy_name, seed):
    """使用指定策略和种子运行一个测试回合。"""

    # 相同种子生成相同初始位置
    position = seed_reset(seed, TARGET)

    # 独立生成该回合的随机扰动序列
    # 两种策略使用相同 seed 时，会得到相同扰动
    noise_rng = random.Random(seed + 10000)

    disturbances = [
        noise_rng.uniform(*DISTURBANCE_RANGE)
        for _ in range(MAX_STEPS)
    ]

    ever_reached = False
    first_reached_step = None

    for step_index in range(MAX_STEPS):

        # 1. 根据策略计算动作
        if strategy_name == "open_loop":
            action = open_loop_strategy(
                step_index,
                REFERENCE_ACTION_SEQUENCE,
            )

        elif strategy_name == "closed_loop":
            action = closed_loop_strategy(
                position,
                TARGET,
                KP,
            )

        else:
            raise ValueError(f"未知策略：{strategy_name}")

        # 2. 限制动作范围
        action = clip_action(action)

        # 3. 获取当前步对应的固定扰动
        disturbance = disturbances[step_index]

        # 4. 执行环境更新
        position = step(
            action,
            position,
            disturbance,
        )

        # 5. 判断是否曾经进入目标范围
        if end_judge(TARGET, position):
            if not ever_reached:
                ever_reached = True
                first_reached_step = step_index + 1

    # 注意：为了判断最终是否仍停留在目标范围，
    # 本实验会完整执行 MAX_STEPS 步，而不是首次到达就结束。

    final_distance = abs(TARGET - position)
    final_success = end_judge(TARGET, position)

    return {
        "strategy": strategy_name,
        "seed": seed,
        "initial_position": round(
            seed_reset(seed, TARGET), 6
        ),
        "target": TARGET,
        "ever_reached": ever_reached,
        "first_reached_step": first_reached_step,
        "final_position": round(position, 6),
        "final_distance": round(final_distance, 6),
        "final_success": final_success,
        "steps_executed": MAX_STEPS,
    }


def main():

    results = []

    strategies = [
        "open_loop",
        "closed_loop",
    ]

    # 依次测试两种策略
    for strategy_name in strategies:

        print(f"\n开始测试策略：{strategy_name}")

        for seed in TEST_SEEDS:

            result = run_episode(strategy_name, seed)
            results.append(result)

            print(
                f"Seed: {seed:2d} | "
                f"初始位置: {result['initial_position']:.3f} | "
                f"最终距离: {result['final_distance']:.3f} | "
                f"曾进入目标范围: {result['ever_reached']} | "
                f"最终成功: {result['final_success']}"
            )

    # 保存 CSV
    save_episode_results(results, OUTPUT_PATH)

    # 打印统计结果
    print_summary(results)


if __name__ == "__main__":
    main()