import os,shutil


def copyfile(fpath, srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!")%(srcfile)
    else:
        fpath, fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(srcfile,dstfile)
        print("copy %s -> %s")%( srcfile,dstfile)


def catch_polygon(row, col, bin_image):
    start_point = (row, col)
    flag = 'left2right'
    line_end = []
    moving_point = [row, col + 1]
    line_end.append([start_point[0], start_point[1]])
    while moving_point[0] != start_point[0] or moving_point[1] != start_point[1]:

        '''
        # the situation which width == 0:
        if bin_image[moving_point[0]][moving_point[1]] == 0:
            moving_point[0] += 1
            moving_point[1] -= 1
            flag = 'up'
        '''

        center = bin_image[moving_point[0]][moving_point[1]]
        right = bin_image[moving_point[0]][moving_point[1] + 1]
        right_down = bin_image[moving_point[0] - 1][moving_point[1] + 1]
        right_up = bin_image[moving_point[0] + 1][moving_point[1] + 1]
        left = bin_image[moving_point[0]][moving_point[1] - 1]
        left_down = bin_image[moving_point[0] - 1][moving_point[1] - 1]
        left_up = bin_image[moving_point[0] + 1][moving_point[1] - 1]
        up = bin_image[moving_point[0] + 1][moving_point[1]]
        down = bin_image[moving_point[0] - 1][moving_point[1]]

        # read the polygons:
        if flag == 'left2right':
            if right == 0 or (up == 1 and left_up == 0) or (down == 1 and left_down == 0):
                line_end.append([moving_point[0], moving_point[1]])
                if up == 1 and left_up != right_down:
                    flag = 'down2up'
                    moving_point[0] += 1
                else:
                    flag = 'up2down'
                    moving_point[0] -= 1
            else:
                moving_point[1] += 1
        elif flag == 'right2left':
            if left == 0 or (up == 1 and right_up == 0) or (down == 1 and right_down == 0):
                line_end.append([moving_point[0], moving_point[1]])
                if up == 1 and right_up != left_down:
                    flag = 'down2up'
                    moving_point[0] += 1
                else:
                    flag = 'up2down'
                    moving_point[0] -= 1
            else:
                moving_point[1] -= 1
        elif flag == 'down2up':
            if up == 0 or (right == 1 and right_down == 0) or (left == 1 and left_down == 0):
                line_end.append([moving_point[0], moving_point[1]])
                if left == 1 and right_up != left_down:
                    flag = 'right2left'
                    moving_point[1] -= 1
                else:
                    flag = 'left2right'
                    moving_point[1] += 1
            else:
                moving_point[0] += 1
        elif flag == 'up2down':
            if down == 0 or (right == 1 and right_up == 0) or (left == 1 and left_up == 0):
                line_end.append([moving_point[0], moving_point[1]])
                if left == 1 and left_up != right_down:
                    flag = 'right2left'
                    moving_point[1] -= 1
                else:
                    flag = 'left2right'
                    moving_point[1] += 1
            else:
                moving_point[0] -= 1

    # print(line_end)
    return line_end


def polygons_check(polygons, information='n'):
    authenticated = True
    line_ends = []
    # In every polygon：
    for i in polygons:

        for j in i:
            line_ends.append(j)

        # check the M1 Critical Dimension > 80
        for j in range(len(line_ends)):
            if j == len(line_ends) - 1:
                break
            else:
                if max(abs(line_ends[j + 1][0] - line_ends[j][0]), abs(line_ends[j + 1][1] - line_ends[j][1])) < 80:
                    authenticated = False
                    if information == 'y':
                        print('Dimension error')
                        print(max(abs(line_ends[j + 1][0] - line_ends[j][0]), abs(line_ends[j + 1][1] - line_ends[j][1])))

    # check the Tip to tip distance > 60
    for i in range(len(polygons)):
        for j in range(i + 1, len(polygons)):
            for k in polygons[i]:
                for l in polygons[j]:
                    if abs(k[0] - l[0]) + abs(k[1] - l[1]) < 60:
                        authenticated = False
                        if information == 'y':
                            print('Tip error')
                            print(abs(k[0] - l[0]) + abs(k[1] - l[1]))

    # check the pitch >140 (only the rectangles)
    rectangles = []
    horizontal = []
    vertical = []
    for i in polygons:
        if len(i) == 4:
            rectangles.append(i)
    for i in rectangles:
        if abs(i[0][0] - i[1][0]) > abs(i[0][1] - i[2][1]):
            i.append('horizontal')
            i.append(abs(i[0][1] - i[2][1])/2 + min(i[0][1], i[2][1]))
        else:
            i.append('vertical')
            i.append(abs(i[0][0] - i[1][0])/2 + min(i[0][0], i[1][0]))
    for i in rectangles:
        if i[4] == 'horizontal':
            horizontal.append(i)
        else:
            vertical.append(i)
    # print(vertical)
    # print(horizontal)
    for i in horizontal:
        i.append([min(i[0][0], i[1][0], i[2][0], i[3][0]), max(i[0][0], i[1][0], i[2][0], i[3][0])])
    for i in vertical:
        i.append([min(i[0][1], i[1][1], i[2][1], i[3][1]), max(i[0][1], i[1][1], i[2][1], i[3][1])])
    horizontal.sort(key=lambda x: x[6])
    horizontal.sort(key=lambda x: x[6])
    # 到此为止，数组的结构是[[[多边形点1],[多边形点2],[多边形点3],[多边形点4],[多边形方向],[多边形中线],[多边形最左最右或最低最高]]
    for i in range(len(horizontal)):
        for j in range(i + 1, len(horizontal)):
            if horizontal[j][6][1] > horizontal[i][6][0]:
                continue
            else:
                if i == len(horizontal) - 1:
                    break
                else:
                    if abs(horizontal[j][5] - horizontal[i][5]) < 140:
                        authenticated = False
                        if information == 'y':
                            print('Pitch error')
                            print(horizontal[j][5] - horizontal[i][5])
    for i in range(len(vertical)):
        for j in range(i + 1, len(vertical)):
            if vertical[j][6][1] > vertical[j][6][0]:
                continue
            else:
                if i == len(vertical) - 1:
                    break
                else:
                    if abs(vertical[i + 1][5] - vertical[i][5]) < 140:
                        authenticated = False
                        if information == 'y':
                            print('Pitch error')
                            print(vertical[i + 1][5] - vertical[i][5])

    return authenticated


def main():
    # the count of files
    txt_num = int(input('Input count of the files you hope to read which in [2, 5460]:'))
    information = input('If you need information about the error(y/n):')

    # to count the generated files
    count = 1

    # read the txt file
    for k in range(1, txt_num):
        with open('Mask_bin/M1_test' + str(k) + '.txt') as f:
            print('Reading the text "' + 'Mask_bin/M1_test' + str(k) + '.txt'+'"...(' + str(k) + '/' + str(txt_num - 1) +')')
            # transform the binary file to a array：
            bin_image = [[] for i in range(2048)]
            line = f.readlines()
            for i in range(2048):
                for j in line[i]:
                    if j == '0' or j == '1':
                        bin_image[i].append(int(j))
            # alter the base point form the left top to the left bottom:
            bin_image = bin_image[::-1]
            # check the every point：
            tips = []
            polygons = []
            # the point：[row][col]
            # erase the single point:
            for row in range(2048):
                for col in range(2048):

                    if row == 0 or row == 2047 or col == 0 or col == 2047:
                        continue

                    zero_point = 0

                    center = bin_image[row][col]
                    right = bin_image[row][col + 1]
                    right_down = bin_image[row - 1][col + 1]
                    right_up = bin_image[row + 1][col + 1]
                    left = bin_image[row][col - 1]
                    left_down = bin_image[row - 1][col - 1]
                    left_up = bin_image[row + 1][col - 1]
                    up = bin_image[row + 1][col]
                    down = bin_image[row - 1][col]

                    if center == 1:
                        if right == 0:
                            zero_point += 1
                        if left == 0:
                            zero_point += 1
                        if up == 0:
                            zero_point += 1
                        if down == 0:
                            zero_point += 1
                        if right_down == 0:
                            zero_point += 1
                        if right_up == 0:
                            zero_point += 1
                        if left_up == 0:
                            zero_point += 1
                        if left_down == 0:
                            zero_point += 1

                    if zero_point >= 6:
                        bin_image[row][col] = 0
                        print('erased [' + str(row) + '][' + str(col) + ']')

            for row in range(2048):
                for col in range(2048):

                    if row == 0 or row == 2047 or col == 0 or col == 2047:
                        continue

                    center = bin_image[row][col]
                    right = bin_image[row][col + 1]
                    right_down = bin_image[row - 1][col + 1]
                    right_up = bin_image[row + 1][col + 1]
                    left = bin_image[row][col - 1]
                    left_down = bin_image[row - 1][col - 1]
                    left_up = bin_image[row + 1][col - 1]
                    up = bin_image[row + 1][col]
                    down = bin_image[row - 1][col]

                    if center == 1 and right_down == 0 and left_down == 0 and left_up == 0 and [col, row] not in tips:
                        temp = catch_polygon(row, col, bin_image)
                        for i in temp:
                            i[0], i[1] = i[1], i[0]
                        tips += temp
                        polygons.append(temp)

            # recovery the binary image array:
            bin_image = bin_image[::-1]

            if polygons_check(polygons, information) == True:
                # shutil.copy('Mask_bin/M1_test' + str(k) + '.txt', 'certed_bin/M1_test' + str(k) + '.txt')
                with open('certed_bin/' + str(count) + '.txt', 'w') as f:
                    for i in bin_image:
                        for j in i:
                            f.write(str(j) + ' ')
                        f.write('\n')
                count += 1
                print('certed_bin/' + str(count) + '.txt, finished.')


if __name__ == '__main__':
    main()



