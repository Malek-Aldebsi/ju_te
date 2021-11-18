import cv2
import numpy as np
from .utils import *

def lingual(img, type):
    perfect = PERFECTS["lingual"][type]
    org = img
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(gray_img, 70, 255, 0)
    gcnt, mask = find_rubber(img)
    thresh_img = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
    thresh_img = cv2.erode(thresh_img, kernel, iterations=1)
    rubber_bootom = tuple(gcnt[gcnt[:, :, 1].argmax()][0])
    rubber_top = tuple(gcnt[gcnt[:, :, 1].argmin()][0])
    cv2.line(thresh_img, (-100000000, rubber_top[1]), (100000000, rubber_top[1]), (0, 255, 0), thickness=5)
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
    cv2.putText(org, "l4", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (70, 0, 200), 2)
    cv2.line(org, (1000000, int(vy - (((14) * pix_for_mm)))), (-1000000, int(vy - ((14) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((14) * pix_for_mm))
    cv2.putText(org, "l3", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (70, 0, 200), 2)
    cv2.line(org, (1000000, int(vy - (((14) * pix_for_mm)))), (-1000000, int(vy - ((14) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    vy = int(vy - ((14) * pix_for_mm))
    cv2.putText(org, "l2", (vy, vy), cv2.FONT_HERSHEY_SIMPLEX, 1, (70, 0, 200), 2)
    cv2.line(org, (1000000, int(vy - (((14) * pix_for_mm)))), (-1000000, int(vy - ((14) * pix_for_mm))), (0, 255, 0),
             thickness=int(pix_for_mm))
    line1 = int(vy - ((14) * pix_for_mm))
    cv2.putText(org, "l1", (line1, line1), cv2.FONT_HERSHEY_SIMPLEX, 1, (70, 0, 200), 2)
    cv2.circle(org, tuple(extLeft_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extTop_tooth), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointl), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointr), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extRight_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(extLeft_base), 4, (0, 0, 255), -1)
    cv2.circle(org, tuple(cervix_pointl), 4, (0, 0, 255), -1)
    cnt_red = find_red(img)
    subTop_tooth = tuple(cnt_red[cnt_red[:, :, 1].argmin()][0])
    cv2.circle(org, subTop_tooth, 4, (0, 0, 255), -1)
    cv2.putText(org, "5", (cervix_pointl[0] + 5, cervix_pointl[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0),
                2)
    cv2.putText(org, "6", (cervix_pointr[0] + 5, cervix_pointr[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0),
                2)
    cv2.putText(org, "2", (subTop_tooth[0] + 5, subTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0),
                2)
    cv2.putText(org, "1", (extTop_tooth[0] + 5, extTop_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0),
                2)
    cv2.putText(org, "4", (extLeft_tooth[0] + 5, extLeft_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0),
                2)
    cv2.putText(org, "3", (extRight_tooth[0] + 5, extRight_tooth[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 2,
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
    x_p, y_p, w_p, h_p = cv2.boundingRect(cnt_perfect)
    cv2.drawContours(blank_image1, [cnt_tooth], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image2, [cnt_perfect], -1, (255, 255, 255), -1, offset=(x_t-x_p, y_t-y_p))
    shape_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(shape_img, [cnt_tooth], -1, (255, 255, 255), -1)
    cv2.drawContours(shape_img, [cnt_perfect], -1, (0, 0, 139), 10, offset=(x_t-x_p, y_t-y_p))
    shape_match = shapeMatch(blank_image1, blank_image2, cnt_perfect)
    a10 = f"shape matching= {shape_match}"
    arrayofString.append(a10)
    scale_percent = 80
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    org = cv2.resize(org, dim, interpolation=cv2.INTER_AREA)

    return arrayofString, org, shape_img#,(rubber_bootom[1] - extTop_tooth[1]) / pix_for_mm]
