
from matplotlib import pyplot as plt
import numpy as np
import cv2
import os

# def devide_cell2(img):
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(1,1))
#     img2 = clahe.apply(img)
#
#     ret,thresh = cv2.threshold(img2,127,255,cv2.THRESH_BINARY_INV)
#
#    # adaptiveThreshold
#
#     # cv2.imshow("thresh", thresh)
#     # cv2.waitKey()
#     # cv2.destroyAllWindows()



def devide_cell(img):
    if os.path.exists("../cell_data"):
        pass
    else:
        os.makedirs("../cell_data")
    cell = []
    tmp_circle_cell = []
    tmp_cell = []
    img_copy = img.copy()
    width = img.shape[0]
    height = img.shape[1]
    width = width/9
    height = height/9
    for i in range(10):
        for j in range(10):

            tmp_circle_cell.append((int(j * width),int(i * height)))
            tmp_cell.append([int(j * width),int(i * height)])
            img_copy = cv2.circle(img_copy,tmp_circle_cell[j],4,(0,0,255),-1)

        # print(tmp_cell)


        cell.append(tmp_cell)
        tmp_circle_cell = []
        tmp_cell = []


    for i in range(9):
        for j in range(9):

            img2 = img[int(cell[i][j][0]+(50*0.05)):int(cell[i][j][0]+(50*0.95)), int(cell[i][j][1]+(50*0.05)):int(cell[i][j][1]+(50*0.95))]
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY_INV)

            thresh_copy = thresh.copy()
            kernel = np.ones((3, 3), np.uint8)
            thresh = cv2.dilate(thresh, kernel, iterations=1)

            cnt, hr = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



            max_area = 0
            index = 0

            for c in range(len(cnt)):
                area = cv2.contourArea(cnt[c])
                # print(area)
                if area > 100:
                    if area > max_area:
                        max_area = area
                        index = c


                for k in range(len(cnt)):
                    if k == c:
                        None
                    else:
                        thresh = cv2.drawContours(thresh, cnt, k, 255, -1)



            if max_area >100:
                mom = cv2.moments(cnt[index])
                (x, y) = int(mom['m10'] / mom['m00']), int(mom['m01'] / mom['m00'])

                cv2.drawContours(thresh, cnt, index, 0, -1)
                img2 = cv2.bitwise_xor(thresh, thresh_copy)
                kernel = np.ones((2, 2), np.uint8)
                img2 = cv2.erode(img2, kernel, iterations=1)


                M = np.float32([[1,0,(img2.shape[0]/2-2)-x],[0,1,(img2.shape[1]/2-2)-y]])
                img2 = cv2.warpAffine(img2, M, (img2.shape[0],img2.shape[1]))
                img2 = ~img2
                # cv2.imshow("img2", img2)
                # cv2.waitKey()
                # cv2.destroyAllWindows()

                cv2.imwrite("../cell_data/cell_%d_%d.png" % (j, i), img2)

    print("저장완료")
    # cv2.imshow("img_copy", img_copy)
    #
    #
    # cv2.waitKey()
    # cv2.destroyAllWindows()


def sudoku_v1(ori_img):

    img=cv2.imread(ori_img,1)
    cv2.imshow("original", img)
    cv2.waitKey()
    ####################################이미지 톤 및 노이즈 제거########################################
    img=cv2.GaussianBlur(img,(3,3),0)           #가우시안블러
    frame=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)) #커널생성
    close=cv2.morphologyEx(frame,cv2.MORPH_CLOSE,kernel)#open: erosion -> dialation close:ersion ->dialation
    # cv2.imshow("morclose",close)
    div=np.float32(frame)/(close) #그레이 컬러로 바꾼 이미지를 close로 처리한 이미지로 나눔
    # cv2.imshow("frame",frame)
    # cv2.imshow("div",div)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    #가우시안 -> cvtcolor(bgr2gray) ->(frame)
    #                                                   ----->  div = frame / close       (div생성)
    #커널생성 -> (frame)morphologyEx(close) ->(close)
    #################################################################################################



    res=np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX)) #이미지 정규화 실수타입의 div를 정규화시킨후 uint8(0~255)로 변환
    res2=cv2.cvtColor(res,cv2.COLOR_GRAY2BGR)
    plt.imshow(res2)
    plt.title("res2")
    plt.xticks([0,100,200,300,400,500])
    plt.yticks([])
    plt.show()

    #보통 이진화를 처리할때 영상 전체에서 화소 값을 이용하여 이진화를 한다면
    # adaptive threshold는 영상을 구역으로 나누어 각각 이진화를 처리한다
    ####
    #V_ADAPTIVE_THRESH_MEAN_C 는  주변 픽셀의 가중치가 모두 동일하게 지정되며
    #CV_ADAPTIVE_THRESH_GAUSSIAN_C 는 가중치가 가우시안 형태로 지정되며,
    # 중심 쪽 픽셀 값의 가중치가 높게 부여된다.


    thresh=cv2.adaptiveThreshold(res,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    #tempthresh=cv2.resize(thresh,(450,450))
    # cv2.imshow("thresh",thresh)
    # cv2.waitKey()
    # cv2.destroyAllWindows()


    cnt,hr = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # keys = [i for i in range(48,58)] #제거해도 됨
    area=0
    temparea=0
    p=0 #cnt의 인자값저장
    bestapprox=None
    for i in range(len(cnt)):
        temparea=cv2.contourArea(cnt[i])
        if temparea>1000:
            peri=cv2.arcLength(cnt[i],True) #둘레길이 true:폐곡선 false : 열린호
            epsilon=0.05*peri
            approx=cv2.approxPolyDP(cnt[i],epsilon,True) #근사화 함수 #반환 꼭지점
            if len(approx)==4 and temparea>area:
                area=temparea
                bestapprox=approx
                p=i



    img=cv2.polylines(img,[bestapprox],True,(0,255,0),3)#폐곡선 꼭지점에 라인을 연결
    cv2.drawContours(img,cnt,p,(255,0,0),2) #폐곡선 라인을 검출
    # cv2.imshow("img",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    (x,y)=thresh.shape
    mask=np.zeros((x,y),np.uint8)

    mask=cv2.drawContours(mask,cnt,p,255,-1) # cnt 내부를 채우기
    # cv2.imshow('mask1',mask)
    mask=cv2.drawContours(mask,cnt,p,0,2) # cnt 외각선을 검은색으로 제거
    # cv2.imshow('mask2',mask)
    masked=cv2.bitwise_and(mask,res) # cnt에서 검출한 sudoku와 이미지에서 공통된부분 도출
    # cv2.imshow("masked",masked)
    # cv2.waitKey(0)

    kernelx = cv2.getStructuringElement(cv2.MORPH_RECT,(2,10)) #x 커널
    dx = cv2.Sobel(masked,cv2.CV_16S,1,0) #1,0 은 x 수직방향 에지 검출 // CV_16S : 16-bit signed integer: short ( -32768..32767 )
    dx = cv2.convertScaleAbs(dx) #convertscaleAbs를 이용하여 소벨 결과에 절대값 적용하고 범위를 8비트로 변경
    cv2.normalize(dx,dx,0,255,cv2.NORM_MINMAX)
    # cv2.imshow("dx1",dx)
    ret,close = cv2.threshold(dx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # cv2.imshow("dx2",close)
    close = cv2.morphologyEx(close,cv2.MORPH_DILATE,kernelx,iterations = 1)
    # cv2.imshow("dx3",close)

    contour, hr = cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        x,y,w,h = cv2.boundingRect(cnt)
        if h/w > 5:
            cv2.drawContours(close,[cnt],0,255,-1) #contours boundingrect에서 h/w가 5이상인 사각형을 칠함
        else:
            cv2.drawContours(close,[cnt],0,0,-1)
    close = cv2.morphologyEx(close,cv2.MORPH_CLOSE,None,iterations = 2)
    closex = close.copy()
    # cv2.imshow("closex",closex)

    kernely=cv2.getStructuringElement(cv2.MORPH_RECT,(10,2)) #y 커널
    dy=cv2.Sobel(masked,cv2.CV_16S,0,2) #0,2는 y 수평방향 검출
    dy=cv2.convertScaleAbs(dy)

    cv2.normalize(dy,dy,0,255,cv2.NORM_MINMAX)
    ret,close=cv2.threshold(dy,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    close=cv2.morphologyEx(close,cv2.MORPH_DILATE,kernely,iterations=1)
    cnt, hier = cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(cnt)):
        x,y,w,h = cv2.boundingRect(cnt[i])
        if w/h > 5:
            cv2.drawContours(close,cnt,i,255,-1)
        else:
            cv2.drawContours(close,cnt,i,0,-1)
    close = cv2.morphologyEx(close,cv2.MORPH_CLOSE,None,iterations = 2)
    closey=close
    # cv2.imshow("closey",closey)
    grid=cv2.bitwise_and(closex,closey)
    # cv2.imshow("grid",grid)


    ############################소벨xy를 이용하여 겹치는 부분을 표시 ##########################
    ########################################################################################



    contour, hier = cv2.findContours(grid,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cent=[]
    for cnt in contour:
         mom=cv2.moments(cnt)
         (x,y)=int(mom['m10']/mom['m00']),int(mom['m01']/mom['m00'])
         cent.append((x,y))
         cv2.circle(img,(x,y),4,(0,255,0),-1)
         # print("mom", mom)
    # print("cent",cent)
    # cv2.imshow("img", img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    ce=np.array(cent,np.uint32)
    ce=ce.reshape((100,2))
    ###################cent 정렬############################
    ce2=ce[np.argsort(ce[:,1])]
    #print ce2
    b = np.vstack([ce2[i*10:(i+1)*10][np.argsort(ce2[i*10:(i+1)*10,0])] for i in range(10)])
    #print b
    points = b.reshape((10,10,2))
    # print("points",points)
    output=np.zeros((450,450,3),np.uint8)
    #print(points)
    points_cpy = points
    for i in range(3):
        for j in range(3):
            partimg=np.array([points[i*3,j*3,:],points[(i)*3,(j+1)*3,:],points[(i+1)*3,(j+1)*3,:],points[(i+1)*3,j*3,:]],np.float32)
            # print(partimg)
            dest=np.array([[j*150,i*150],[(j+1)*150,(i)*150],[(j+1)*150,(i+1)*150],[(j)*150,(i+1)*150]],np.float32)
            gpres=cv2.getPerspectiveTransform(partimg,dest)
            warp=cv2.warpPerspective(res2,gpres,(450,450))
            output[i*150:(i+1)*150,j*150:(j+1)*150]=warp[i*150:(i+1)*150,j*150:(j+1)*150]
            # cv2.imshow("output", output)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
    cv2.rectangle(output,(0,0),(450,450),0,1)
    # cv2.imshow("output",output)
    # cv2.waitKey()
    # cv2.destroyAllWindows()


    # devide_cell(output)
    # devide_cell2(output)
    cell = devide_cell(output)
    return points_cpy
   # cv2.imwrite('../images/output.png', output)



