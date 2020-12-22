# three channel image C
from svg.path import parse_path, Line, CubicBezier
import xml.etree.ElementTree as Tree
import sympy
from edge_detection.color_layer import calc_sample, bezier_tangent, get_bezier_sample
import numpy as np


def generate_color_mask(svg_path, c_data):
    xml = Tree.parse(svg_path)
    svg = xml.getroot()
    width = int(svg.attrib['width'])
    height = int(svg.attrib['height'])
    m_bg = np.zeros((height, width, 1), np.uint8)
    c_bg = np.zeros((height, width, 3), np.uint8)
    for path in svg:
        ps = parse_path(path.attrib['d'])
        # p_style = path.attrib['style']
        # if '#ffffff' in p_style:
        #     continue
        for p in ps:
            if type(p) == Line:  # 可能有QuadraticBezier
                delta_y = p.end.imag - p.start.imag  # 实部和虚部，即x和y的值
                delta_x = p.end.real - p.start.real
                mid_x = (p.start.real + p.end.real) / 2
                mid_y = (p.start.imag + p.end.imag) / 2
                if p.start.real != p.end.real:
                    k = delta_y / delta_x
                    if k == 0:
                        s1x, s1y, s2x, s2y = calc_sample(mid_x, mid_y, 4)
                    elif -1 <= k < 0 or 0 < k <= 1:  # 视作水平，垂直采样 该坐标轴y方向向下，但-1和1的取值不影响
                        s1x, s1y, s2x, s2y = calc_sample(mid_x, mid_y, delta_y)
                    else:
                        s1x, s1y, s2x, s2y = calc_sample(mid_x, mid_y, delta_x, 1)
                else:  # line与x轴垂直
                    s1x, s1y, s2x, s2y = calc_sample(mid_x, mid_y, 4, 1)  # delta_x为0，为了采样给一个差
                if -1 < s1x < width and -1 < s1y < height:
                    m_bg[s1y][s1x][0] = 255
                    c_bg[s1y][s1x] = c_data.pop(0)
                if -1 < s2x < width and -1 < s2y < height:
                    m_bg[s2y][s2x][0] = 255
                    c_bg[s2y][s2x] = c_data.pop(0)
                # black_bg[s1y-1][s1x-1][0] = 255
                # black_bg[s2y-1][s2x-1][0] = 255
            elif type(p) == CubicBezier:
                # 初步思路-以初始点和终止点的的连线作为直线对曲线切割，交点为1时即为切线
                # 一般的cb曲线 - 记p0,p1,p2,p3为初始、控制1、控制2、终止
                p0 = [p.start.real, p.start.imag]
                p1 = [p.control1.real, p.control1.imag]
                p2 = [p.control2.real, p.control2.imag]
                p3 = [p.end.real, p.end.imag]
                t = sympy.symbols("t")
                # 贝塞尔方程求导 导函数带入y除以导函数带入x为切线斜率
                # 注意贝塞尔曲线求导x带入为0的情况,即切线与x轴垂直斜率不存在的情况
                if p3[0] - p0[0] != 0:
                    a = sympy.solve([bezier_tangent(t, p0[1], p1[1], p2[1], p3[1])
                                     /
                                     bezier_tangent(t, p0[0], p1[0], p2[0], p3[0])
                                     -
                                     (p3[1] - p0[1]) / (p3[0] - p0[0])], [t])
                else:
                    a = sympy.solve([bezier_tangent(t, p0[0], p1[0], p2[0], p3[0])], [t])
                if type(a) == dict:
                    x, y = get_bezier_sample(a.get(t), p0, p1, p2, p3)
                    # if color_positions.count([x, y]) == 0:
                    #     color_positions.append([x, y])  # <1>
                    if -1 < x < width and -1 < y < height:
                        m_bg[y][x][0] = 255
                        c_bg[y][x] = c_data.pop(0)
                else:
                    if 0 <= a[0][0] <= 1:
                        x, y = get_bezier_sample(a[0][0], p0, p1, p2, p3)
                        # if color_positions.count([x, y]) == 0:
                        #     color_positions.append([x, y])  # <1>
                        if -1 < x < width and -1 < y < height:
                            m_bg[y][x][0] = 255
                            c_bg[y][x] = c_data.pop(0)
                    if 0 <= a[1][0] <= 1:  # here use "if" but not "elif" means that both situation can happen. so <1>
                        x, y = get_bezier_sample(a[1][0], p0, p1, p2, p3)  # and <2> should be write twice.
                        # if color_positions.count([x, y]) == 0:
                        #     color_positions.append([x, y])  # <1>
                        if -1 < x < width and -1 < y < height:
                            m_bg[y][x][0] = 255
                            c_bg[y][x] = c_data.pop(0)
    # 另，二维数组不能list(set(LIST))来去重
    return m_bg, c_bg



