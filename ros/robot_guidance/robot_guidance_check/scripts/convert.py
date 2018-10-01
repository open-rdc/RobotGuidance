#!/usr/bin/env python
from __future__ import print_function
import csv
import chainer.functions as F
import numpy as np
from chainer import Variable

src_file = '/home/mirai/data.txt'
dst_file = '/home/mirai/data.csv'

if __name__ == '__main__':
    data = [[0 for x in range(11)] for y in range(11)]
    sf = open(src_file, 'r')
    df = open(dst_file, 'a')
    reader = csv.reader(sf)
    writer = csv.writer(df)
    i = 0
    while True:
        i = i + 1
        for y in range(11):
            for x in range(11):
                raw_data = reader.next()
                if float(raw_data[2]) == 0 and float(raw_data[3]) == 0 and float(raw_data[4]) == 0 and float(raw_data[5]) == 0:
                    data[y][x] = [0, 0, 0, 0]
                    continue
                raw_data_list = np.array([[float(raw_data[2]), float(raw_data[3]), float(raw_data[4]), float(raw_data[5])]], np.float32)
                sdata = F.softmax(raw_data_list)
                data[y][x] = sdata.data[0]

        writer.writerow([i, 0])
        writer.writerow(["", 1,2,3,4,5,6,7,8,9,10,11])
        for y in range(11):
            writer.writerow([y,data[y][0][0],data[y][1][0],data[y][2][0],data[y][3][0],data[y][4][0],data[y][5][0],data[y][6][0],data[y][7][0],data[y][8][0],data[y][9][0],data[y][10][0]])

        writer.writerow([i, 1])
        writer.writerow(["", 1,2,3,4,5,6,7,8,9,10,11])
        for y in range(11):
            writer.writerow([y,data[y][0][1],data[y][1][1],data[y][2][1],data[y][3][1],data[y][4][1],data[y][5][1],data[y][6][1],data[y][7][1],data[y][8][1],data[y][9][1],data[y][10][1]])

        writer.writerow([i, 2])
        writer.writerow(["", 1,2,3,4,5,6,7,8,9,10,11])
        for y in range(11):
            writer.writerow([y,data[y][0][2],data[y][1][2],data[y][2][2],data[y][3][2],data[y][4][2],data[y][5][2],data[y][6][2],data[y][7][2],data[y][8][2],data[y][9][2],data[y][10][2]])

        writer.writerow([i, 3])
        writer.writerow(["", 1,2,3,4,5,6,7,8,9,10,11])
        for y in range(11):
            writer.writerow([y,data[y][0][3],data[y][1][3],data[y][2][3],data[y][3][3],data[y][4][3],data[y][5][3],data[y][6][3],data[y][7][3],data[y][8][3],data[y][9][3],data[y][10][3]])

