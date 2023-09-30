# import cv2

# # read the first image
# img1 = cv2.imread('C:/Users/Amit/Downloads/amit_degree_vflat.jpg')

# # read the second image
# img2 = cv2.imread('C:/Users/Amit/Downloads/20230406_210240633_vflat.jpg')
path1 = 'C:/Users/Amit/Downloads/Akshit_orig_001.jpg'
path2 = 'C:/Users/Amit/Downloads/amit_orig_001.jpg'
import cv2

# read the first image
img1 = cv2.imread(path1)

# read the second image
img2 = cv2.imread(path2)

import cv2

# read the first image
img1 = cv2.imread(path1)

# read the second image
img2 = cv2.imread(path2)

# find the minimum height and width
min_height = min(img1.shape[0], img2.shape[0])
min_width = min(img1.shape[1], img2.shape[1])

# resize both images to the same size
resized_img1 = cv2.resize(img1, (min_width, min_height))
resized_img2 = cv2.resize(img2, (min_width, min_height))

# save the resized images
cv2.imwrite('resized_image1.jpg', resized_img1)
cv2.imwrite('resized_image2.jpg', resized_img2)
