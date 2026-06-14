
import random
from PIL import Image
import time
import sys
# img = Image.open("og_img.jpg")

img = Image.open(sys.argv[1])
# start = time.perf_counter()
k_val = int(sys.argv[2])
# k_val = 27


def naive_27(img):
    new_img = img.copy()
    width, height = new_img.size
    new_pix = new_img.load() 
    for i in range(width):
        for j in range(height):
            colors = new_pix[i, j]
            new_colors = []
            for val in colors:
                if val < (255 // 3):
                    new_colors.append(0)
                elif val > (255 * 2 // 3):
                    new_colors.append(255)
                else:
                    new_colors.append(127)
            new_pix[i, j] = (new_colors[0], new_colors[1], new_colors[2])
    new_img.show()
    new_img.save("naive_27.png")

def naive_8(img):
    new_img = img.copy()
    width, height = new_img.size
    new_pix = new_img.load() 
    for i in range(width):
        for j in range(height):
            colors = new_pix[i, j]
            new_colors = []
            for val in colors:
                if val < 128:
                    new_colors.append(0)
                else:
                    new_colors.append(255)
            new_pix[i, j] = (new_colors[0], new_colors[1], new_colors[2])
    new_img.show()
    new_img.save("naive_8.png")
    
def create_dict(pix, width, height):
    colors = dict()
    for i in range(width):
        for j in range(height):
            if pix[i, j] in colors.keys():
                colors[pix[i, j]].append((i, j))
            else:
                colors[pix[i, j]] = [(i, j)]
    return colors


def initialize_means(img, k_val):
    means = []
    possible_x_vals = range(img.size[0])
    possible_y_vals = range(img.size[1])
    while len(means) < k_val:
        x_val = random.choice(possible_x_vals)
        y_val = random.choice(possible_y_vals)
        pixel = img.getpixel((x_val, y_val))
        if pixel not in means:
            means.append(pixel)
    return means

def assign_pixels_to_clusters(colors, means):
    clusters = [[] for _ in range(len(means))]
    for color, pixel_list in colors.items():
        closest_mean_idx = min(range(len(means)), key=lambda i: distance(means[i], color))
        clusters[closest_mean_idx].extend(pixel_list)
    return clusters

def update_means(new_pix, clusters):
    new_means = []
    for cluster in clusters:
        new_mean = find_average(new_pix, cluster)
        new_means.append(new_mean)
    return new_means

def iteration(img, k_val, means):
    new_img = img.copy()
    new_pix = new_img.load()
    colors = create_dict(new_pix, *img.size)
    mean_pixels = assign_pixels_to_clusters(colors, means)

    while True:
        new_means = update_means(new_pix, mean_pixels)
        new_clusters = assign_pixels_to_clusters(colors, new_means)
        if new_means == means:
            break
        means = new_means
        mean_pixels = new_clusters

    for count, mean in enumerate(means):
        for pixel in mean_pixels[count]:
            new_pix[pixel[0], pixel[1]] = tuple(round(x) for x in mean)

    new_img.save('kmeansout.png')

def k_means(img, k_val):
    means = initialize_means(img, k_val)
    iteration(img, k_val, means)



def distance(pixel1, pixel2):
    red = (pixel1[0] - pixel2[0]) ** 2
    blue = (pixel1[1] - pixel2[1]) ** 2
    green = (pixel1[2] - pixel2[2]) ** 2
    return red + blue + green

def find_average(new_pix, pixels):
    red_sum = 0
    blue_sum = 0
    green_sum = 0
    for i in range(len(pixels)):
        red_sum += new_pix[pixels[i][0], pixels[i][1]][0]
        green_sum += new_pix[pixels[i][0], pixels[i][1]][1]
        blue_sum += new_pix[pixels[i][0], pixels[i][1]][2]
    avg_tuple = (red_sum/len(pixels), green_sum/len(pixels), blue_sum/len(pixels))
    return avg_tuple

k_means(img,k_val)
# naive_27(img)
# naive_8(img)


# end = time.perf_counter()
# print(end-start)
