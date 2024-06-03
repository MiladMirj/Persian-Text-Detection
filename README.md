# Persian-Text-Detection-Wikipedia
This Python source code tool performs the following functions:

    -Extracting articles from Wikipedia in Farsi.
    -Creating random images with text and their bounding box coordinates for text detection.
    -Creating augmented images to enhance performance.
    -Using a YOLO v5 pre-trained model to detect text in images.

## Description
In the initial phase of this project, I aim to create an article scraper for Wikipedia in Persian. It will start from a random URL, extract all links on that page, then randomly open another page and repeat the process. 
Next, I aim to overlay text on different random images. Depending on the length of the text, I will break it into smaller chunks, and for each chunk, I will create images using a random font and draw the text at a random position on the image. I also create augmented images for better performance.
Using a YOLO v5 model, The model will then take an image as input, with up to four possible locations of text and their bounding boxes. The model's output will be the number of detected bounding boxes and their coordinates. It was trained for maximum 4 text areas inside an image.
## Requirements
```
$ pip install pillow
$ pip install beautifulsoup4
$ pip install numpy
$ pip install scikit-learn
$ pip install imgaug

```
## How to run
Run main.py and follow the instructions.

## Sample training data and output
![val_batch0_pred](https://github.com/MiladMirj/Persian-Text-Detection-Wikipedia/assets/131509932/5d5b97a2-2f63-4d94-8503-735c72c1d8a0)

![train_batch0](https://github.com/MiladMirj/Persian-Text-Detection-Wikipedia/assets/131509932/46ff5994-46ea-4527-8933-5fbcd747fc06)

![Capture2](https://github.com/MiladMirj/Persian-Text-Detection-Wikipedia/assets/131509932/2cb536c6-a1df-4276-9ec1-7538f7d2e261)

![Capture](https://github.com/MiladMirj/Persian-Text-Detection-Wikipedia/assets/131509932/9b52711e-1835-40e2-9c47-3780b15e1425)

