import cv2
import numpy as np
from django.conf import settings
import os

kernel = np.ones((5, 5), np.uint8)


def shapeMatch(img1 , img2 , cntImg2):
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, thr_inter = cv2.threshold(img1, 50, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    ret, thr_union = cv2.threshold(img2, 50, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    intersection = cv2.bitwise_and(img1,img2,mask=None)
    union = cv2.bitwise_or(img1 , img2 , mask=None)
    ret, thr_inter = cv2.threshold(intersection, 0, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)
    ret, thr_union = cv2.threshold(union, 70, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)
    contours_inter, hierarchy = cv2.findContours(thr_inter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_union, hierarchy = cv2.findContours(thr_union, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    cnt_inter=0
    cnt_union=0
    for c in  contours_inter:
        if(cv2.contourArea(c)>area):
            area = cv2.contourArea(c)
            cnt_inter = c
    area=0
    for c in contours_union:
        if (cv2.contourArea(c) > area):
            area = cv2.contourArea(c)
            cnt_union = c
    return cv2.contourArea(cnt_inter)/cv2.contourArea(cnt_union);

def find_rubber(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (35, 40, 40), (70, 255, 255))
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
    mask_inv = cv2.bitwise_not(mask)
    return gcnt, mask_inv


def find_base(contours, rubber_bottom):
    barea = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > barea and cy > rubber_bottom[1]:
                cnt_base = c
                barea = cv2.contourArea(c)
    return cnt_base


def find_crown(contours, rubber_bottom):
    cnt_crown = contours[0]
    carea = 0
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > carea and cy < rubber_bottom[1]:
                cnt_crown = c
                carea = cv2.contourArea(c)
    return cnt_crown


def find_red(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask = mask0 + mask1
    red = cv2.bitwise_and(img, img, mask=mask)
    red = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
    get, rthresh = cv2.threshold(red, 45, 255, 0)
    rcontours, hierarchy = cv2.findContours(rthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    arear = 0
    for c in rcontours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > arear:
                cnt_red = c
                arear = cv2.contourArea(c)
    return cnt_red

    

def buccal(img):
    org = img
    perfect = cv2.imread(os.path.join(settings.STATIC_ROOT, "engine/buccal-perfect.jpg"), cv2.IMREAD_UNCHANGED)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(gray_img, 40, 255, 0)
    gcnt, mask = find_rubber(img)
    thresh_img = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
    thresh_img = cv2.erode(thresh_img, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rubber_bootom = tuple(gcnt[gcnt[:, :, 1].argmax()][0])
    cnt_base = find_base(contours, rubber_bootom)
    cnt_tooth = find_crown(contours, rubber_bootom)
    extLeft_base = (cnt_base[cnt_base[:, :, 0].argmin()][0])
    extRight_base = (cnt_base[cnt_base[:, :, 0].argmax()][0])
    pix_for_mm = ((extRight_base[0] - extLeft_base[0]) / 40)
    extLeft_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmin()][0])
    extRight_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmax()][0])
    extTop_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmin()][0])
    extBot_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmax()][0])
    cervix_pointl = (gcnt[gcnt[:, :, 0].argmin()][0])
    cervix_pointr = (gcnt[gcnt[:, :, 0].argmax()][0])
    mid = int((cervix_pointl[0] + cervix_pointr[0]) / 2)
    cv2.line(org, (mid, 10000000), (mid, -10000000), (0, 255, 0), thickness=int(pix_for_mm))
    vy = rubber_bootom[1]
    line4 = vy;
    cv2.line(org, (10000000, vy), (-10000000, vy), (0, 255, 0), thickness=int(pix_for_mm))
    cv2.putText(org, "line 4", (vy - 250, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 3", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((12) * pix_for_mm)))), (-1000000, int(vy - ((12) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((12) * pix_for_mm))
    cv2.putText(org, "line 2", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    line1 = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.circle(org, tuple(extLeft_tooth), 4, (0, 255, 255), -1)
    cv2.circle(org, tuple(extRight_tooth), 4, (0, 255, 255), -1)
    cv2.circle(org, tuple(extTop_tooth), 4, (0, 255, 255), -1)
    cv2.circle(org, tuple(cervix_pointl), 4, (0, 255, 255), -1)
    cv2.circle(org, tuple(cervix_pointr), 4, (0, 255, 255), -1)
    cv2.circle(org, tuple(extRight_base), 4, (0, 255, 255), -1)
    cv2.circle(org, tuple(extLeft_base), 4, (0, 255, 255), -1)
    cv2.putText(org, "point5", (cervix_pointl[0] + 5, cervix_pointr[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point6", (cervix_pointr[0] + 5, cervix_pointr[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point1", (extTop_tooth[0] + 5, extTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point3", (extLeft_tooth[0] + 5, extLeft_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point4", (extRight_tooth[0] + 5, extRight_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 2)
    a1 = f" 5 to 6 is(width at cervix) {round((abs(cervix_pointl[0] - cervix_pointr[0]) / pix_for_mm), 2)}"
    a2 = f"3 to ml {round((abs(extLeft_tooth[0] - mid)) / pix_for_mm, 2)}"
    a3 = f"4 to Ml {round(abs(extRight_tooth[0] - mid) / pix_for_mm, 2)}"
    a4 = f"3 to L1  {round(abs(extLeft_tooth[1] - line1) / pix_for_mm, 2)}"
    a5 = f"3 to l4  {round(abs(extLeft_tooth[1] - line4) / pix_for_mm, 2)}"
    a6 = f"4 to l1  {round(abs(extRight_tooth[1] - line1) / pix_for_mm, 2)}"
    a7 = f"4 to l4{round(abs(extRight_tooth[1] - line4) / pix_for_mm, 2)}"
    a8 = f"3 to 4 is(Maximum width) {round(abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm, 2)}"
    a9 = f"the height: {(rubber_bootom[1] - extTop_tooth[1]) / pix_for_mm}"
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
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image2 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    gray_perfect = cv2.cvtColor(perfect, cv2.COLOR_BGR2GRAY)
    ret, thresh_perfect = cv2.threshold(gray_perfect, 80, 255, 0)
    contours1, hierarchy1 = cv2.findContours(thresh_perfect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    parea = 0
    for c in contours1:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > parea:
                cnt_perfect = c
                parea = cv2.contourArea(c)
    x_t, y_t, w_t, h_t = cv2.boundingRect(cnt_tooth)
    x_p, y_p, w_p, h_p = cv2.boundingRect(cnt_perfect)
    coef_y = h_t / h_p
    coef_x = w_t / w_p
    cnt_perfect[:, :, 0] = cnt_perfect[:, :, 0] * coef_x
    cnt_perfect[:, :, 1] = cnt_perfect[:, :, 1] * coef_y
    cv2.drawContours(blank_image1, [cnt_tooth], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_perfect], -1, (255, 255, 255), -1, offset=(x_t - x_p, y_t - y_p))
    shape_match = shapeMatch(blank_image1, blank_image2, cnt_perfect)
    a10 = f"shape matching= {shape_match}"
    arrayofString.append(a10)
    scale_percent = 80
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    org = cv2.resize(org, dim, interpolation=cv2.INTER_AREA)

    return arrayofString, org#, (rubber_bootom[1] - extTop_tooth[1]) / pix_for_mm



def distal(img):
    org = img
    perfect = cv2.imread(os.path.join(settings.STATIC_ROOT, "engine/distal-perfect.jpeg"), cv2.IMREAD_UNCHANGED)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(gray_img, 40, 255, 0)
    gcnt, mask = find_rubber(img)
    thresh_img = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
    thresh_img = cv2.erode(thresh_img, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rubber_bootom = tuple(gcnt[gcnt[:, :, 1].argmax()][0])
    cnt_base = find_base(contours, rubber_bootom)
    cnt_tooth = find_crown(contours, rubber_bootom)
    extLeft_base = (cnt_base[cnt_base[:, :, 0].argmin()][0])
    extRight_base = (cnt_base[cnt_base[:, :, 0].argmax()][0])
    pix_for_mm = ((extRight_base[0] - extLeft_base[0]) / 40)
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
    cervix_pointl = (gcnt[gcnt[:, :, 0].argmin()][0])
    cervix_pointr = (gcnt[gcnt[:, :, 0].argmax()][0])
    mid = int((cervix_pointl[0] + cervix_pointr[0]) / 2)
    cv2.line(org, (mid, 10000000), (mid, -10000000), (0, 255, 0), thickness=int(pix_for_mm))
    vy = rubber_bootom[1]
    line4 = vy;
    cv2.line(org, (10000000, vy), (-10000000, vy), (0, 255, 0), thickness=int(pix_for_mm))
    cv2.putText(org, "line 4", (vy - 250, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 3", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((12) * pix_for_mm)))), (-1000000, int(vy - ((12) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((12) * pix_for_mm))
    cv2.putText(org, "line 2", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    line1 = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.circle(org, tuple(extLeft_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extTop_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointl), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointr), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extLeft_base), 4, (0, 0, 255), -1)
    cv2.circle(org, left, 4, (0, 0, 255), -1)
    cv2.putText(org, "point5", (cervix_pointl[0] + 5, cervix_pointl[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point6", (cervix_pointr[0] + 5, cervix_pointr[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point7", (left[0] + 5, left[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point1", (extTop_tooth[0] + 5, extTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point4", (extLeft_tooth[0] + 5, extLeft_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point3", (extRight_tooth[0] + 5, extRight_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 2)

    a1 = f"5 and 6 is(width at cervix) {round((abs(cervix_pointl[0] - cervix_pointr[0]) / pix_for_mm), 2)}"
    a2 = f"4 and ml is  {round((abs(extLeft_tooth[0] - mid)) / pix_for_mm, 2)}"
    a3 = f"3 and ml is  {round(abs(extRight_tooth[0] - mid) / pix_for_mm, 2)}"
    a4 = f"4 and l1 is  {round(abs(extLeft_tooth[1] - line1) / pix_for_mm, 2)}"
    a5 = f"4 and l4 is {round(abs(extLeft_tooth[1] - line4) / pix_for_mm, 2)}"
    a6 = f"3 and l1 is {round(abs(extRight_tooth[1] - line1) / pix_for_mm, 2)}"
    a7 = f"3 and l4 is {round(abs(extRight_tooth[1] - line4) / pix_for_mm, 2)}"
    a8 = f"3 and point4 is(Maximum width) {round(abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm, 2)}"
    a9 = f"the height: {(rubber_bootom[1] - extTop_tooth[1]) / pix_for_mm}"
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
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image2 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    gray_perfect = cv2.cvtColor(perfect, cv2.COLOR_BGR2GRAY)
    ret, thresh_perfect = cv2.threshold(gray_perfect, 80, 255, 0)
    contours1, hierarchy1 = cv2.findContours(thresh_perfect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    parea = 0
    for c in contours1:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > parea:
                cnt_perfect = c
                parea = cv2.contourArea(c)
    x_t, y_t, w_t, h_t = cv2.boundingRect(cnt_tooth)
    x_p, y_p, w_p, h_p = cv2.boundingRect(cnt_perfect)
    coef_y = h_t / h_p
    coef_x = w_t / w_p
    cnt_perfect[:, :, 0] = cnt_perfect[:, :, 0] * coef_x
    cnt_perfect[:, :, 1] = cnt_perfect[:, :, 1] * coef_y
    cv2.drawContours(blank_image1, [cnt_tooth], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_perfect], -1, (255, 255, 255), -1, offset=(x_t - x_p, y_t - y_p))
    shape_match = shapeMatch(blank_image1, blank_image2, cnt_perfect)
    a10 = f"shape matching= {shape_match}"
    arrayofString.append(a10)
    scale_percent = 80
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    org = cv2.resize(org, dim, interpolation=cv2.INTER_AREA)
    return arrayofString, org#, (rubber_bootom[1] - extTop_tooth[1]) / pix_for_mm



def mesial(img):
    org = img
    perfect = cv2.imread(os.path.join(settings.STATIC_ROOT, "engine/mesial-perfect.jpg"), cv2.IMREAD_UNCHANGED)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(gray_img, 40, 255, 0)
    gcnt, mask = find_rubber(img)
    thresh_img = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
    thresh_img = cv2.erode(thresh_img, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rubber_bootom = tuple(gcnt[gcnt[:, :, 1].argmax()][0])
    cnt_base = find_base(contours, rubber_bootom)
    cnt_tooth = find_crown(contours, rubber_bootom)
    extLeft_base = (cnt_base[cnt_base[:, :, 0].argmin()][0])
    extRight_base = (cnt_base[cnt_base[:, :, 0].argmax()][0])
    pix_for_mm = ((extRight_base[0] - extLeft_base[0]) / 40)
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
    cervix_pointl = (gcnt[gcnt[:, :, 0].argmin()][0])
    cervix_pointr = (gcnt[gcnt[:, :, 0].argmax()][0])
    mid = int((cervix_pointl[0] + cervix_pointr[0]) / 2)
    cv2.line(org, (mid, 10000000), (mid, -10000000), (0, 255, 0), thickness=int(pix_for_mm))
    vy = rubber_bootom[1]
    line4 = vy;
    cv2.line(org, (10000000, vy), (-10000000, vy), (0, 255, 0), thickness=int(pix_for_mm))
    cv2.putText(org, "line 4", (vy - 250, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 3", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((12) * pix_for_mm)))), (-1000000, int(vy - ((12) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((12) * pix_for_mm))
    cv2.putText(org, "line 2", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    line1 = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.circle(org, tuple(extLeft_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extTop_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointl), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointr), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extLeft_base), 4, (0, 0, 255), -1)
    cv2.circle(org, right, 4, (0, 0, 255), -1)
    cv2.putText(org, "point5", (cervix_pointl[0] + 5, cervix_pointl[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point6", (cervix_pointr[0] + 5, cervix_pointr[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point7", (right[0] + 5, right[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(org, "point1", (extTop_tooth[0] + 5, extTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point3", (extLeft_tooth[0] + 5, extLeft_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point4", (extRight_tooth[0] + 5, extRight_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 2)

    a1 = f"5 and 6 is(width at cervix) {round((abs(cervix_pointl[0] - cervix_pointr[0]) / pix_for_mm), 2)}"
    a2 = f"3 and ml is {round((abs(extLeft_tooth[0] - mid)) / pix_for_mm, 2)}"
    a3 = f"4 and ml is  {round(abs(extRight_tooth[0] - mid) / pix_for_mm, 2)}"
    a4 = f"3 and l1 is  {round(abs(extLeft_tooth[1] - line1) / pix_for_mm, 2)}"
    a5 = f"3 and l4 is {round(abs(extLeft_tooth[1] - line4) / pix_for_mm, 2)}"
    a6 = f"4 and l1 is {round(abs(extRight_tooth[1] - line1) / pix_for_mm, 2)}"
    a7 = f"4 and l4 is {round(abs(extRight_tooth[1] - line4) / pix_for_mm, 2)}"
    a8 = f"3 and 4 is(Maximum width) {round(abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm, 2)}"
    a9 = f"the height: {(rubber_bootom[1] - extTop_tooth[1]) / pix_for_mm}"
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
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image2 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    gray_perfect = cv2.cvtColor(perfect, cv2.COLOR_BGR2GRAY)
    ret, thresh_perfect = cv2.threshold(gray_perfect, 80, 255, 0)
    contours1, hierarchy1 = cv2.findContours(thresh_perfect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    parea = 0
    for c in contours1:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > parea:
                cnt_perfect = c
                parea = cv2.contourArea(c)
    x_t, y_t, w_t, h_t = cv2.boundingRect(cnt_tooth)
    x_p, y_p, w_p, h_p = cv2.boundingRect(cnt_perfect)
    coef_y = h_t / h_p
    coef_x = w_t / w_p
    cnt_perfect[:, :, 0] = cnt_perfect[:, :, 0] * coef_x
    cnt_perfect[:, :, 1] = cnt_perfect[:, :, 1] * coef_y
    cv2.drawContours(blank_image1, [cnt_tooth], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_perfect], -1, (255, 255, 255), -1, offset=(x_t - x_p, y_t - y_p))
    shape_match = shapeMatch(blank_image1, blank_image2, cnt_perfect)
    a10 = f"shape matching= {shape_match}"
    arrayofString.append(a10)
  
    scale_percent = 80
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    org = cv2.resize(org, dim, interpolation=cv2.INTER_AREA)

    return arrayofString, org#, (rubber_bootom[1] - extTop_tooth[1]) / pix_for_mm


def lingual(img):
    org = img
    perfect = cv2.imread(os.path.join(settings.STATIC_ROOT, "engine/lingual-perfect.jpg"), cv2.IMREAD_UNCHANGED)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(gray_img, 40, 255, 0)
    gcnt, mask = find_rubber(img)
    thresh_img = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
    thresh_img = cv2.erode(thresh_img, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rubber_bootom = tuple(gcnt[gcnt[:, :, 1].argmax()][0])
    cnt_base = find_base(contours, rubber_bootom)
    cnt_tooth = find_crown(contours, rubber_bootom)
    extLeft_base = (cnt_base[cnt_base[:, :, 0].argmin()][0])
    extRight_base = (cnt_base[cnt_base[:, :, 0].argmax()][0])
    pix_for_mm = ((extRight_base[0] - extLeft_base[0]) / 40)
    extLeft_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmin()][0])
    extRight_tooth = (cnt_tooth[cnt_tooth[:, :, 0].argmax()][0])
    extTop_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmin()][0])
    extBot_tooth = (cnt_tooth[cnt_tooth[:, :, 1].argmax()][0])
    cervix_pointl = (gcnt[gcnt[:, :, 0].argmin()][0])
    cervix_pointr = (gcnt[gcnt[:, :, 0].argmax()][0])
    mid = int((cervix_pointl[0] + cervix_pointr[0]) / 2)
    cv2.line(org, (mid, 10000000), (mid, -10000000), (0, 255, 0), thickness=int(pix_for_mm))
    vy = rubber_bootom[1]
    line4 = vy;
    cv2.line(org, (10000000, vy), (-10000000, vy), (0, 255, 0), thickness=int(pix_for_mm))
    cv2.putText(org, "line 4", (vy - 250, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((11) * pix_for_mm))
    cv2.putText(org, "line 3", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((12) * pix_for_mm)))), (-1000000, int(vy - ((12) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((12) * pix_for_mm))
    cv2.putText(org, "line 2", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.line(org, (1000000, int(vy - (((11) * pix_for_mm)))), (-1000000, int(vy - ((11) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    line1 = int(vy - ((11) * pix_for_mm))
    cnt_red = find_red(img)
    subTop_tooth = tuple(cnt_red[cnt_red[:, :, 1].argmin()][0])
    cv2.putText(org, "line 1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.circle(org, tuple(extLeft_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extTop_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointl), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointr), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extLeft_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointl), 4, (0, 0, 255), -1)
    cv2.circle(org, subTop_tooth, 4, (0, 0, 255), -1)
    cv2.putText(org, "point5", (cervix_pointl[0] + 5, cervix_pointl[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point6", (cervix_pointr[0] + 5, cervix_pointr[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point7", (subTop_tooth[0] + 5, subTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point1", (extTop_tooth[0] + 5, extTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point4", (extLeft_tooth[0] + 5, extLeft_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                2)
    cv2.putText(org, "point3", (extRight_tooth[0] + 5, extRight_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 2)

    a1 = f"5 and 6 is(width at cervix) {round((abs(cervix_pointl[0] - cervix_pointr[0]) / pix_for_mm), 2)}"
    a2 = f"4 and ml is  {round((abs(extLeft_tooth[0] - mid)) / pix_for_mm, 2)}"
    a3 = f"3 and ml is  {round(abs(extRight_tooth[0] - mid) / pix_for_mm, 2)}"
    a4 = f"4 and l1 is  {round(abs(extLeft_tooth[1] - line1) / pix_for_mm, 2)}"
    a5 = f"4 and l4 is {round(abs(extLeft_tooth[1] - line4) / pix_for_mm, 2)}"
    a6 = f"3 and l1 is {round(abs(extRight_tooth[1] - line1) / pix_for_mm, 2)}"
    a7 = f"3 and l4 is {round(abs(extRight_tooth[1] - line4) / pix_for_mm, 2)}"
    a8 = f"3 and 4 is(Maximum width) {round(abs(extLeft_tooth[0] - extRight_tooth[0]) / pix_for_mm, 2)}"
    a9 = f"the height: {(rubber_bootom[1] - extTop_tooth[1]) / pix_for_mm}"
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
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image2 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    gray_perfect = cv2.cvtColor(perfect, cv2.COLOR_BGR2GRAY)
    ret, thresh_perfect = cv2.threshold(gray_perfect, 80, 255, 0)
    contours1, hierarchy1 = cv2.findContours(thresh_perfect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    parea = 0
    for c in contours1:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > parea:
                cnt_perfect = c
                parea = cv2.contourArea(c)
    x_t, y_t, w_t, h_t = cv2.boundingRect(cnt_tooth)
    x_p, y_p, w_p, h_p = cv2.boundingRect(cnt_perfect)
    coef_y = h_t / h_p
    coef_x = w_t / w_p
    cnt_perfect[:, :, 0] = cnt_perfect[:, :, 0] * coef_x
    cnt_perfect[:, :, 1] = cnt_perfect[:, :, 1] * coef_y
    cv2.drawContours(blank_image1, [cnt_tooth], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_perfect], -1, (255, 255, 255), -1, offset=(x_t - x_p, y_t - y_p))
    shape_match = shapeMatch(blank_image1, blank_image2, cnt_perfect)
    a10 = f"shape matching= {shape_match}"
    arrayofString.append(a10)
    scale_percent = 80
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    org = cv2.resize(org, dim, interpolation=cv2.INTER_AREA)

    return arrayofString, org#, (rubber_bootom[1] - extTop_tooth[1]) / pix_for_mm



def top_view(img):
    org = img
    perfect = cv2.imread(os.path.join(settings.STATIC_ROOT, "engine/top_view-perfect.jpg"), cv2.IMREAD_UNCHANGED)
    gray_tv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh_tv = cv2.threshold(gray_tv, 80, 255, 0)
    thresh_tv = cv2.erode(thresh_tv, kernel, iterations=1)
    tcontours, hierarchy = cv2.findContours(thresh_tv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt_perfect=0
    tcnt=0
    area = 0
    for c in tcontours:
        if cv2.contourArea(c) > area:
            tcnt = c
            area = cv2.contourArea(tcnt)
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image2 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    gray_perfect = cv2.cvtColor(perfect, cv2.COLOR_BGR2GRAY)
    ret, thresh_perfect = cv2.threshold(gray_perfect, 80, 255, 0)
    contours1, hierarchy1 = cv2.findContours(thresh_perfect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    parea = 0
    for c in contours1:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cy = int(M['m01'] / M['m00'])
            if cv2.contourArea(c) > parea:
                cnt_perfect = c
                parea = cv2.contourArea(c)

    x_t, y_t, w_t, h_t = cv2.boundingRect(tcnt)
    x_p, y_p, w_p, h_p = cv2.boundingRect(cnt_perfect)
    coef_y = h_t / h_p
    coef_x = w_t / w_p
    cnt_perfect[:, :, 0] = cnt_perfect[:, :, 0] * coef_x
    cnt_perfect[:, :, 1] = cnt_perfect[:, :, 1] * coef_y
    x_p, y_p, w_p, h_p = cv2.boundingRect(cnt_perfect)
    cv2.drawContours(blank_image1, [tcnt], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_perfect], -1, (255, 255, 255), -1 , offset=(x_t-x_p,y_t-y_p))
    shape_match = shapeMatch(blank_image1, blank_image2,cnt_perfect)
    a3 = f"shape matching= {shape_match}"
    arrayofString = []
    arrayofString.append(a3)
    return arrayofString, org