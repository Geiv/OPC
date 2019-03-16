from PIL import Image, ImageDraw
# 规定2048 x 2048画纸:
width = 2048
height = 2048


for k in range(1, 11):
    image = Image.new('RGB', (width, height), (255, 255, 255))
    bin_image = [[] for i in range(2048)]
    # 读取二进制文件:
    with open('Mask_bin/M1_test' + str(k) + '.txt', 'r') as f:
        line = f.readlines()
        for i in range(2048):
            for j in line[i]:
                if j == '0' or j == '1':
                    bin_image[i].append(int(j))

    # 填充每个像素:
    for y in range(height):
        for x in range(width):
            if bin_image[x][y] == 1:
                ImageDraw.Draw(image).point((y, x), fill=(255, 0, 0))

    image.save('Mask_Png/M1_test' + str(k) + '.png', 'png')
    print('Mask_Png/M1_test' + str(k) + '.png, done.')
