import numpy as np
import json

class Analysis():
    def __init__(self, sudoku, type_, num):
        self.sudoku = sudoku
        self.type_ = type_
        self.num = num

    def analysis(self):
        print("Type:{} Num:{}".format(self.type_, self.num))
        if self.type_ == 'r':
            print("{} {} {} | {} {} {} | {} {} {}".format(*self.sudoku.arr[self.num]))
        if self.type_ == 'c':
            print("{} {} {} | {} {} {} | {} {} {}".format(*self.sudoku.arr[:, self.num]))
        print()

class Sudoku():

    def __init__(self, quizzes):
        self.analysis = np.zeros((9, 9, 9), int)
        self.sudoku = np.zeros((9, 9), int)
        self.to_be_filled = []
        for r in range(9):
            for c in range(9):
                self.analysis[r, c] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for n in range(len(quizzes)):
            num = int(quizzes[n]) # 数字提取
            r = int(n / 9) # 行下标
            c = n % 9 # 列下标
            if num != 0:
                self.to_be_filled.append((r, c, num))

    def print(self):
        # 草稿纸信息
        # print("-----草稿纸信息-----")
        # for i in range(9):
        #     print(self.analysis[:, :, i])

        # 答题Sudoku信息
        print("---答题Sudoku信息---")
        for i in range(9):
            print("{} {} {} | {} {} {} | {} {} {}".format(*self.sudoku[i]).replace("0", " "))
            if i < 6 and (i + 1) % 3 == 0:
                print("----- ~ ----- ~ -----")

    def processing(self):
        while len(self.to_be_filled) > 0:
            r, c, num = self.to_be_filled.pop(0)
            self.analysis[:, c, num - 1] = 0 # 同一列格子刪除此數
            self.analysis[r, :, num - 1] = 0 # 同一行格子刪除此數
            self.analysis[r, c, :] = 0 # 同一格子删除其他可能的數
            self.analysis[r - r % 3:r - r % 3 + 3, c - c % 3:c - c % 3 + 3, num - 1] = 0# 同一九宫格删除此数
            self.sudoku[r, c] = num # 填入此格子的数

    def find(self):
        for num in range(9):
            for a in range(9):
                row_num = self.analysis[a, :, num]
                if len(row_num[row_num == num + 1]) == 1:
                    for b in range(9):
                        if row_num[b] == num + 1:
                            self.to_be_filled.append((a, b, num + 1))
                col_num = self.analysis[:, a, num]
                if len(col_num[col_num == num + 1]) == 1:
                    for b in range(9):
                        if col_num[b] == num + 1:
                            self.to_be_filled.append((b, a, num + 1))
        for r in range(9):
            for c in range(9):
                cell_num = self.analysis[r, c, :]
                if len(cell_num[cell_num == 0]) == 8:
                    for num in cell_num:
                        if num != 0:
                            self.to_be_filled.append((r, c, num))

    def resolve(self):
        while len(self.to_be_filled) > 0:
            self.processing()
            self.find()
        return ''.join(str(c) for c in self.sudoku.reshape(-1))

if __name__ == '__main__':
    with open("./data/sudoku.csv", "r") as fr, open("./data/result.csv", "w") as fw:
        line_num = 0
        for line in fr:
            line_num += 1
            quizzes, solutions = line.split(",")
            if quizzes != "quizzes":
                sudoku = Sudoku(quizzes)
                solutions = sudoku.resolve()
                if "0" in solutions:
                    sudoku.print()
                fw.write("{},{}\n".format(quizzes,solutions))
            else:
                fw.write("{},{}\n".format("quizzes","solutions"))
