# 參閱16-42頁

import math

def calc_angle(s, e, w): # 接收肩、肘、腕的座標
    se = (s[0] - e[0], s[1] - e[1]) # 座標點轉換成向量（肩→肘
    we = (w[0] - e[0], w[1] - e[1]) # 『腕/肘』向量
    dot_product = se[0] * we[0] + se[1] * we[1] # 計算向量的點積
    mag1 = math.sqrt(se[0]**2 + se[1]**2) # 肩→肘的向量長度
    mag2 = math.sqrt(we[0]**2 + we[1]**2) # 腕→肘的向量長度

    if mag1 * mag2 == 0: return 180
    
    angle_rad = math.acos(dot_product / (mag1 * mag2))  # 夾角的弧度
    angle_deg = math.degrees(angle_rad)                 # 弧度轉角度
    return angle_deg
   
shoulder = [2, 2] # 肩膀的座標
elbow = [4, 6]    # 手肘的座標
wrist = [7, 7]    # 手腕的座標

angle = calc_angle(shoulder, elbow, wrist)
print(f'手臂彎曲的角度：{angle:.2f}度')