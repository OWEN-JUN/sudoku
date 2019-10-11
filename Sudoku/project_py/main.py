import use_mnist as keras_v1
import sudoku_v1 as v1
import print_back as pb
import sudoku_solver as sv

path = "../images/sudoku4.jpg"
print('####스도쿠 이미지 처리####')
coords = v1.sudoku_v1(path)

print()

print('####숫자 이미지 예측####')
pred_9x9 = keras_v1.predict()
print(pred_9x9)

print()

print('####스도쿠 알고리즘####')
answers = sv.sudoku_pro(pred_9x9)
print("answer:",answers)

print()

print('####이미지 정답 출력 알고리즘####')
pb.print_back(path, coords, answers)

print("프로그램 종료")




