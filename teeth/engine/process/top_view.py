import cv2
import numpy as np
from .utils import *

def top_view(img, type):
    perfect = PERFECTS["top_view", type]
    org = img
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
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(blank_image, [tcnt], -1, (255, 255, 255), -1)
    cv2.drawContours(blank_image, [cnt_perfect], -1, (255, 255, 255), -1, offset=(x_t - x_p, y_t - y_p))
    shape_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(shape_img, [tcnt], -1, (0, 0, 139), -1)
    cv2.drawContours(shape_img, [cnt_perfect], -1, (139, 0, 0), 10, offset=(x_t - x_p, y_t - y_p))
    shape_match= shapeMatch(blank_image1, blank_image2, tcnt,cnt_perfect)
    a3 = f"shape matching= {shape_match}"
    arrayofString = []
    arrayofString.append(a3)
    return arrayofString, org,shape_img
