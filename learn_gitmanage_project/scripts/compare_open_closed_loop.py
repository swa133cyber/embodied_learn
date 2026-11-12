from embodied_learning import PControllers


# =========================
# 实验参数
# =========================

kp = 4.0
dt = 0.05
max_speed = 4.0
tolerance = 0.02
max_steps = 200


# =========================
# 闭环控制
# 每一步读取当前位置，重新计算动作
# =========================

def run_closed_loop(start,target):
    controller = PControllers(kp)
    actions=[]
    position=start
    
    for i in range(max_steps):
    
        output = controller.calculate(target,position)
        action = max(-max_speed, min(output, max_speed))
        position += action*dt
        actions.append(action)
        if abs(target - position) < tolerance:
            break
    return actions, position
    

# =========================
# 开环控制
# 只执行记录好的动作，不读取状态
# =========================

def replay_actions(start, actions):

    position = start

    for action in actions:
        position += action * dt

    return position


# =========================
# A：原始闭环实验
# =========================

actions, original_position = run_closed_loop(0.0, 5.0)

print("A. 原始闭环最终位置：", round(original_position, 4))
print("记录的动作数量：", len(actions))


# =========================
# B：相同起点开环回放
# =========================

same_position = replay_actions(0.0, actions)

print("B. 相同起点开环回放：", round(same_position, 4))


# =========================
# C：改变起点，开环回放
# =========================

changed_position = replay_actions(1.0, actions)

print("C. 改变起点后开环回放：", round(changed_position, 4))


# =========================
# D：改变起点，重新闭环控制
# =========================

actions, feedback_position = run_closed_loop(1.0, 5.0)


print("D. 改变起点后闭环控制：", round(feedback_position, 4))
print("E.改变起点后的闭环控制步数：",len(actions))
    