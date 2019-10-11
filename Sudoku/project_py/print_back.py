
import cv2
import numpy as np
import shutil

def blend_non_transparent(face_img, overlay_img):
    # Let's find a mask covering all the non-black (foreground) pixels
    # NB: We need to do this on grayscale version of the image
    gray_overlay = cv2.cvtColor(overlay_img, cv2.COLOR_BGR2GRAY)
    overlay_mask = cv2.threshold(gray_overlay, 1, 255, cv2.THRESH_BINARY)[1]

    # Let's shrink and blur it a little to make the transitions smoother...
    overlay_mask = cv2.erode(overlay_mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    overlay_mask = cv2.blur(overlay_mask, (3, 3))

    # And the inverse mask, that covers all the black (background) pixels
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

# ==============================================================================

def print_back(path, coords, answers):

    num2img_dict = {}
    #출력할 숫자 이미지 불러오기
    for i in range(1, 10):
        num_img = cv2.imread('../numbers/' + str(i) + '.png', 1)
        num2img_dict[i] = num_img

    print('coords:', coords)
    # print('answers:', answers)

    # for x in num2img_dict.values():
    #     cv2.imshow('aa', x)
    #     cv2.waitKey()
    #원본 이미지 불러오기
    image = cv2.imread(path)

    for i in range(0, len(answers)):
        for j in range(0, len(answers[0])):
            num = int(answers[i][j])
            if num != 0:
                # print()
                #print(coords[i][j])
                # print(coords[i + 1][j + 1])

                cell_start = coords[i][j]
                cell_end = coords[i+1][j+1]

                list_a = [cell_start[1],cell_end[1], cell_start[0],cell_end[0]]

                roi = image[cell_start[1]:cell_end[1], cell_start[0]:cell_end[0]]

                # cv2.imshow('aa', num2img_dict[num])
                # cv2.waitKey()

                h, w, depth = roi.shape

                dst = cv2.resize(num2img_dict[num], (w, h), interpolation=cv2.INTER_NEAREST)

                result_1 = blend_non_transparent(roi, dst)
                image[cell_start[1]:cell_end[1], cell_start[0]:cell_end[0]] = result_1

    cv2.imshow("result", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    shutil.rmtree("../cell_data")