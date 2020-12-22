# color layer (second layer)
import xml.etree.ElementTree as Tree
from svg.path import parse_path, Line, CubicBezier
import sympy


def get_color_data(svg_path, img):
    xml = Tree.parse(svg_path)
    svg = xml.getroot()
    # color_positions = []
    colors = []
    width = img.shape[1]
    height = img.shape[0]
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
                    # color_positions.append([s1x, s1y])
                    colors.append(img[s1y, s1x])
                if -1 < s2x < width and -1 < s2y < height:
                    # color_positions.append([s2x, s2y])
                    colors.append(img[s2y, s2x])
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
                        colors.append(img[y, x])  # <2>
                else:
                    if 0 <= a[0][0] <= 1:
                        x, y = get_bezier_sample(a[0][0], p0, p1, p2, p3)
                        # if color_positions.count([x, y]) == 0:
                        #     color_positions.append([x, y])  # <1>
                        if -1 < x < width and -1 < y < height:
                            colors.append(img[y, x])  # <2>
                    if 0 <= a[1][0] <= 1:  # here use "if" but not "elif" means that both situation can happen. so <1>
                        x, y = get_bezier_sample(a[1][0], p0, p1, p2, p3)  # and <2> should be write twice.
                        # if color_positions.count([x, y]) == 0:
                        #     color_positions.append([x, y])  # <1>
                        if -1 < x < width and -1 < y < height:
                            colors.append(img[y, x])  # <2>
    # print(len(color_positions))  # 该长度过大，几乎是原图像素数量一半
    # 另，二维数组不能list(set(LIST))来去重
    return colors


def bezier(t, p0, p1, p2, p3):
    return p0 * (1 - t) ** 3 + 3 * p1 * t * (1 - t) ** 2 + 3 * p2 * t * t * (1 - t) + p3 * t ** 3


def bezier_tangent(t, p0, p1, p2, p3):
    return -3 * p0 * (1 - t) ** 2 \
           + 3 * p1 * ((1 - t) ** 2 - 2 * t * (1 - t)) \
           + 3 * p2 * (2 * t * (1 - t) - t ** 2) \
           + 3 * p3 * t ** 2


def get_bezier_sample(c_t, p0, p1, p2, p3):
    x0 = bezier(c_t, p0[0], p1[0], p2[0], p3[0])
    y0 = bezier(c_t, p0[1], p1[1], p2[1], p3[1])
    # 注意切线与x轴垂直斜率不存在的情况
    if p3[0] - p0[0] != 0:
        delta_x = p3[0] - p0[0]
        delta_y = p3[1] - p0[1]
        k = delta_y / delta_x
        # 此时切线函数 y = (delta_y / delta_x)(x-x0)+y0
        if k == 0:
            s1x, s1y, s2x, s2y = calc_sample(x0, y0, 4)
        elif -1 <= k < 0 or 0 < k <= 1:
            s1x, s1y, s2x, s2y = calc_sample(x0, y0, delta_y)
        else:
            s1x, s1y, s2x, s2y = calc_sample(x0, y0, delta_x, 1)
            # svg y轴方向向下， 切线b<0->则采样在切线下方-切线下方的y更大
            # 理论上不存在=的情况
        if y0 - (delta_y / delta_x) * x0 < p0[1] - (delta_y / delta_x) * p0[0]:
            if s1x > s2x or s1y > s2y:
                return s1x, s1y
            else:
                return s2x, s2y
        else:
            if s1x > s2x or s1y > s2y:
                return s2x, s2y
            else:
                return s1x, s1y
    else:
        s1x, s1y, s2x, s2y = calc_sample(x0, y0, 8, 1)  # delta取8，s1x > s2x
        if x0 > p0[0]:
            return s2x, s2y
        else:
            return s1x, s1y


def calc_sample(mid_x, mid_y, delta, flag=0):
    """
    :param mid_x: 中点横坐标
    :param mid_y: 中点纵坐标
    :param delta: 起点终点横坐标差或纵坐标差，flag=0取纵差1取横差
    :param flag: 0为水平，1为垂直
    :return: 采样点1横坐标或纵坐标大于mid 采样点2横坐标或纵坐标小于mid round()后的结果
    """
    if flag == 0:
        sample1_x = round(mid_x)
        sample2_x = round(mid_x)
        sample1_y = round(mid_y + 1 / 4 * delta)
        sample2_y = round(mid_y - 1 / 4 * delta)
    else:
        sample1_x = round(mid_x + 1 / 4 * delta)
        sample2_x = round(mid_x - 1 / 4 * delta)
        sample1_y = round(mid_y)
        sample2_y = round(mid_y)
    return sample1_x, sample1_y, sample2_x, sample2_y