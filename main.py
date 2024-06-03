# #                                                        Code Surge !
# #                                                        Code Surge !
# #                                                        Code Surge !
# #                                                        Code Surge !
#                                                   https://github.com/MiladMirj
#                                           https://www.linkedin.com/in/milad-mirjalili-15147421a/
#
"""
    Enjoy Scraping !
                        * This script allows the user to :
                                -- scrape Articles from Wikipedia Farsi (Persian) !
                                -- Use extracted data to create images of text and with boudning boxe coordinates of text area !
                                -- Create augmented versions of generated images
                                -- Draw bounding boxes
                        * In order to run this script it's required to install the following library.
                                1- `BeautifulSoup` for processing the HTML.
                                2- `Pillow` for processing images.
                                3- `Scikit-learn` to split training data
                                4- `imgaug` for augmenting images.

"""

from pathlib import Path
import os
from glob import glob
from scrape_Wikipedia import generate_data, load_data
from image_with_text_generator import process_data    
from utils import draw_bbox, create_files_to_train

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    resources_folder = os.path.join(dir_path, "resources")
    data_folder = os.path.join(dir_path, "Articles_data")
    Path(resources_folder).mkdir(parents=True, exist_ok=True)
    Path(data_folder).mkdir(parents=True, exist_ok=True)
    data_location = os.path.join(data_folder, 'Articles_data.json')
    extracted_links_location = os.path.join(data_folder, 'extracted_links.txt')
    font_location = os.path.join(resources_folder, 'fonts')
    train_imgs_path = os.path.join(dir_path, "created_imgs_with_text")
    Path(train_imgs_path).mkdir(parents=True, exist_ok=True)
    print( " << WELCOME ! >>")
    command_text = " Enter \n 1 for scraping Wikipedia Articles ! \n 2 for generating Images with Augmentation ! \n 3 for generating Images without Augmentation ! \n 4 for moving images and text files to folders for training ! \n 5 for Adding bounding boxes to Images \n e for Exit ! \n Input : "
    command = input (command_text)

    if command not in ['1', '2', '3', '4', '5', 'e']:
        command = 'invalid'
        while command == 'invalid' or command not in ['1', '2', '3', '4', '5', 'e']:
                command = input (" Invalid input ! ! ")

    loaded_datas, processed_links, extracted_links = load_data(data_location, extracted_links_location)
    if command == '1':
        print(str(len(loaded_datas)) + " Articles are stored in the database !")
        print(str(len(extracted_links)) + " Links are ready to extract !")
        number_links_to_save = input("How many articles to save? ")
        if number_links_to_save.isdigit() and number_links_to_save!= '0':
                try:
                    generate_data(processed_links, loaded_datas, extracted_links, number_links_to_extract=int(number_links_to_save), save_location=data_location,
                        save_extracted_location=extracted_links_location)
                except Exception as e:
                    print("Error " + str(e))
        else:
            number_links_to_save = "invalid"
            print(" Enter a number ! ")
            while not number_links_to_save.isdigit() or number_links_to_save== '0':
                number_links_to_save = input("How many Articles to save? ")  
            try:
                generate_data(processed_links, loaded_datas, extracted_links, number_links_to_extract=int(number_links_to_save), save_location=data_location,
                    save_extracted_location=extracted_links_location)
            except Exception as e:
                print("Error " + str(e))  

    elif command == '2' or command =='3':
        if command =='2':
            augment = True
        else:
            augment = False
        number_articles_to_process = input("How many Articles to process? ")
        if number_articles_to_process.isdigit() and number_articles_to_process!= '0':
                try:
                    process_data(limit=int(number_articles_to_process), train_path=train_imgs_path,
                        loaded_datas=loaded_datas, _augment=augment, _font_location=font_location, _dir_path = dir_path)
                except Exception as e:
                    print("Error " + str(e))
        else:
            number_articles_to_process = "invalid"
            print(" Enter a number ! ")
            while not number_articles_to_process.isdigit() or number_articles_to_process== '0':
                number_articles_to_process = input("How many Articles to process? ")  
            try:
                process_data(limit=int(number_articles_to_process), train_path=train_imgs_path, 
                        loaded_datas=loaded_datas, _augment=augment, _font_location=font_location, _dir_path = dir_path)
            except Exception as e:
                print("Error " + str(e))  

    elif command == '4':
        print ("Start moving Images and Texts ... ")
        create_files_to_train(dir_path=dir_path)
    elif command == '5':
        print("Start creating Images with bounding boxes ! ")
        imgs_path = list(glob(os.path.join(dir_path, "created_imgs_with_text\**\*.jpg"), recursive=True))
        draw_bbox(imgs_path, 2)
    elif command == 'e':
        pass

# ////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////
# ////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////# ////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////# ////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////# ////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# ///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////


