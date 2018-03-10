# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import ipdb
from django.conf import settings
from quickstart.matched import get_matched
import json

class Contour(object):
    def __init__(self, x, cnt):
        self.x = x
        self.cnt = cnt

matched = get_matched()
def calculate_point(filename, name, ANSWER_KEY = []):
    # # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    #     help="path to the input image")
    # args = vars(ap.parse_args())

    # define the answer key which maps the question number
    # to the correct answer
    

    # load the image, convert it to grayscale, blur it
    # slightly, then find edges
    image = cv2.imread('{}/media/{}'.format(settings.BASE_DIR, filename))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    print('step 1')
    # find contours in the edge map, then initialize
    # the contour that corresponds to the document
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    docCnt = None
    print('step 2')
    # ensure that at least one contour was found
    if len(cnts) > 0:
    	# sort the contours according to their size in
    	# descending order
    	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        print('step 3')
    	# loop over the sorted contours
    	round = 0
    	for c in cnts:
    		# approximate the contour
    		peri = cv2.arcLength(c, True)
    		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    		# if our approximated contour has four points,
    		# then we can assume we have found the paper
    		if len(approx) == 4:
    			docCnt = approx

    			(x, y, w, h) = cv2.boundingRect(cnts[round + 1])

    			if w < 200:
    				break
    			round = round + 1

    print('step 4')
    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper
    paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))
    correct_paper = four_point_transform(image, docCnt.reshape(4, 2))
    print('step 5')
    # apply Otsu's thresholding method to binarize the warped
    # piece of paper
    thresh = cv2.threshold(warped, 0, 255,
    	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # store mask and bird view paper
    cv2.imwrite('media/mask/{}-bird.png'.format(name), paper)
    cv2.imwrite('media/mask/{}-mask.png'.format(name), thresh)


    # find contours in the thresholded image, then initialize
    # the list of contours that correspond to questions
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    questionCnts = []
    print('step 6')
    # loop over the contours
    count = 0
    color = (0, 255, 0)
    for c in cnts:
    	# compute the bounding box of the contour, then use the
    	# bounding box to derive the aspect ratio
    	(x, y, w, h) = cv2.boundingRect(c)
    	ar = w / float(h)

    	# in order to label the contour as a question, region
    	# should be sufficiently wide, sufficiently tall, and
    	# have an aspect ratio approximately equal to 1
        if w >= 15 and h >= 15 and w <= 40 and h <= 40:
            # if count >= 480 and count < 500:
            cv2.drawContours(paper, [c], -1, color, 3)
            questionCnts.append(Contour(y, c))
            count = count +1

    def sort_by_x(countour):
        return countour.x

    questionCnts = sorted(questionCnts, key=sort_by_x, reverse=False)
    questionCnts = [c.cnt for c in questionCnts]
    cv2.imwrite('media/mask/{}-circle.png'.format(name), paper)
    #
    # # sort the question contours top-to-bottom, then initialize
    # # the total number of correct answers
    # # questionCnts = contours.sort_contours(questionCnts,
    # # 	method="top-to-bottom")[0]
    print('step 7')
    correct = 0
    print(len(questionCnts))
    if(len(questionCnts) != 500):
        raise ValueError('Wrong number of answer.')
    # each question has 5 possible answers, to loop over the
    # question in batches of 5

    for (q, i) in enumerate(np.arange(0, len(ANSWER_KEY), 1)):
    	# draw the outline of the correct answer on the test
    	# sort the contours for the current question from
    	# left to right, then initialize the index of the
    	# bubbled answer
    	start = matched[str(i+1)]['start']
        no = i+1
        rownum = 0
        startInRow = 0
        if no >= 1 and no <= 25:
            rownum = start
            startInRow = 0
        elif no >= 26 and no <= 50:
            rownum = start - 5
            startInRow = 5
        elif no >= 51 and no <= 75:
            rownum = start - 10
            startInRow = 10
        elif no >= 76 and no <= 100:
            rownum = start - 15
            startInRow = 15
        cnts = []
        rowCnts = questionCnts[rownum: rownum + 20]
        for c in rowCnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cnts.append(Contour(x, c))

        cnts = sorted(cnts, key=sort_by_x, reverse=False)
        cnts = cnts[startInRow: startInRow + 5]
        cnts = [c.cnt for c in cnts]
        # for c in cnts:
        #     cv2.drawContours(paper, [c], -1, color, 3)
        # cv2.imwrite('media/mask/{}-answer.png'.format(name), paper)

    	bubbled = None
    	color = (0, 0, 255)
        # # loop over the sorted contours
    	for (j, c) in enumerate(cnts):

    		# construct a mask that reveals only the current
    		# "bubble" for the question
    		mask = np.zeros(thresh.shape, dtype="uint8")
    		cv2.drawContours(mask, [c], -1, 255, -1)

    		# apply the mask to the thresholded image, then
    		# count the number of non-zero pixels in the
    		# bubble area
    		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
    		total = cv2.countNonZero(mask)

    		# if the current total has a larger number of total
    		# non-zero pixels, then we are examining the currently
    		# bubbled-in answer
    		if bubbled is None or total > bubbled[0]:
    			bubbled = (total, j + 1)

        # initialize the contour color and the index of the
    	# *correct* answer
    	k = ANSWER_KEY[q]['correct']

        color = (0, 0, 255)
    	if k == str(bubbled[1]):
            color = (0, 255, 0)
            correct += 1
        cv2.drawContours(correct_paper, [cnts[bubbled[1]-1]], -1, color, 3)

    cv2.imwrite('media/mask/{}-answer.png'.format(name), correct_paper)
    print('step 8')
    return correct
