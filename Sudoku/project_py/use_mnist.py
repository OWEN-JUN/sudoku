from keras.models import load_model
model = load_model("../models/mnist_0.h5")
# import warnings
# warnings.filterwarnings('ignore',category=DeprecationWarning)

import numpy as np

#import matplotlib.pyplot as plt

def set_image():

    import sys
    import cv2
    import glob

    path = '../cell_data\\'
    images = glob.glob(path + '*.png')

    fnames = []

    if len(images) == 0:
        print("no such directory")
        sys.exit()

    results = []
    pixel_size = 28
    cnt = 0

    for image in images:

        fname = str(image)
        fname = fname.replace(path+'cell', '')
        fname = fname.replace('.png', '')
        fname = fname.replace('_', '')
        fnames.append(fname)

        image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(255 - image, (28, 28))
        image = image.reshape(1, 28, 28, 1)
        image = image.astype('float32')
        image /= 255

        # weight = 0.5
        # for i in range(0, pixel_size):
        #      for j in range(0, pixel_size):
        #          if image[0][i][j] < weight:
        #             image[0][i][j] = 0.0
        #
        #          elif image[0][i][j] >= weight:
        #             image[0][i][j] = 1.0

        results.append(image)

    return results, fnames

def get_accuracy(probs):

    #probability 값을 hot encoding 으로 받고 스트링으로 바꿔준다.
    str_a = np.array2string(probs, precision=2, separator=" ")

    #스트링의 필요없는 부분 제거
    str_a = str_a.replace("[", "")
    str_a = str_a.replace("]", "")

    # 10개의 숫자로 나눈다.
    x = str_a.split()


    # 제일 높은 정확도를 가진 숫자를 찾고 퍼센트로 바꾼다.
    highest_acc = 0.0
    for i in range(len(x)):
        if highest_acc < float(x[i]):
            highest_acc = float(x[i])

    accuracy = int(highest_acc * 100)

    return accuracy



def dict2sudoku(answer_dict):

    num_in_rows = [] #9개의 0이 채워질 리스트
    predict = [] #딕셔너리에서 정답들만 뽑아올 자리

    # 9 x 9 의 스도쿠 판을 만든다
    for i in range(0,9):
        num_in_rows.append(list('000000000'))

    # 딕셔너리에서 정답들을 뽑아온다
    for answer in answer_dict.values():
        predict.append(answer)

    cnt = 0 #딕셔너리에서 좌표들로 스도쿠 판에 집어넣는다.
    for coords in answer_dict:
        num_in_rows[int(coords[0])][int(coords[1])] = str(predict[cnt])
        cnt += 1

    strings = []
    for row in num_in_rows:
        string = ''
        for number in row:
            string += number
        strings.append(string)


    return strings




def predict():

    #   이미지를 불러오고 인식을 위한 처리
    images, fnames = set_image()

    #   딥러닝 모델로 숫자 예측
    answers = []
    for img in images:
        prediction = model.predict(img)

        #accuracy = get_accuracy(prediction)
        answers.append(np.argmax(prediction))

    answer_dic = {}
    for i in range(0, len(answers)):
        answer_dic[fnames[i]] = answers[i]

    # #print(answer_dic)
    # if wrong_cnt == 0:
    #     print("every predictions correct!")
    # else:
    #     print("wrong predictions:", wrong_cnt)


    string = dict2sudoku(answer_dic)
    return string

#predict()