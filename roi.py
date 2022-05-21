import cv2


def roi(imagein):
    image0 = cv2.imread("well.jpg")
    gray0 = cv2.cvtColor(image0, cv2.COLOR_BGR2GRAY)
    template = gray0[50:220, 115:230]
    h, w = template.shape[0:2]

    image1 = imagein
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

    methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]
    for md in methods:
        result = cv2.matchTemplate(gray1, template, md)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if md == cv2.TM_SQDIFF_NORMED:
            tl = min_loc
        else:
            tl = max_loc
    br = (tl[0] + w, tl[1] + h)

    image2 = image1[tl[1]:br[1], tl[0]:br[0]]
    return (image2, tl, br)
