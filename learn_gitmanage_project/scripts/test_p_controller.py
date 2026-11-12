from embodied_learning import PControllers
controller = PControllers(kp=2.0)

output = controller.calculate(
    target=5.0,
    current=2.0
)

print("控制量：", output)