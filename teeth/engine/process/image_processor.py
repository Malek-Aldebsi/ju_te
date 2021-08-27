import numpy as np
import cv2
from django.conf import settings
import os


def buccal(img) :
    img = img
    org = img
    perfect = cv2.imread(os.path.join(settings.STATIC_ROOT, "engine/buccal perfect11.jpg"), cv2.IMREAD_UNCHANGED)
    perf = perfect
    hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_RGB2HSV))
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image2= np.zeros((perf.shape[0],perf.shape[1],3), np.uint8)
    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 40, 255, 0)
    gray1 = cv2.cvtColor(perf, cv2.COLOR_BGR2GRAY)
    ret1, thresh1 = cv2.threshold(gray1, 80, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours1, hierarchy1 = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    area1=0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > area:
                cnt_base = c
                area = cv2.contourArea(c)
    for c in contours1:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > area1:
                cnt_perfect = c
                area1 = cv2.contourArea(c)
    extLeft_base = (cnt_base[cnt_base[:, :, 0].argmin()][0])
    extRight_base = (cnt_base[cnt_base[:, :, 0].argmax()][0])
    extTop_base = (cnt_base[cnt_base[:, :, 1].argmin()][0])
    pix_for_mm = ((extRight_base[0] - extLeft_base[0]) / 40)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (35, 40, 40), (70, 255, 255))
    not_mask = cv2.bitwise_not(mask)
    green = cv2.bitwise_and(img, img, mask=mask)
    green = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
    green = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
    get, gthresh = cv2.threshold(green, 100, 255, 0)
    gthresh = cv2.erode(gthresh, kernel, iterations=1)
    gcontours, hierarchy = cv2.findContours(gthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in gcontours:
        if cv2.contourArea(c) > area:
            gcnt = c
            area = cv2.contourArea(gcnt)
    pivot1 = tuple(gcnt[gcnt[:, :, 1].argmin()][0])
    pivot2 = tuple(gcnt[gcnt[:, :, 1].argmax()][0])
    cv2.line(img, (-1000000, int(pivot1[1] - 1 * pix_for_mm)), (1000000, int(pivot1[1] - 1 * pix_for_mm)), (0, 0, 0),
             thickness=int(pix_for_mm))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 40, 255, 0)
    thresh = cv2.erode(thresh, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if pivot1[1] > cy and cv2.contourArea(c) > area:
                cnt_tooth = c
                area = cv2.contourArea(c)
    area = 0
    for c in gcontours:
        if cv2.contourArea(c) > area:
            cnt_rubber = c
            area = cv2.contourArea(c)
    hull = cv2.convexHull(cnt_tooth, returnPoints=False)
    defects = cv2.convexityDefects(cnt_tooth, hull)
    md = 0
    eplison = 0.01 * cv2.arcLength(cnt_tooth, True)
    approx_tooth = cv2.approxPolyDP(cnt_tooth, eplison, True)
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt_tooth[e][0])
        if md < d:
            md = d
            right = start
    extLeft_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmin()][0])
    extRight_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmax()][0])
    extTop_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmin()][0])
    extBot_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmax()][0])
    b1 = approx_tooth[0][0]
    b2 = approx_tooth[1][0]
    for p in approx_tooth:
        if (p[0][1] > b1[1]):
            b1 = p[0]
    for p in approx_tooth:
        if (p[0][0] != b1[0] and p[0][1] > b2[1]):
            b2 = p[0]
    if (b1[0] > b2[0]):
        tmp = b1
        b1 = b2
        b2 = tmp
    b1 = (b1[0], b1[1] + int(2.5 * pix_for_mm))
    b2 = (b2[0], b2[1] + int(2.5 * pix_for_mm))
    r = (extBot_tooth[1] - extTop_tooth[1]) / pix_for_mm
    mid = int((b1[0] + b2[0]) / 2)
    cv2.line(org, (mid, 1000000), (mid, -1000000), (0, 255, 0), thickness=4)
    vy = pivot2[1]
    line4 = pivot2[1];
    cv2.line(org, (1000000, vy), (-1000000, vy), (0, 255, 0), thickness=3)
    cv2.putText(org, "line 4", (vy - 250, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    vy = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 3", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((12) * pix_for_mm)))), (-1000000, int(vy - ((12) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    vy = int(vy - ((12) * pix_for_mm))
    cv2.putText(org, "line 2", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    line1 = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.circle(org, tuple(extLeft_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extTop_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b1), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b2), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extLeft_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b2), 4, (0, 0, 255), -1)
    cv2.putText(org, "point5", (b1[0] + 5, b1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point6", (b2[0] + 5, b2[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point1", (extTop_tooth[0] + 5, extTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point3", (extLeft_tooth[0] + 5, extLeft_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point4", (extRight_tooth[0] + 5, extRight_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 2)
    a1 = f"the distance between point5 and point6 is(width at cervix) {round((abs(b1[0] - b2[0]) / pix_for_mm), 2)}"
    a2 = f"the distance between point3 and mid line is  {round((abs(extLeft_tooth[0] - mid)) / pix_for_mm, 2)}"
    a3 = f"the distance between point4 and mid line is  {round(abs(extRight_tooth[0] - mid) / pix_for_mm, 2)}"
    a4 = f"the distance between point3 and line 1 is  {round(abs(extLeft_tooth[1] - line1) / pix_for_mm, 2)}"
    a5 = f"the distance between point3 and line 4 is {round(abs(extLeft_tooth[1] - line4) / pix_for_mm, 2)}"
    a6 = f"the distance between point4 and line 1 is {round(abs(extRight_tooth[1] - line1) / pix_for_mm, 2)}"
    a7 = f"the distance between point4 and line 4 is {round(abs(extRight_tooth[1] - line4) / pix_for_mm, 2)}"
    a8 = f"the distance between point3 and point4 is(Maximum width) {round(abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm, 2)}"
    a9 = f"the height using {(pivot2[1] - extTop_tooth[1]) / pix_for_mm}"
    arrayofString = []
    arrayofString.append(a1)
    arrayofString.append(a2)
    arrayofString.append(a3)
    arrayofString.append(a4)
    arrayofString.append(a5)
    arrayofString.append(a6)
    arrayofString.append(a7)
    arrayofString.append(a8)
    arrayofString.append(a9)
    cv2.drawContours(blank_image1, [cnt_perfect], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_tooth], -1, (255, 255, 255), -1)
    blank_image1 = cv2.cvtColor(blank_image1, cv2.COLOR_BGR2GRAY)
    blank_image2 = cv2.cvtColor(blank_image2, cv2.COLOR_BGR2GRAY)

    scale_percent = 80
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    org = cv2.resize(org, dim, interpolation=cv2.INTER_AREA)
    coef_y = 0.5
    coef_x = 0.5
    cnt_perfect[:, :, 0] = cnt_perfect[:, :, 0] * coef_x
    cnt_perfect[:, :, 1] = cnt_perfect[:, :, 1] * coef_y
    blank_image3 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(blank_image3, [cnt_perfect], -1, (255, 255, 255), -1)
    #cv2.imshow('org', org)
    #cv2.waitKey(0)
    return arrayofString ,org

    cv2.waitKey(0)



def distal(img) :

    img =img
    org = img
    hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_RGB2HSV))
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image2 = np.zeros((org.shape[0], img.shape[1], 3), np.uint8)
    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 40, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > area:
                cnt_base = c
                area = cv2.contourArea(c)
    extLeft_base = (cnt_base[cnt_base[:, :, 0].argmin()][0])
    extRight_base = (cnt_base[cnt_base[:, :, 0].argmax()][0])
    extTop_base = (cnt_base[cnt_base[:, :, 1].argmin()][0])
    pix_for_mm = ((extRight_base[0] - extLeft_base[0]) / 50)
    mid = int((extRight_base[0] + extLeft_base[0]) / 2)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (35, 50, 40), (70, 255, 255))
    not_mask = cv2.bitwise_not(mask)
    green = cv2.bitwise_and(img, img, mask=mask)
    green = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
    green = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
    get, gthresh = cv2.threshold(green, 10, 255, 0)
    gthresh = cv2.erode(gthresh, kernel, iterations=1)
    gcontours, hierarchy = cv2.findContours(gthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in gcontours:
        if cv2.contourArea(c) > area:
            gcnt = c
            area = cv2.contourArea(gcnt)
    pivot1 = tuple(gcnt[gcnt[:, :, 1].argmin()][0])
    pivot2 = tuple(gcnt[gcnt[:, :, 1].argmax()][0])
    cv2.line(img, (-1000000, int(pivot1[1] - 1 * pix_for_mm)), (1000000, int(pivot1[1] - 1 * pix_for_mm)), (0, 0, 0),
             thickness=int(2 * pix_for_mm))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 40, 255, 0)
    thresh = cv2.bitwise_and(thresh, thresh, mask=not_mask)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if pivot1[1] > cy and cv2.contourArea(c) > area:
                cnt_tooth = c
                area = cv2.contourArea(c)
    area = 0
    for c in gcontours:
        if cv2.contourArea(c) > area:
            cnt_rubber = c
            area = cv2.contourArea(c)
    hull = cv2.convexHull(cnt_tooth, returnPoints=False)
    defects = cv2.convexityDefects(cnt_tooth, hull)
    md = 0
    eplison = 0.01 * cv2.arcLength(cnt_tooth, True)
    approx_tooth = cv2.approxPolyDP(cnt_tooth, eplison, True)
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt_tooth[e][0])
        if md < d:
            md = d
            left = start
    extLeft_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmin()][0])
    extRight_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmax()][0])
    extTop_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmin()][0])
    extBot_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmax()][0])
    b1 = approx_tooth[0][0]
    b2 = approx_tooth[1][0]
    for p in approx_tooth:
        if (p[0][1] > b1[1]):
            b1 = p[0]
    for p in approx_tooth:
        if (p[0][0] != b1[0] and p[0][1] > b2[1]):
            b2 = p[0]
    if (b1[0] > b2[0]):
        tmp = b1
        b1 = b2
        b2 = tmp
    b1 = (b1[0], b1[1] + int(2.5 * pix_for_mm))
    b2 = (b2[0], b2[1] + int(2.5 * pix_for_mm))

    r = (extBot_tooth[1] - extTop_tooth[1]) / pix_for_mm
    mid = int((extRight_base[0] + extLeft_base[0]) / 2)
    cv2.line(org, (mid, 1000000), (mid, -1000000), (0, 255, 0), thickness=4)
    vy = pivot2[1]
    line4 = pivot2[1];
    cv2.line(org, (1000000, vy), (-1000000, vy), (0, 255, 0), thickness=3)
    cv2.putText(org, "line 4", (vy - 250, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    vy = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 3", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((12) * pix_for_mm)))), (-1000000, int(vy - ((12) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    vy = int(vy - ((12) * pix_for_mm))
    cv2.putText(org, "line 2", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    line1 = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.circle(org, tuple(extLeft_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extTop_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b1), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b2), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extLeft_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b2), 4, (0, 0, 255), -1)
    cv2.circle(org, left, 4, (0, 0, 255), -1)
    cv2.putText(org, "point5", (b1[0] + 5, b1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point6", (b2[0] + 5, b2[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point7", (left[0] + 5, left[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point1", (extTop_tooth[0] + 5, extTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point3", (extLeft_tooth[0] + 5, extLeft_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point4", (extRight_tooth[0] + 5, extRight_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 2)
    print('the distance between point5 and point6 is(width at cervix)', round((abs(b1[0] - b2[0]) / pix_for_mm), 2), 20,
          round(20 / (abs(b1[0] - b2[0]) / pix_for_mm), 2))
    print('the distance between point3 and mid line is', round((abs(extLeft_tooth[0] - mid)) / pix_for_mm, 2), 14,
          round(((abs(extLeft_tooth[0] - mid) / pix_for_mm) / 14), 2))
    print('the distance between point4 and mid line is', round(abs(extRight_tooth[0] - mid) / pix_for_mm, 2), 14,
          round(1 / ((abs(extRight_tooth[0] - mid) / pix_for_mm) / 14), 2))
    print('the distance between point3 and line 1 is', round(abs(extLeft_tooth[1] - line1) / pix_for_mm, 2), 22,
          round((abs(extLeft_tooth[1] - line1) / pix_for_mm) / 22, 2))
    print('the distance between point3 and line 4 is', round(abs(extLeft_tooth[1] - line4) / pix_for_mm, 2), 12,
          round(12 / (abs(extLeft_tooth[1] - line4) / pix_for_mm), 2))
    print('the distance between point4 and line 1 is', round(abs(extRight_tooth[1] - line1) / pix_for_mm, 2), 22,
          round(1 / (22 / (abs(extRight_tooth[1] - line1) / pix_for_mm)), 2))
    print('the distance between point4 and line 4 is', round(abs(extRight_tooth[1] - line4) / pix_for_mm, 2), 12,
          round(1 / (abs(extRight_tooth[1] - line4) / pix_for_mm / 12), 2))
    print('the distance between point3 and point4 is(Maximum width)',
          round(abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm, 2), 28,
          round((abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm / 28), 2))
    cv2.drawContours(blank_image1, [gcnt], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_base], -1, (255, 255, 255), -1)
    cv2.drawContours(img, [gcnt], -1, (255, 255, 255), -1)
    blank_image1 = cv2.cvtColor(blank_image1, cv2.COLOR_BGR2GRAY)
    blank_image2 = cv2.cvtColor(blank_image2, cv2.COLOR_BGR2GRAY)
    print("shape matching= ", cv2.matchShapes(blank_image1, blank_image2, cv2.CONTOURS_MATCH_I2, 0))
    print("the height using", (pivot1[1] - extTop_tooth[1]) / pix_for_mm)
    scale_percent = 70
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    org = cv2.resize(org, dim, interpolation=cv2.INTER_AREA)
    hue = cv2.resize(hue, dim, interpolation=cv2.INTER_AREA)
    sat = cv2.resize(sat, dim, interpolation=cv2.INTER_AREA)
    val = cv2.resize(val, dim, interpolation=cv2.INTER_AREA)
    green = cv2.resize(green, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('org', org)
    cv2.imshow('img', img)
    cv2.imshow('g', green)
    cv2.imshow('h', hue)
    cv2.imshow('s', sat)
    cv2.imshow('v', val)
    cv2.waitKey(0)




def mesial(img) :

    img = img
    org = img
    hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_RGB2HSV))
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image2 = np.zeros((org.shape[0], img.shape[1], 3), np.uint8)
    kernel = np.ones((7, 7), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 40, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > area:
                cnt_base = c
                area = cv2.contourArea(c)
    extLeft_base = (cnt_base[cnt_base[:, :, 0].argmin()][0])
    extRight_base = (cnt_base[cnt_base[:, :, 0].argmax()][0])
    extTop_base = (cnt_base[cnt_base[:, :, 1].argmin()][0])
    pix_for_mm = ((extRight_base[0] - extLeft_base[0]) / 50)
    mid = int((extRight_base[0] + extLeft_base[0]) / 2)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (28, 50, 40), (70, 255, 255))
    not_mask = cv2.bitwise_not(mask)
    green = cv2.bitwise_and(img, img, mask=mask)
    green = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
    green = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
    get, gthresh = cv2.threshold(green, 10, 255, 0)
    gthresh = cv2.erode(gthresh, kernel, iterations=1)
    gcontours, hierarchy = cv2.findContours(gthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in gcontours:
        if cv2.contourArea(c) > area:
            gcnt = c
            area = cv2.contourArea(gcnt)
    pivot1 = tuple(gcnt[gcnt[:, :, 1].argmin()][0])
    pivot2 = tuple(gcnt[gcnt[:, :, 1].argmax()][0])
    cv2.line(img, (-1000000, int(pivot1[1] - 1 * pix_for_mm)), (1000000, int(pivot1[1] - 1 * pix_for_mm)), (0, 0, 0),
             thickness=int(2 * pix_for_mm))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 40, 255, 0)
    thresh = cv2.erode(thresh, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if pivot1[1] > cy and cv2.contourArea(c) > area:
                cnt_tooth = c
                area = cv2.contourArea(c)
    area = 0
    for c in gcontours:
        if cv2.contourArea(c) > area:
            cnt_rubber = c
            area = cv2.contourArea(c)
    hull = cv2.convexHull(cnt_tooth, returnPoints=False)
    defects = cv2.convexityDefects(cnt_tooth, hull)
    md = 0
    eplison = 0.01 * cv2.arcLength(cnt_tooth, True)
    approx_tooth = cv2.approxPolyDP(cnt_tooth, eplison, True)
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt_tooth[s][0])
        if md < d:
            md = d
            right = start
    extLeft_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmin()][0])
    extRight_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmax()][0])
    extTop_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmin()][0])
    extBot_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmax()][0])
    b1 = approx_tooth[0][0]
    b2 = approx_tooth[1][0]
    for p in approx_tooth:
        if (p[0][1] > b1[1]):
            b1 = p[0]
    for p in approx_tooth:
        if (p[0][0] != b1[0] and p[0][1] > b2[1]):
            b2 = p[0]
    if (b1[0] > b2[0]):
        tmp = b1
        b1 = b2
        b2 = tmp
    b1 = (b1[0], b1[1] + int(2.5 * pix_for_mm))
    b2 = (b2[0], b2[1] + int(2.5 * pix_for_mm))
    r = (extBot_tooth[1] - extTop_tooth[1]) / pix_for_mm
    mid = int((extRight_base[0] + extLeft_base[0]) / 2)
    cv2.line(org, (mid, 1000000), (mid, -1000000), (0, 255, 0), thickness=4)
    vy = pivot2[1]
    line4 = pivot2[1];
    cv2.line(org, (1000000, vy), (-1000000, vy), (0, 255, 0), thickness=3)
    cv2.putText(org, "line 4", (vy - 250, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    vy = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 3", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((12) * pix_for_mm)))), (-1000000, int(vy - ((12) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    vy = int(vy - ((12) * pix_for_mm))
    cv2.putText(org, "line 2", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    line1 = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.circle(org, tuple(extLeft_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extTop_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b1), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b2), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extLeft_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b2), 4, (0, 0, 255), -1)
    cv2.circle(org, right, 4, (0, 0, 255), -1)
    cv2.putText(org, "point5", (b1[0] + 5, b1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point6", (b2[0] + 5, b2[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point7", (right[0] + 5, right[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point1", (extTop_tooth[0] + 5, extTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point3", (extLeft_tooth[0] + 5, extLeft_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point4", (extRight_tooth[0] + 5, extRight_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 2)
    print('the distance between point5 and point6 is(width at cervix)', round((abs(b1[0] - b2[0]) / pix_for_mm), 2), 20,
          round(20 / (abs(b1[0] - b2[0]) / pix_for_mm), 2))
    print('the distance between point3 and mid line is', round((abs(extLeft_tooth[0] - mid)) / pix_for_mm, 2), 14,
          round(((abs(extLeft_tooth[0] - mid) / pix_for_mm) / 14), 2))
    print('the distance between point4 and mid line is', round(abs(extRight_tooth[0] - mid) / pix_for_mm, 2), 14,
          round(1 / ((abs(extRight_tooth[0] - mid) / pix_for_mm) / 14), 2))
    print('the distance between point3 and line 1 is', round(abs(extLeft_tooth[1] - line1) / pix_for_mm, 2), 22,
          round((abs(extLeft_tooth[1] - line1) / pix_for_mm) / 22, 2))
    print('the distance between point3 and line 4 is', round(abs(extLeft_tooth[1] - line4) / pix_for_mm, 2), 12,
          round(12 / (abs(extLeft_tooth[1] - line4) / pix_for_mm), 2))
    print('the distance between point4 and line 1 is', round(abs(extRight_tooth[1] - line1) / pix_for_mm, 2), 22,
          round(1 / (22 / (abs(extRight_tooth[1] - line1) / pix_for_mm)), 2))
    print('the distance between point4 and line 4 is', round(abs(extRight_tooth[1] - line4) / pix_for_mm, 2), 12,
          round(1 / (abs(extRight_tooth[1] - line4) / pix_for_mm / 12), 2))
    print('the distance between point3 and point4 is(Maximum width)',
          round(abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm, 2), 28,
          round((abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm / 28), 2))
    cv2.drawContours(blank_image1, [gcnt], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_base], -1, (255, 255, 255), -1)
    cv2.drawContours(img, [gcnt], -1, (255, 255, 255), -1)

    blank_image1 = cv2.cvtColor(blank_image1, cv2.COLOR_BGR2GRAY)
    blank_image2 = cv2.cvtColor(blank_image2, cv2.COLOR_BGR2GRAY)
    print("shape matching= ", cv2.matchShapes(blank_image1, blank_image2, cv2.CONTOURS_MATCH_I2, 0))
    print("the height ", (pivot1[1] - extTop_tooth[1]) / pix_for_mm)
    scale_percent = 70
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    org = cv2.resize(org, dim, interpolation=cv2.INTER_AREA)
    hue = cv2.resize(hue, dim, interpolation=cv2.INTER_AREA)
    sat = cv2.resize(sat, dim, interpolation=cv2.INTER_AREA)
    val = cv2.resize(val, dim, interpolation=cv2.INTER_AREA)
    green = cv2.resize(green, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('org', org)
    cv2.imshow('img', img)
    cv2.imshow('g', green)
    cv2.imshow('h', hue)
    cv2.imshow('s', sat)
    cv2.imshow('v', val)
    cv2.waitKey(0)




def lingual(img):

    img = img
    org = img
    hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_RGB2HSV))
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image2 = np.zeros((org.shape[0], img.shape[1], 3), np.uint8)
    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 40, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > area:
                cnt_base = c
                area = cv2.contourArea(c)
    extLeft_base = (cnt_base[cnt_base[:, :, 0].argmin()][0])
    extRight_base = (cnt_base[cnt_base[:, :, 0].argmax()][0])
    extTop_base = (cnt_base[cnt_base[:, :, 1].argmin()][0])
    pix_for_mm = ((extRight_base[0] - extLeft_base[0]) / 40)
    mid = int((extRight_base[0] + extLeft_base[0]) / 2)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (35, 50, 40), (70, 255, 255))
    not_mask = cv2.bitwise_not(mask)
    green = cv2.bitwise_and(img, img, mask=mask)
    green = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
    green = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
    get, gthresh = cv2.threshold(green, 10, 255, 0)
    gthresh = cv2.erode(gthresh, kernel, iterations=1)
    gcontours, hierarchy = cv2.findContours(gthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in gcontours:
        if cv2.contourArea(c) > area:
            gcnt = c
            area = cv2.contourArea(gcnt)
    pivot1 = tuple(gcnt[gcnt[:, :, 1].argmin()][0])
    pivot2 = tuple(gcnt[gcnt[:, :, 1].argmax()][0])
    cv2.line(img, (-1000000, int(pivot1[1] - 1 * pix_for_mm)), (1000000, int(pivot1[1] - 1 * pix_for_mm)), (0, 0, 0),
             thickness=int(pix_for_mm))
    mask = cv2.inRange(hsv, (61, 155, 84), (179, 255, 255))
    red = cv2.bitwise_and(img, img, mask=mask)
    red = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
    get, rthresh = cv2.threshold(red, 40, 255, 0)
    rcontours, hierarchy = cv2.findContours(rthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    subTop_tooth = tuple(rcontours[0][rcontours[0][:, :, 1].argmin()][0])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 40, 255, 0)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if pivot1[1] > cy and cv2.contourArea(c) > area:
                cnt_tooth = c
                area = cv2.contourArea(c)
    area = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if pivot1[1] < cy and cv2.contourArea(c) > area:
                cnt_base = c
                area = cv2.contourArea(c)
    area = 0
    for c in gcontours:
        if cv2.contourArea(c) > area:
            cnt_rubber = c
            area = cv2.contourArea(c)
    hull = cv2.convexHull(cnt_tooth, returnPoints=False)
    defects = cv2.convexityDefects(cnt_tooth, hull)
    md = 0
    eplison = 0.0005 * cv2.arcLength(cnt_tooth, True)
    approx_tooth = cv2.approxPolyDP(cnt_tooth, eplison, True)
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt_tooth[e][0])
        if md < d:
            md = d
            left = start
    extLeft_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmin()][0])
    extRight_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmax()][0])
    extTop_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmin()][0])
    extBot_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmax()][0])
    b1 = (cnt_rubber[cnt_rubber[:, :, 0].argmin()][0])
    b2 = (cnt_rubber[cnt_rubber[:, :, 0].argmax()][0])
    extLeft_base = (cnt_base[cnt_base[:, :, 0].argmin()][0])
    extRight_base = (cnt_base[cnt_base[:, :, 0].argmax()][0])
    extTop_base = (cnt_base[cnt_base[:, :, 1].argmin()][0])
    pix_for_mm = ((extRight_base[0] - extLeft_base[0]) / 40)
    r = (extBot_tooth[1] - extTop_tooth[1]) / pix_for_mm
    mid = int((extRight_base[0] + extLeft_base[0]) / 2)
    cv2.line(org, (mid, 1000000), (mid, -1000000), (0, 255, 0), thickness=4)
    vy = pivot2[1]
    line4 = pivot2[1];
    cv2.line(org, (1000000, vy), (-1000000, vy), (0, 255, 0), thickness=3)
    cv2.putText(org, "line 4", (vy - 250, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    vy = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 3", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((12) * pix_for_mm)))), (-1000000, int(vy - ((12) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    vy = int(vy - ((12) * pix_for_mm))
    cv2.putText(org, "line 2", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=3)
    line1 = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.circle(org, tuple(extLeft_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extTop_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b1), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b2), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extLeft_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(b2), 4, (0, 0, 255), -1)
    cv2.circle(org, subTop_tooth, 4, (0, 0, 255), -1)
    cv2.putText(org, "point5", (b1[0] + 5, b1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point6", (b2[0] + 5, b2[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point7", (subTop_tooth[0] + 5, subTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point1", (extTop_tooth[0] + 5, extTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point3", (extLeft_tooth[0] + 5, extLeft_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point4", (extRight_tooth[0] + 5, extRight_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 2)
    print('the distance between point5 and point6 is(width at cervix)', round((abs(b1[0] - b2[0]) / pix_for_mm), 2), 20,
          round(20 / (abs(b1[0] - b2[0]) / pix_for_mm), 2))
    print('the distance between point3 and mid line is', round((abs(extLeft_tooth[0] - mid)) / pix_for_mm, 2), 14,
          round(((abs(extLeft_tooth[0] - mid) / pix_for_mm) / 14), 2))
    print('the distance between point4 and mid line is', round(abs(extRight_tooth[0] - mid) / pix_for_mm, 2), 14,
          round(1 / ((abs(extRight_tooth[0] - mid) / pix_for_mm) / 14), 2))
    print('the distance between point3 and line 1 is', round(abs(extLeft_tooth[1] - line1) / pix_for_mm, 2), 22,
          round((abs(extLeft_tooth[1] - line1) / pix_for_mm) / 22, 2))
    print('the distance between point3 and line 4 is', round(abs(extLeft_tooth[1] - line4) / pix_for_mm, 2), 12,
          round(12 / (abs(extLeft_tooth[1] - line4) / pix_for_mm), 2))
    print('the distance between point4 and line 1 is', round(abs(extRight_tooth[1] - line1) / pix_for_mm, 2), 22,
          round(1 / (22 / (abs(extRight_tooth[1] - line1) / pix_for_mm)), 2))
    print('the distance between point4 and line 4 is', round(abs(extRight_tooth[1] - line4) / pix_for_mm, 2), 12,
          round(1 / (abs(extRight_tooth[1] - line4) / pix_for_mm / 12), 2))
    print('the distance between point3 and point4 is(Maximum width)',
          round(abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm, 2), 28,
          round((abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm / 28), 2))
    cv2.drawContours(blank_image1, [gcnt], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_base], -1, (255, 255, 255), -1)
    blank_image1 = cv2.cvtColor(blank_image1, cv2.COLOR_BGR2GRAY)
    blank_image2 = cv2.cvtColor(blank_image2, cv2.COLOR_BGR2GRAY)
    print("shape matching= ", cv2.matchShapes(blank_image1, blank_image2, cv2.CONTOURS_MATCH_I2, 0))
    print("the height using", (pivot1[1] - extTop_tooth[1]) / pix_for_mm)
    scale_percent = 80
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    org = cv2.resize(org, dim, interpolation=cv2.INTER_AREA)
    hue = cv2.resize(hue, dim, interpolation=cv2.INTER_AREA)
    sat = cv2.resize(sat, dim, interpolation=cv2.INTER_AREA)
    val = cv2.resize(val, dim, interpolation=cv2.INTER_AREA)
    green = cv2.resize(green, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('org', org)
    cv2.imshow('img', img)
    cv2.imshow('g', green)
    cv2.imshow('h', hue)
    cv2.imshow('s', sat)
    cv2.imshow('v', val)
    cv2.waitKey(0)


