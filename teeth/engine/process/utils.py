import cv2
import numpy as np
from django.conf import settings
import os

kernel = np.ones((5, 5), np.uint8)

PERFECTS = {
    "buccal": {
        "premandibular": cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/buccal-perfect-premandibular.jpg"), cv2.IMREAD_UNCHANGED),
        "central": cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/buccal-perfect-central.jpeg"), cv2.IMREAD_UNCHANGED)
    },
    "distal": {
        "premandibular": cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/distal-perfect-premandibular.jpg"), cv2.IMREAD_UNCHANGED),
        "central": cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/distal-perfect-central.jpeg"), cv2.IMREAD_UNCHANGED)
    },
    "mesial": {
        "premandibular": cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/mesial-perfect-premandibular.jpg"), cv2.IMREAD_UNCHANGED),
        "central":  cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/mesial-perfect-central.jpeg"), cv2.IMREAD_UNCHANGED)
    },
    "lingual": {
        "premandibular":  cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/lingual-perfect-premandibular.jpeg"), cv2.IMREAD_UNCHANGED),
        "central": cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/lingual-perfect-central.jpeg"), cv2.IMREAD_UNCHANGED)
    },
    "top_view": {
        "premandibular": cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/top_view-perfect-premandibular.jpg"), cv2.IMREAD_UNCHANGED),
        "central": cv2.imread(os.path.join(settings.STATIC_ROOT, f"engine/top_view-perfect-central.jpeg"), cv2.IMREAD_UNCHANGED)
    }
}

kernel = np.ones((5, 5), np.uint8)

def shapeMatch(img1 , img2 , cntImg2):
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
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
    return cv2.contourArea(cnt_inter)/cv2.contourArea(cnt_union)

def find_rubber(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50], np.uint8)
    upper_blue = np.array([140, 255, 255], np.uint8)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue = cv2.bitwise_and(img, img, mask=mask)
    blue = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
    get, bthresh = cv2.threshold(blue, 70, 255, 0)
    bthresh = cv2.dilate(bthresh, kernel, iterations=1)
    bcontours, hierarchy = cv2.findContours(bthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for c in bcontours:
        if cv2.contourArea(c) > area:
            gcnt = c
            area = cv2.contourArea(gcnt)
    mask_inv = cv2.bitwise_not(mask)
    return gcnt, mask_inv


def find_base(contours, rubber_bottom):
    barea = 0
    cnt_base = contours[0]
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
