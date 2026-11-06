
import gymnasium as gym

# 创建 CartPole 环境，打开图形显示窗口
env = gym.make("CartPole-v1", render_mode="human")

# 初始化环境，获取初始状态
observation, info = env.reset()

# 统计累计奖励和坚持步数
total_reward = 0
steps = 0

try:
    while True:
        # 读取当前状态
        # observation[2]：杆子的倾斜角，单位为弧度
        # observation[3]：杆子的角速度，单位为弧度/秒
        angle = observation[2]
        angular_velocity = observation[3]

        # 将倾斜角和角速度结合起来
        # 0.5 是人为设置的权重，用来调整角速度的影响
        control_value = angle + 0.5 * angular_velocity

        # 打印当前状态和控制器的计算结果
        print(
            f"第 {steps + 1:3d} 步 | "
            f"角度：{angle: .3f} rad | "
            f"角速度：{angular_velocity: .3f} rad/s | "
            f"控制值：{control_value: .3f}"
        )

        # 根据控制值选择动作
        # action = 0：向左推小车
        # action = 1：向右推小车
        if control_value > 0:
            action = 1
        else:
            action = 0

        # 执行动作，获得下一时刻的状态
        observation, reward, terminated, truncated, info = env.step(action)

        # 更新累计奖励和步数
        total_reward += reward
        steps += 1

        # 判断本轮实验是否结束
        if terminated or truncated:
            break

    # 输出本轮实验结果
    print("\n本轮实验结束")
    print("坚持步数：", steps)
    print("累计奖励：", total_reward)

finally:
    # 无论程序正常结束还是中途退出，都关闭环境
    env.close()
