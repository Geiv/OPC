from PIL import Image, ImageDraw
# 规定2048 x 2048画纸:
width = 2048
height = 2048

# 最大为5460：
txt_num = int(input('输入读取txt的数量,最大为5460，最小为2:'))

for k in range(1, txt_num):
    image = Image.new('RGB', (width, height), (255, 255, 255))
    small_bin_image = [[] for i in range(1200)]
    bin_image = [[] for i in range(2048)]
    # read the bin.txt:
    with open('train/ac' + str(k) + '.txt', 'r') as f:
        line = f.readlines()
        for i in range(1200):
            for j in line[i]:
                if j == '0' or j == '1':
                    small_bin_image[i].append(int(j))
        '''
        for i in range(512):
            bin_image[i] = [0 for i in range(2048)]
        temp = 0
        for i in range(512, 1712):
            bin_image[i] = [0 for i in range(512)] + small_bin_image[temp] + [0 for i in range(336)]
            temp += 1
        for i in range(1712, 2048):
            bin_image[i] = [0 for i in range(2048)]
        '''

    # fill the pixels:
    for y in range(height):
        for x in range(width):
            if bin_image[x][y] == 1:
                ImageDraw.Draw(image).point((y, x), fill=(255, 0, 0))
    # output the png:
    image.save('temp/' + str(k) + '.png', 'png')
    print('temp/' + str(k) + '.png, done.')