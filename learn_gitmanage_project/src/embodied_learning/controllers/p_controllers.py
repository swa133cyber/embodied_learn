class PControllers:
    def __init__(self, kp):
        # 比例系数，决定控制器对误差的响应强度
        self.kp = kp
        
    def calculate(self, target, current):
        # 计算位置误差
        error = target - current

        # P 控制公式：控制量 = Kp × 误差
        output = self.kp * error

        return output

