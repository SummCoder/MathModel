import random
import math
import numpy as np
import matplotlib.pyplot as plt

# 车辆参数
vehicle_length = 4.0  # 车辆长度（m）
vehicle_width = 2.0  # 车辆宽度（m）
wheel_diameter = 0.6  # 车轮直径（m）
wheel_width = 0.16  # 车轮宽度（m）
front_rear_distance = 0.5  # 前后轮到车头车尾的距离（m）
L = 2.4

# 车位参数
parking_space_length = 5.3  # 停车位长度（m）
parking_space_width = 2.4  # 停车位宽度（m）
road_width = 5.5  # 道路宽度（m）

# 蒙特卡罗模拟参数
num_samples = 1000000  # 采样次数

# 初始化最大和最小转弯角度
max_turn_angle = 0
min_turn_angle = 50

# 初始化最大和最小转弯开始位置
max_start_turn_position = parking_space_length
min_start_turn_position = 0.0

# 蒙特卡罗模拟
for _ in range(num_samples):
    # 随机生成一个车辆开始转弯的位置
    start_position = random.uniform(0, parking_space_length)

    # 随机车辆在转弯过程中的最大和最小转弯角度
    max_angle = random.uniform(0, 40)
    min_angle = random.uniform(0, 40)

    # 更新最大和最小转弯角度
    if max_angle > max_turn_angle:
        R = L / math.tan(np.deg2rad(max_angle))
        R_in = R - 0.92
        if R_in * R_in - (R_in - 0.2) * (R_in - 0.2) >= (3.85 - start_position) * (3.85 - start_position):
            max_turn_angle = max(max_turn_angle, max_angle)

    if min_angle < min_turn_angle:
        R = L / math.tan(np.deg2rad(min_angle))
        R_out = math.sqrt((R + 0.92) * (R + 0.92) + 2.4 * 2.4)
        if start_position + R_out <= 5.5 + 3.85:
            min_turn_angle = min(min_turn_angle, min_angle)

# 使用蒙特卡罗统计开始转弯位置
for _ in range(num_samples):
    # 随机生成一个车辆开始转弯的位置
    start_position = random.uniform(0, parking_space_length)
    # 更新最大转弯开始位置
    R = L / math.tan(np.deg2rad(max_turn_angle))
    R_in = R - 0.92
    if R_in * R_in - (R_in - 0.2) * (R_in - 0.2) >= (3.85 - start_position) * (3.85 - start_position):
        max_start_turn_position = min(max_start_turn_position, start_position)

# 再次使用蒙特卡罗统计开始转弯位置
for _ in range(num_samples):
    # 随机生成一个车辆开始转弯的位置
    start_position = random.uniform(0, parking_space_length)
    # 更新最大转弯开始位置
    R = L / math.tan(np.deg2rad(min_turn_angle))
    R_out = math.sqrt((R + 0.92) * (R + 0.92) + 2.4 * 2.4)
    if start_position + R_out <= 5.5 + 3.85:
        min_start_turn_position = max(min_start_turn_position, start_position)

# 打印结果
print("前内轮最大转弯角度（角度）：", max_turn_angle)
print("前内轮最小转弯角度（角度）：", min_turn_angle)
print("最大转弯开始位置距离出库线（m）：", 3.85 - max_start_turn_position)
print("最小转弯开始位置距离起点（m）：", min_start_turn_position)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 创建一个新的图形
plt.figure()

# 定义数据
data = {'前内轮最大转弯角度（角度）': max_turn_angle, '前内轮最小转弯角度（角度）': min_turn_angle}
positions = list(data.keys())
values = list(data.values())

# 绘制柱状图
plt.bar(positions, values)

# 添加标签
plt.xlabel('类型')
plt.ylabel('转弯角度/度')
plt.title('最大最小转弯角度')

# 显示图形
plt.show()
