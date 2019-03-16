from PIL import Image, ImageDraw
import numpy as np
import matplotlib.image as mpimg

# enlarged image size:
enlarged_width = 2400
enlarged_height = 2400

# smaller image size:
sm_width = 1200
sm_height = 1200

# output image size:
output_width = 2048
output_height = 2048

# count the output of png and txt:
output_count = 1

# max num is 440
txt_num = int(input('input the number of texts, in [2, 440]:'))
for k in range(1, txt_num):
    print('Reading the ' + 'temp/' + str(k) + '.png')

    # load a color image
    sm_im = Image.open('temp/' + str(k) + '.png')

    # enlarge the image
    im = sm_im.resize((enlarged_width, enlarged_height))

    # read the enlarged image to a array
    im_numpy_array = np.array(im)
    shape = im_numpy_array.shape
    im_array = im_numpy_array.tolist()
    large_image_array = im_array
    for i in range(enlarged_height):
        for j in range(enlarged_width):
            if im_array[i][j] == [255, 255, 255]:
                large_image_array[i][j] = 0
            else:
                large_image_array[i][j] = 1

    # split the array:
    splited_image_array = [[[] for j in range(sm_height)] for i in range(4)]
    for i in range(enlarged_height // 2):
        for j in range(enlarged_width // 2):
            splited_image_array[0][i].append(large_image_array[i][j])
    for i in range(enlarged_height // 2):
        for j in range(enlarged_width // 2, enlarged_width):
            splited_image_array[1][i].append(large_image_array[i][j])
    for i in range(enlarged_height // 2, enlarged_height):
        for j in range(enlarged_width // 2):
            splited_image_array[2][i - enlarged_height // 2].append(large_image_array[i][j])
    for i in range(enlarged_height // 2, enlarged_height):
        for j in range(enlarged_width // 2, enlarged_width):
            splited_image_array[3][i - enlarged_height // 2].append(large_image_array[i][j])

    # generate the 2048*2048 array:
    output_image_array = [[[] for j in range(output_height)] for i in range(4)]
    for i in range(4):
        for j in range(512):
            output_image_array[i][j] = [0 for i in range(2048)]
        temp = 0
        for j in range(512, 1712):
            output_image_array[i][j] = [0 for i in range(512)] + splited_image_array[i][temp] + [0 for i in range(336)]
            temp += 1
        for j in range(1712, 2048):
            output_image_array[i][j] = [0 for i in range(2048)]

    for k in output_image_array:
        image = Image.new('RGB', (2048, 2048), (255, 255, 255))
        # fill the pixels:
        for y in range(output_height):
            for x in range(output_width):
                if k[x][y] == 1:
                    ImageDraw.Draw(image).point((y, x), fill=(255, 0, 0))
        # output the png:
        image.save('Mask_png_splited/' + str(output_count) + '.png', 'png')
        print('Mask_png_splited/' + str(output_count) + '.png, done.')
        # output the txt:
        with open('Mask_bin_splited/' + str(output_count) + '.txt', 'w') as f:
            for i in k:
                for j in i:
                    f.write(str(j) + ' ')
                f.write('\n')
        print('Mask_bin_splited/' + str(output_count) + '.txt, done.')
        output_count += 1
