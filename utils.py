from pathlib import Path
import os
from glob import glob
import shutil
from sklearn.model_selection import train_test_split
from PIL import ImageDraw
from PIL import Image



def load_fonts(path):
    list_fonts = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(".ttf") or file.lower().endswith("otf"):
                list_fonts.append(os.path.join(root, file))


    return list_fonts

def draw_bbox(img_paths, mode=1):

    for img_path in img_paths:
        if "rectangle" in img_path:
            continue

        img = Image.open(img_path).copy()
        draw = ImageDraw.Draw(img)
        if mode == 1:
            with open(img_path.replace(".jpg", ".txt"), mode="r") as file:
                texts = file.readlines()
                for text in texts:
                    _, c1, a1, d1, b1, w1, h1 =  map(int, text.split())
                    draw.rectangle((c1, a1, d1, b1), outline =(0, 0, 0))
        elif mode == 2:
            with open(img_path.replace(".jpg", ".txt"), mode="r") as file:
                texts = file.readlines()
                for text in texts:
                    _, w_center, h_center, width, height =  map(float, text.split())
                    c1, a1, d1, b1 = convert_center_to_actual(img.width, img.height, w_center, h_center, width, height)
                    draw.rectangle((c1, a1, d1, b1), outline =(0, 0, 0))
        img.save(img_path.replace(".jpg", "_rectangle.jpg"))

def convert_center_to_actual(img_width, img_height, w_center, h_center, width, height):
        d1 = int((img_width * w_center) + (img_width*width / 2))
        c1 = int(d1 - width * img_width)
        b1 = int((img_height * h_center) + (height * img_height / 2))
        a1 = int(b1 - height * img_height)    
        return c1, a1, d1, b1



def create_files_to_train(dir_path):
    
    train_img_directory = os.path.join(dir_path, "dataset\\images\\train")
    val_img_directory = os.path.join(dir_path, "dataset\\images\\val")
    test_img_directory = os.path.join(dir_path, "dataset\\images\\test")
    train_lable_directory = os.path.join(dir_path, "dataset\\labels\\train")
    val_lable_directory = os.path.join(dir_path, "dataset\\labels\\val")
    test_lable_directory = os.path.join(dir_path, "dataset\\labels\\test")
    dataset_locations = [train_img_directory, val_img_directory, test_img_directory, train_lable_directory, val_lable_directory, test_lable_directory]
    for train_location in dataset_locations:
        Path(train_location).mkdir(parents=True, exist_ok=True)

    img_locations = list(glob(os.path.join(dir_path, "created_imgs_with_text\**\*.jpg"), recursive=True))
    filter_imgs = [img for img in img_locations if not "rectangle" in img]
    text_locations = list(glob(os.path.join(dir_path, "created_imgs_with_text\**\*.txt"), recursive=True))
    if len(filter_imgs) == 0 :
        print ( " No Image to move ! ")
        return
    train_images, val_images, train_annotations, val_annotations = train_test_split(filter_imgs, text_locations, test_size = 0.2, random_state = 1)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

    def move_files_to_folder(list_of_files, destination_folder):
        for f in list_of_files:
            try:
                shutil.move(f, destination_folder)
            except:
                print(f)
                assert False
    move_files_to_folder(train_images, train_img_directory)
    move_files_to_folder(val_images, val_img_directory)
    move_files_to_folder(test_images, test_img_directory)
    move_files_to_folder(train_annotations, train_lable_directory)
    move_files_to_folder(val_annotations, val_lable_directory)
    move_files_to_folder(test_annotations, test_lable_directory)
    print("Finished creating data for training ! ")
    print("Images and Texts are stored inside " + str(os.path.join(dir_path, "dataset\\")))        