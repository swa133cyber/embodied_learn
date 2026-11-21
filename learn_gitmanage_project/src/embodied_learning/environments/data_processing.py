"""
import matplotlib.pyplot as plt
def data_record(positions,actions,position,action):
    positions.append(position)
    actions.append(action)
    return positions,actions

def data_handle(end_position,steps,positions):
    final_err = end_position - 5
    print(f"本次产生误差为{final_err:.4f}")
    plt.plot(steps,positions,marker='o')
    plt.xlabel("step")
    plt.ylabel("position")
    plt.title('单步位置折线图')
    plt.grid(True)
    plt.show()
    return final_err
"""

import csv
from pathlib import Path


def save_episode_results(results, file_path):
    """将每回合实验结果保存为 CSV。"""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not results:
        return

    fieldnames = list(results[0].keys())

    with file_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"实验结果已保存：{file_path}")


def print_summary(results):
    """统计两种策略的实验结果。"""
    strategies = sorted(set(row["strategy"] for row in results))

    for strategy in strategies:
        group = [
            row for row in results
            if row["strategy"] == strategy
        ]

        total = len(group)
        successes = sum(row["final_success"] for row in group)
        reached = sum(row["ever_reached"] for row in group)

        print(f"\n策略：{strategy}")
        print(f"最终成功：{successes}/{total}")
        print(f"最终成功率：{successes / total:.2%}")
        print(f"曾进入目标范围：{reached}/{total}")