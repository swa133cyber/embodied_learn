import matplotlib.pyplot as plt

from embodied_learning import PControllers

kp = 2.0
target = 5.0
position = 0.0
dt = 0.05
max_steps = 300
max_speed = 4.0

controller = PControllers(kp=kp)

steps = []       # 记录步数
distances = []

for step in range(max_steps):

    error = target - position
    output = controller.calculate(
            target=target,
            current=position
                            )


    velocity = max(
            -max_speed,
            min(output, max_speed)
                  )

    position += velocity * dt
    distance = abs(target - position) 
    steps.append(step + 1)
    distances.append(distance)
    
    print(
            f"Step: {step + 1:3d} | "
            f"Position: {position:.4f} | "
            f"Velocity: {velocity:.4f} | "
            f"Error: {error:.4f}"
        )

    if abs(error) < 0.02:
            print("到达目标！")
            break
        
        # 绘制距离变化曲线
plt.plot(steps, distances)

# 设置横轴和纵轴名称
plt.xlabel("Steps")
plt.ylabel("Distance")

# 设置图表标题
plt.title("P Controller Distance Curve")

# 显示网格
plt.grid(True)

# 显示图像
plt.show()

