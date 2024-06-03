import random
from pathlib import Path
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from glob import glob
from augment import create_aug
from utils import convert_center_to_actual, load_fonts






def process_text(text, I1, font, spacing, break_text_width, break_text_height):
    final_text = ''
    temp_text = final_text
    h_text = ''
    for ii, line in enumerate(text.splitlines()):
        if line.strip() == '' or line.isspace():
            continue
        for i, split in enumerate(line.split()):
            temp_text = h_text
            h_text += ' ' + split
            ww_text, hh_text= I1.multiline_textsize(h_text, font=font, spacing=spacing, direction='rtl')
            if ww_text > break_text_width :
                    h_text = split
                    if i == len(line.split()) - 1:
                        final_text += temp_text + '\n' + split
                        wf_text, hf_text= I1.multiline_textsize(final_text, font=font, spacing=spacing, direction='rtl')
                    else:
                         final_text += temp_text + '\n'
                         wf_text, hf_text= I1.multiline_textsize(final_text, font=font, spacing=spacing, direction='rtl')
                    if hf_text > break_text_height:
                        if i == len(line.split()) - 1:
                            return final_text, hf_text, [s + '\n' for s in text.splitlines()[ii + 1 : len(text.splitlines())] if s != ''] 
                        else:
                            return final_text, hf_text, \
                        [ss + " " for ss in line.split()[i: len(line.split())]] + ["\n"] + [s + '\n' for s in text.splitlines()[ii + 1 : len(text.splitlines())] if s != '']    

        if ww_text < break_text_width:
            final_text += ' '+ h_text
        h_text = ''
        final_text += '\n'        
    wf_text, hf_text= I1.multiline_textsize(final_text, font=font, spacing=spacing, direction='rtl')
    return final_text, hf_text, []

def create_img(list_fonts, texts, cc, path, file_name, font_color, img_background_color, part_number=0):
     for i, text in enumerate(texts):
        if len(texts) > 1:
            part_number = i
            cc = 0
        text = "".join(text)
        img_format = "RGB"
        img_width_size =  random.randint(128, 1500)
        img_height_size = random.randint(128, 1200)
        text_width_position =  random.randint(img_width_size//4, img_width_size - 20)
        text_height_position = random.randint(1, img_height_size - 100)
        spacing = random.randint(5, 20)
        font_size = random.randint(12, 32)
        font = random.choice(list_fonts)
        font = ImageFont.truetype(font, font_size)
        break_text_width = random.randint(text_width_position // 4, text_width_position - 20) 
        break_text_height = random.randint(25, img_height_size - text_height_position - 50)
        img = Image.new("RGB", (150, 150), 0)
        draw = ImageDraw.Draw(img)
        final_text, h_text, remain_texts = process_text(text, draw, font, spacing=spacing, break_text_width=break_text_width,
                                           break_text_height=break_text_height)
                  
        img = Image.new(img_format, (img_width_size, img_height_size), img_background_color)
        temp_img = Image.new(img_format, (img_width_size, img_height_size), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        temp_draw = ImageDraw.Draw(temp_img)
        draw.multiline_text((text_width_position, text_height_position), final_text,font = font, 
            fill=font_color, align='right', anchor='ra', direction='rtl', spacing=spacing )
        temp_draw.multiline_text((text_width_position, text_height_position), final_text,font = font, 
            fill=(255, 255, 255), align='right', anchor='ra', direction='rtl', spacing=spacing )
        coordinates= temp_img.getbbox()

        if (temp_img.getbbox() is not None):
            # center_width = round(((coordinates[0] + coordinates[2]) / 2 ) / img_width_size, 2)
            # center_height = round(((coordinates[1] + coordinates[3]) / 2) / img_height_size, 2)
            # text_w = round((coordinates[2] - coordinates[0]) / img_width_size, 2)
            # text_h = round((coordinates[3] - coordinates[1]) / img_height_size, 2)

            center_width = ((coordinates[0] + coordinates[2]) / 2 ) / img_width_size
            center_height = ((coordinates[1] + coordinates[3]) / 2) / img_height_size
            text_w = (coordinates[2] - coordinates[0] + 2) / img_width_size
            text_h = (coordinates[3] - coordinates[1] + 2) / img_height_size

            with open(path + '\\' + file_name + "_" + str(part_number) + "_" + str(cc) + '.txt', mode="w") as file:
                file.write("0 " + str(center_width)  + " " + \
                    str(center_height) + " " + str(text_w) + " " + str(text_h))
                
            if (final_text != ""):
                img.save(path + '\\' + file_name + "_" + str(part_number) + "_" + str(cc)  + '.jpg')
        if len(remain_texts) > 0:
                    cc += 1
                    create_img(list_fonts, [remain_texts], cc, path, file_name, font_color, img_background_color, part_number)

        else:
            pass

def load_random_img(text_paths):
    text_index= random.randint(0, len(text_paths) - 1)
    with open(text_paths[text_index], mode="r") as file2:
        _, c2, a2, d2, b2 = map(float, file2.read().split())
    if None not in (c2, a2, d2, b2):
        img_random = Image.open(str(text_paths[text_index]).replace(".txt", ".jpg")).copy() 
    return img_random, c2, a2, d2, b2, text_index

def create_overlaps(path):
    try:
        text_paths = list(Path(path).glob("*.txt"))
        text_paths = [p for p in text_paths if "overlap" not in str(p)]
        for i, text_path in enumerate(text_paths):
            with open(text_path, mode="r") as file:
                _, c1, a1, d1, b1 =  map(float, file.read().split())
            if None not in (c1, a1, d1, b1):
                chance = random.random()
                if chance > .4:
                    region1 = False
                    region2 = False
                    region3 = False
                    region4 = False
                    img_random, c2, a2, d2, b2, text_index = load_random_img(text_paths)
                    c2, a2, d2, b2 = convert_center_to_actual(img_random.width, img_random.height, c2, a2, d2, b2)
                    img_orig = Image.open(str(text_path).replace(".txt", ".jpg")).copy()
                    c1, a1, d1, b1 = convert_center_to_actual(img_orig.width, img_orig.height, c1, a1, d1, b1)
                    w1 = img_orig.width
                    h1 = img_orig.height
                    crop = img_random.crop((c2 - 2, a2 - 2, d2 + 2, b2 + 2))
                    if (((d2 - c2 + 4) < w1 - 4) and ((b2 + 2 <a1) and ((b2-a2 + 4) < a1 - 4))) :
                        paste_w1 = random.randint(4, w1 - d2 + c2 - 4)
                        paste_h1 = random.randint(4, a1 - b2+ a2- 4)
                        img_orig.paste(crop, (paste_w1, paste_h1))
                        region1 = True
                        c2_1, a2_1, d2_1, b2_1 = c2, a2, d2, b2
                        img_random, c2, a2, d2, b2, text_index = load_random_img(text_paths)
                        c2, a2, d2, b2 = convert_center_to_actual(img_random.width, img_random.height, c2, a2, d2, b2)
                        crop = img_random.crop((c2 - 2, a2 - 2, d2 + 2, b2 + 2))                    
                    if (((b2 - a2 + 4) < h1 - 4) and ((c2 >d1 + 2) and ((d2-c2 + 4) < (w1-d1 -4)))) :
                        
                        paste_w2 = random.randint(d1 + 4, w1 - d2 + c2 - 4)
                        if region1:
                            if paste_w1 + d2 - c2 + 4 > d1 + 4:

                                if ((b2 - a2 + 4) < (h1 - (paste_h1 + b2_1 - a2_1) -4)):

                                    paste_h2 = random.randint(paste_h1 + b2_1 - a2_1 + 4, h1 - b2 + a2 - 4)
                                    region2 = True
                                else:
                                    region2 = False
                            else:
                                paste_h2 = random.randint(4, h1 - b2 + a2 - 4)
                            
                        else:
                            paste_h2 = random.randint(4, h1 - b2 + a2 - 4)
                            region2 = True
                        if region2:    
                            img_orig.paste(crop, (paste_w2, paste_h2))
                            c2_2, a2_2, d2_2, b2_2 = c2, a2, d2, b2
                            img_random, c2, a2, d2, b2, text_index = load_random_img(text_paths)
                            c2, a2, d2, b2 = convert_center_to_actual(img_random.width, img_random.height, c2, a2, d2, b2)
                            crop = img_random.crop((c2 - 2, a2 - 2, d2 + 2, b2 + 2))           
                    if (((b2 - a2 + 4) < h1 - 4) and ((d2 + 2 <c1) and ((d2-c2 + 4) < (c1 -4)))) :
                        paste_w3 = random.randint(4, c1 - d2 + c2 - 4)
                        if region1:
                            if paste_w1 - 4 < c1:
                                if ((b2 - a2 + 4) < (h1 - (paste_h1 + b2_1 - a2_1) -4)):

                                    paste_h3 = random.randint(paste_h1 + b2_1 - a2_1 + 4, h1 - b2+ a2- 4)
                                    region3 = True
                                else:
                                    region3 = False
                            else:
                                paste_h3 = random.randint(4, h1 - b2+ a2- 4)
                        else:
                            paste_h3 = random.randint(4, h1 - b2+ a2- 4)
                            region3 = True
                        if region3:
                            img_orig.paste(crop, (paste_w3, paste_h3))
                        
                            c2_3, a2_3, d2_3, b2_3 = c2, a2, d2, b2
                            img_random, c2, a2, d2, b2, text_index = load_random_img(text_paths)
                            c2, a2, d2, b2 = convert_center_to_actual(img_random.width, img_random.height, c2, a2, d2, b2)
                            crop = img_random.crop((c2 - 2, a2 - 2, d2 + 2, b2 + 2))           
                    if (((d2 - c2 + 4) < w1) and ((a2 >b1 + 2) and ((b2-a2 + 4) < (h1-b1 - 4)))) :
                        
                        paste_h4 = random.randint(b1 + 4, h1 - b2+ a2- 4)
                        if region2 and region3:
                            
                                if(paste_h3 + b2_3 - a2_3 + 4) < b1:
                                    lower_paste_w4 = 4
                                else:
                                    lower_paste_w4 = paste_w3 + d2_3 - c2_3 + 4 
                                if (paste_h2 + b2_2 - a2_2 + 4) < b1:
                                    upper_paste_w4 = w1 - d2 + c2 - 4
                                else:
                                    upper_paste_w4 = paste_w2
                                
                                print("region2 , 3", str(text_path).replace(".txt", "_overlap.jpg"))
                                if (d2 - c2 + 4) > upper_paste_w4 - lower_paste_w4 - 4 :
                                    region4 = False
                                else:
                                    region4 = True
                                    paste_w4 = random.randint(lower_paste_w4, upper_paste_w4 - d2 + c2 - 4)
                        elif region3:
                                if(paste_h3 + b2_3 - a2_3 + 4) < b1:
                                    lower_paste_w4 = 4
                                else:
                                    lower_paste_w4 = paste_w3 + d2_3 - c2_3 + 4

                                if (d2 - c2 + 4) > w1 - lower_paste_w4 - 4 :
                                        region4 = False
                                else:
                                    paste_w4 = random.randint(lower_paste_w4, w1 - d2 + c2 - 4)
                                    region4 = True

                        elif region2:
                                if (paste_h2 + b2_2 - a2_2 + 4) < b1:
                                    upper_paste_w4 = w1 
                                else:
                                    upper_paste_w4 = paste_w2 
                                
                                if (d2 - c2 + 4) > upper_paste_w4 - 4:
                                    region4 = False
                                else:
                                    
                                    paste_w4 = random.randint(4, upper_paste_w4 - d2 + c2 - 4 )
                                    region4 = True
                                    

                        else:
                            if w1 - d2 + c2 - 4 > 4:
                                paste_w4 = random.randint(4, w1 - d2 + c2 - 4)
                                region4 = True
                            else:
                                region4 = False
                        if region4:
                            img_orig.paste(crop, (paste_w4, paste_h4))
                            
                        c2_4, a2_4, d2_4, b2_4 = c2, a2, d2, b2
                    if region1 or region2 or region3 or region4:
                        
                        img_orig.save(str(text_path).replace(".txt", "_overlap.jpg"))  
                        
                        center_width = ((c1 + d1) / 2 ) / w1
                        center_height = ((a1 + b1) / 2) / h1
                        text_w = (d1 - c1) / w1
                        text_h = (b1 - a1) / h1

                        text_to_save = "0" + " " + str(center_width) + " " + str(center_height) + " " + str(text_w) + " " + str(text_h) 


                        if region1:
                            center_width = ((paste_w1 + 1 + paste_w1 + d2_1 - c2_1+ 1) / 2 ) / w1
                            center_height = ((paste_h1+ 1 + paste_h1 + b2_1 - a2_1+ 1) / 2) / h1
                            text_w = (d2_1 - c2_1) / w1
                            text_h = (b2_1 - a2_1) / h1
                            text_to_save += '\n' + "0" + " " + str(center_width) + " " + str(center_height) + " " + str(text_w) + " " + str(text_h) 

                        if region2:
                            center_width = ((paste_w2 + 1 + paste_w2 + d2_2 - c2_2+ 1) / 2 ) / w1
                            center_height = ((paste_h2+ 1 + paste_h2 + b2_2 - a2_2+ 1) / 2) / h1
                            text_w = (d2_2 - c2_2) / w1
                            text_h = (b2_2 - a2_2) / h1
                            text_to_save += '\n' + "0" + " " + str(center_width) + " " + str(center_height) + " " + str(text_w) + " " + str(text_h)
                          

                        if region3:

                            center_width = ((paste_w3 + 1 + paste_w3 + d2_3 - c2_3+ 1) / 2 ) / w1
                            center_height = ((paste_h3+ 1 + paste_h3 + b2_3 - a2_3+ 1) / 2) / h1
                            text_w = (d2_3 - c2_3) / w1
                            text_h = (b2_3 - a2_3) / h1
                            text_to_save += '\n' + "0" + " " + str(center_width) + " " + str(center_height) + " " + str(text_w) + " " + str(text_h)

                        if region4:
                            center_width = ((paste_w4 + 1 + paste_w4 + d2_4 - c2_4+ 1) / 2 ) / w1
                            center_height = ((paste_h4+ 1 + paste_h4 + b2_4 - a2_4+ 1) / 2) / h1
                            text_w = (d2_4 - c2_4) / w1
                            text_h = (b2_4 - a2_4) / h1
                            text_to_save += '\n' + "0" + " " + str(center_width) + " " + str(center_height) + " " + str(text_w) + " " + str(text_h)

                            # text_to_save += '\n' + "0" + " " + str(paste_w4+ 1) + " " + str(paste_h4+ 1) + " " + str(paste_w4 + d2_4 - c2_4+ 1) + " " + \
                            #         str(paste_h4 + b2_4 - a2_4+ 1) + " " + str(w1) + " " + str(h1) 
                        with open(str(text_path).replace(".txt", "_overlap.txt"), mode="w") as file:
                # file.write("0 " + center_width + " " + center_width + " " + text_w + " " + text_h)
                            
                            file.write(text_to_save)
            
    except Exception as e:
        print("Error creating augmented images ! " + str(e))


def process_data(limit = 1, train_path= '',  loaded_datas=[], _augment=False,  _font_location=[], _dir_path=''):
    if (limit > len(loaded_datas)):
        limit = len(loaded_datas)
        print("The number of Articles are low, run scrape_Wikipedia first")
    c_counter = 0
    print( " Progress :  ... ")
    list_fonts = load_fonts(_font_location)
    for i, loaded_data in enumerate(loaded_datas):
        url_id = "".join(x for x in str(loaded_data["id_url"]).replace("https://fa.wikipedia.org//wiki/", "") if x.isalnum())
        url_id_short = url_id[:(216  - len(train_path)) // 2]
        folder_path = os.path.join(train_path, url_id_short)
        if os.path.exists(folder_path):
            continue
        
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        R_img = random.randint(150, 255)
        G_img = random.randint(150, 255)
        B_img = random.randint(150, 255)
        img_background_color = (R_img, G_img, B_img)
        R_text = random.randint(0, 50)
        G_text = random.randint(0, 50)
        B_text = random.randint(0, 50)
        font_color = (R_text, G_text, B_text)
        cc = 0
        text =loaded_data["info"]["body_text"].strip()
        temp_string = [s + '\n' for s in text.splitlines() if s != '']
        counterr = len(temp_string)
        if (counterr > 10):
            n = random.randint(counterr//6,  counterr//4)
            parts = [temp_string[i:i+n] for i in range(0, len(temp_string), n)]
            create_img(list_fonts, parts, cc, folder_path, url_id_short,
                    font_color, img_background_color)
        else:
            create_img(list_fonts, temp_string, cc, folder_path, url_id_short,
                    font_color, img_background_color)
        
        create_overlaps(folder_path)
        c_counter += 1
        progress =str(round(c_counter / limit * 100, 2))
        print(progress + " % ", end= ' ', flush=True)
        if c_counter >= limit:
            break
        
    imgs_path = list(glob(os.path.join(_dir_path, "created_imgs_with_text\**\*.jpg"), recursive=True))        
    if _augment:        
        create_aug(imgs_path)  
    imgs_path = list(glob(os.path.join(_dir_path, "created_imgs_with_text\**\*.jpg"), recursive=True))
    print("\n "+str(len(imgs_path)) + " Images of Articles are stored in the database !")          





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


