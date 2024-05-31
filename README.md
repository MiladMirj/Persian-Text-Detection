# Persian-Text-Detection-Wikipedia
This Python source code tool performs the following functions:

    -Extracting articles from Wikipedia in Farsi.
    -Creating random images with text and their bounding box coordinates for text detection.
    -Creating augmented images to enhance performance.
    -Using a YOLO v5 pre-trained model to detect text in images.

## Description
In the initial phase of this project, I aim to create an article scraper for Wikipedia in Persian. It will start from a random URL, extract all links on that page, then randomly open another page and repeat the process. 
Next, I aim to overlay text on different random images. Depending on the length of the text, I will break it into smaller chunks, and for each chunk, I will create images using a random font and draw the text at a random position on the image. I also create augmented images for better performance.
Using a YOLO v5 model, The model will then take an image as input, with up to four possible locations of text and their bounding boxes. The model's output will be the number of detected bounding boxes and their coordinates.
## Requirements
```
$ pip install pillow
$ pip install beautifulsoup4
$ pip install numpy
$ pip install scikit-learn
```
## Sample output
