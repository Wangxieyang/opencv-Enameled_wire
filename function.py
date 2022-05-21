import cv2
import numpy as np



# 列求和
def sumY(array, y):
    sumr = 0
    for i in range(len(array) - 1):
        sumr += array[i][0][y]
    return sumr


# 行求和
def sumX(array, x):
    sumr = 0
    for j in range(len(array[0])):
        sumr += array[x][j]
    return sumr


# 列表中间的元素
def median(s):
    n = len(s)  # 计算列表内元素数量
    if n == 1:  # 这个要非常注意，当元素只有一个的时候，直接取值
        return s[0]
    elif n % 2 != 0:  # 如果元素数量为奇数            #排序一下
        mid = s[(n - 1) // 2]  # 中间值等于元素总数量减一以后除以2，记得要用//
        return mid
    else:
        mid = (s[n // 2 - 1] + s[n // 2]) / 2  # 如果是偶数，取元素数量//2后减一位的那个值，以及元素数量//2的那个值，记得最后要用float，不然没有小数点
        return mid


def listsum(s):
    sum = 0
    for i in range(len(s)):
        sum += s[i]
    return sum


# 相邻元素提取函数
def neib(x, y, mat):  # 输入位置和目标数组
    max_x = mat.shape[0] - 1  # 确定行、列最大坐标
    max_y = mat.shape[1] - 1

    matr = []

    # 这里需要重点理解下，坐标不在边缘处，就从前一个遍历到后一个，否则从自身开始
    if x > 0:
        dx = -1
    else:
        dx = 0
    if x < max_x:
        X = 1
    else:
        X = 0
    if y > 0:
        dy = -1
    else:
        dy = 0
    if y < max_y:
        Y = 1
    else:
        Y = 0

    for i in range(dx, X + 1):
        for j in range(dy, Y + 1):
            # if (i == 0 or j == 0) and (i + j != 0):
            if i != 0 or j != 0:
                matr.append(mat[x + i][y + j])
    return matr


# 提取数组最小非零元素
def zxfl(a):
    c = np.asarray(a)
    img5 = c.nonzero()
    imm = c[img5].min()
    return imm


# 标注连续白色区域的像素点
def count(a):
    # 二值化处理
    global image1
    image1 = a
    image = a[:, :, 0]  # 提取BLUE通道灰度图
    ret1, imageB = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # otsu法取阈值
    global temp
    temp = np.asarray(imageB)

    X = temp.shape[0]
    Y = temp.shape[1]
    global matrix
    matrix = np.zeros((X, Y))
    matrix = matrix.astype(int)
    label = 1
    # print(matrix)
    for i in range(X):
        for j in range(Y):
            if (temp[i][j] == 255 and matrix[i][j] == 0):
                if max(neib(i, j, matrix)) == 0:
                    matrix[i][j] = label
                    label += 1
                else:
                    matrix[i][j] = zxfl(neib(i, j, matrix))
            else:
                continue

    # print(matrix)
    for i in range(X):
        for j in range(Y):
            if matrix[i][j] != 0:
                if max(neib(i, j, matrix)) != 0 and zxfl(neib(i, j, matrix)) < matrix[i][j]:
                    np.place(matrix, matrix == matrix[i][j], zxfl(neib(i, j, matrix)))

    # print(matrix)
    # np.savetxt("data.txt", matrix)

    S = matrix.max()
    matr = []
    COUNT = 0
    for i in range(S):
        if np.sum(matrix == S) > 0:
            COUNT = np.sum(matrix == S)
            matr.append(COUNT)
        S -= 1

    return matr


# 有无判断函数
def isnone(counts):
    if len(counts) == 1:
        return 1
    else:
        return 0


# 偏差判断函数
def isbias(counts):
    a = max(counts)
    counts.remove(a)
    b = max(counts)
    ratio = float(a / b)
    # print(ratio)
    if ratio > 5:
        return 1
    else:
        return 0


# 倾斜判断函数
def isincline():
    global temp
    img = temp

    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    #cv2.imshow("edge", edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 3600, 10, minLineLength=100, maxLineGap=5)
    if lines is None:
        # print('倾斜判断出错')
        return 0
    else:
        ratio = float((sumY(lines, 2) - sumY(lines, 0)) / (sumY(lines, 3) - sumY(lines, 1)))
        if ratio < np.tan([np.pi / 12]):  # hege
            return 0
        else:
            return 1

    # p2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    # for line in lines:
    #     x1 = line[0][0]
    #     y1 = line[0][1]
    #     x2 = line[0][2]
    #     y2 = line[0][3]
    #     cv2.line(p2, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #
    # cv2.imshow('edges', p2)
    # cv2.waitKey(0)
    # print(lines)


# 翘起判断函数
def iscocked(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("graycocked", img)
    score = cv2.Laplacian(img, cv2.CV_64F).var()
    # print("Laplacian score of given image is ", score)
    if score > 120:  # 这个值可以根据需要自己调节，在我的测试集中100可以满足我的需求。
        return 0
    else:
        return 1

# 弯曲判断函数
