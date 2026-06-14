import random
from PIL import Image
import sys

def abundance(data):
    counts = {}
    for item in data:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    max_count = max(counts.values())
    mode_items = [item for item, count in counts.items() if count == max_count]
    return random.choice(mode_items)


def get_image_dataset(img):
    coords = []
    colors = []
    width, height = img.size
    pixels = img.load()
    for i in range(width):
        for j in range(height):
            coords.append([i, j])
            colors.append(pixels[i, j])
    return coords, colors

def error(mean, pixel):
    total = 0
    for i in range(len(mean)):
        total += (mean[i] - pixel[i]) ** 2
    return total

weights = [[0, 0, 2], [1, 1, 0]]

def naive_algorithm(img, k):
    width, height = img.size
    output_img = Image.new("RGB", size=(width, height + (width // k)))
    original_pixels = img.load()
    output_pixels = output_img.load()

    diff_colors = set()
    for i in range(width):
        for j in range(height):
            rgb_value = original_pixels[i, j]
            if k == 8:
                classified_color = (
                    0 if rgb_value[0] < 128 else 255,
                    0 if rgb_value[1] < 128 else 255,
                    0 if rgb_value[2] < 128 else 255
                )
            else:
                if rgb_value[0] < 255 // 3:
                    classified_color = (0, 0, 0)
                elif rgb_value[0] > 255 * 2 // 3:
                    classified_color = (255, 255, 255)
                else:
                    classified_color = (127, 127, 127)
            diff_colors.add(classified_color)
            dR = original_pixels[i, j][0] - classified_color[0]
            dG = original_pixels[i, j][1] - classified_color[1]
            dB = original_pixels[i, j][2] - classified_color[2]
            for r in range(len(weights)):
                for c in range(len(weights[0])):
                    if i + r < width and j + c < height:
                        temp = original_pixels[i + r, j + c]
                        if temp != 0:
                            ratio = weights[r][c] / 4
                            original_pixels[i + r, j + c] = (
                                int(temp[0] + ratio * dR),
                                int(temp[1] + ratio * dG),
                                int(temp[2] + ratio * dB),
                            )
            output_pixels[i, j] = classified_color

    diff_colors = list(diff_colors)
    for i in range(width):
        color_index = int(i // (width / len(diff_colors)))
        for j in range(height, output_img.size[1]):
            output_pixels[i, j] = diff_colors[color_index]

    output_img.save("naive.png")
    output_img.show()


def kmeans(img, k, coordinates, colors):
    pixels = img.load()
    pixels_coords = coordinates
    dataset_colors = colors
    diff_colors = list(set(dataset_colors))

    def calculate_cluster_means():
        temp_diff_colors = diff_colors.copy()
        means = set()
        means.add(abundance(dataset_colors))
        temp_diff_colors.remove(abundance(dataset_colors))
        while len(means) != k:
            if len(means) == k - 1:
                times = 1
            else:
                times = random.choice([1, 2])
            values = [min([error(mean, m) for m in means]) for mean in temp_diff_colors]
            new_clusters = random.choices(values, weights=values, k=times)
            for val in new_clusters:
                temp_color = temp_diff_colors[values.index(val)]
                means.add(temp_color)
                temp_diff_colors.remove(temp_color)
        return list(means)

    def assign_clusters(k_means, clusters, coords, data):
        diff = {}
        for color in diff_colors:
            values = [error(mean, color) for mean in k_means]
            diff[color] = values.index(min(values))
        for i, color in enumerate(data):
            idx = diff[color]
            clusters[idx].append(coords[i])

    def apply_dithering(image, output, width, height, colors):
        for i in range(width):
            for j in range(height):
                values = [error(mean, image[i, j]) for mean in colors]
                color = colors[values.index(min(values))]
                dR = image[i, j][0] - color[0]
                dG = image[i, j][1] - color[1]
                dB = image[i, j][2] - color[2]
                for r in range(len(weights)):
                    for c in range(len(weights[0])):
                        if i + r < width and j + c < height:
                            temp = image[i + r, j + c]
                            if temp != 0:
                                ratio = weights[r][c] / 4
                                image[i + r, j + c] = (
                                    int(temp[0] + ratio * dR),
                                    int(temp[1] + ratio * dG),
                                    int(temp[2] + ratio * dB),
                                )
                output[i, j] = color

    def change_color_with_dithering(image, k_means, clusters):
        output_img = image.load()
        apply_dithering(pixels, output_img, img.size[0], img.size[1], k_means)
        for i in range(img.size[0]):
            color_index = int(i // (img.size[0] / k))
            for j in range(img.size[1], image.size[1]):
                output_img[i, j] = k_means[color_index]
        image.save("kmeansout.png")


    def calculate_new_mean(cluster):
        avg_red = 0
        avg_green = 0
        avg_blue = 0
        for val in cluster:
            avg_red += pixels[val[0], val[1]][0]
            avg_green += pixels[val[0], val[1]][1]
            avg_blue += pixels[val[0], val[1]][2]
        return (avg_red / len(cluster), avg_green / len(cluster), avg_blue / len(cluster))

    means = calculate_cluster_means()
    groups = [[] for _ in range(k)]

    assign_clusters(means, groups, pixels_coords, dataset_colors)
    sizes = [len(groups[i]) for i in range(k)]
    colors_count = len(dataset_colors)

    while colors_count != 0:
        means = [calculate_new_mean(cluster) for cluster in groups]
        groups = [[] for _ in range(k)]

        assign_clusters(means, groups, pixels_coords, dataset_colors)
        new_sizes = [len(groups[i]) for i in range(k)]
        colors_count = sum([abs(new_sizes[i] - sizes[i]) for i in range(k)])
        sizes = new_sizes

    for color_index in range(k):
        means[color_index] = (
            int(means[color_index][0]),
            int(means[color_index][1]),
            int(means[color_index][2]),
        )

    output_img = Image.new("RGB", size=(img.size[0], img.size[1] + (img.size[0]) // k), color=0)
    change_color_with_dithering(output_img, means, groups)



image_coordinates, image_colors = get_image_dataset(Image.open(sys.argv[1]))
image = Image.open(sys.argv[1])
# image_coordinates, image_colors = get_image_dataset(Image.open("og_img.jpg"))
# image = Image.open("og_img.jpg")
# k = 8  
k = int(sys.argv[2])
# naive_algorithm(image, k)
kmeans(image, k, image_coordinates, image_colors)
