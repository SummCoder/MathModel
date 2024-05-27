import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 车辆参数
L_f = 1.2
L_r = 1.2
V = 5.56  # 车辆速度，单位：米/秒
delta = np.deg2rad(30)  # 前轮偏转角，单位：弧度
car_length = 4.0  # 车身长度 m
car_width = 2.0  # 车身宽度 m
wheel_diameter = 0.6  # 车轮直径 m
wheel_width = 0.16  # 车轮宽度 m
front_offset = 0.5  # 前轮到车头距离 m
rear_offset = 0.5  # 后轮到车尾距离 m
# 轮子相对于车辆中心的横向和纵向偏移量
front_wheel_offset = car_length / 2 - front_offset - wheel_diameter / 2
rear_wheel_offset = -car_length / 2 + rear_offset / 2 + wheel_diameter / 2
side_wheel_offset = car_width / 2 - wheel_width / 2

len_center = math.sqrt(front_wheel_offset * front_wheel_offset + side_wheel_offset * side_wheel_offset)

theta_rad = np.arctan(side_wheel_offset / front_wheel_offset)

# 运动参数
dt = 0.1  # 时间间隔，单位：秒
total_time = 2  # 总仿真时间，单位：秒
steps = int(total_time / dt)  # 总步数

# 初始化车辆状态
x = 0  # 车辆x坐标，单位：米
y = 0  # 车辆y坐标，单位：米
psi = np.deg2rad(90)  # 车辆航向角，单位：弧度，车头方向为y轴
beta = np.arctan((L_r / (L_r + L_f)) * np.tan(delta))

# 车辆运动轨迹
x_traj = []
y_traj = []
x_front_in_traj = []
y_front_in_traj = []
x_front_out_traj = []
y_front_out_traj = []
x_rear_in_traj = []
y_rear_in_traj = []
x_rear_out_traj = []
y_rear_out_traj = []

# 初始化位置数据列表，包含车辆中心及四个轮子的位置
data = []

for step in range(steps):
    # 车辆中心位置
    x_center = x
    y_center = y

    # 各轮子位置计算
    x_front_in = x_center + np.cos(theta_rad + psi) * len_center
    y_front_in = y_center + np.sin(theta_rad + psi) * len_center

    x_front_out = x_center + np.cos(theta_rad - psi) * len_center
    y_front_out = y_center - np.sin(theta_rad - psi) * len_center

    x_rear_in = x_center - np.cos(theta_rad - psi) * len_center
    y_rear_in = y_center + np.sin(theta_rad - psi) * len_center

    x_rear_out = x_center - np.cos(theta_rad + psi) * len_center
    y_rear_out = y_center - np.sin(theta_rad + psi) * len_center

    # 收集当前时间步的数据
    data.append([step * dt,
                 x_center, y_center,
                 x_front_in, y_front_in,
                 x_front_out, y_front_out,
                 x_rear_in, y_rear_in,
                 x_rear_out, y_rear_out])

    x_traj.append(x)
    y_traj.append(y)

    x_front_in_traj.append(x_front_in)
    y_front_in_traj.append(y_front_in)
    x_front_out_traj.append(x_front_out)
    y_front_out_traj.append(y_front_out)
    x_rear_in_traj.append(x_rear_in)
    y_rear_in_traj.append(y_rear_in)
    x_rear_out_traj.append(x_rear_out)
    y_rear_out_traj.append(y_rear_out)

    # 更新x、y坐标以及与x轴夹角
    x += V * np.cos(psi + beta) * dt
    y += V * np.sin(psi + beta) * dt
    psi += (V / L_r) * np.sin(beta) * dt

# 绘制车辆轨迹
plt.figure(figsize=(8, 6))
plt.plot(x_traj, y_traj, label='车辆轨迹', color='b')
plt.plot(x_front_in_traj, y_front_in_traj, label='前内车轮轨迹', color='y')
plt.plot(x_front_out_traj, y_front_out_traj, label='前外车轮轨迹', color='r')
plt.plot(x_rear_in_traj, y_rear_in_traj, label='后内车轮轨迹', color='g')
plt.plot(x_rear_out_traj, y_rear_out_traj, label='后外车轮轨迹', color='maroon')
plt.scatter(x_traj[0], y_traj[0], color='r', marker='o', label='起点')
plt.scatter(x_traj[-1], y_traj[-1], color='g', marker='o', label='终点')
plt.axis('equal')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('前轮驱动单车运动模型仿真')
plt.legend()
plt.show()

# 构建DataFrame
columns = ['时间/s',
           '车辆中心_x', '车辆中心_y',
           '前内轮中心_x', '前内轮中心_y',
           '前外轮中心_x', '前外轮中心_y',
           '后内轮中心_x', '后内轮中心_y',
           '后外轮中心_x', '后外轮中心_y']
df_positions = pd.DataFrame(data, columns=columns)

# 打印DataFrame
print(df_positions)

# 保存到Excel文件
df_positions.to_excel('result2.xlsx', index=False)