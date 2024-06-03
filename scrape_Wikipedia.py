# #                                                        Code Surge !
# #                                                        Code Surge !
# #                                                        Code Surge !
# #                                                        Code Surge !
#                                                   https://github.com/MiladMirj
#                                           https://www.linkedin.com/in/milad-mirjalili-15147421a/
#
"""
    Enjoy Scraping !
                        This script allows the user to scrape Articles from Wikipedia Farsi (Persian) !

"""




import requests
from bs4 import BeautifulSoup
import random
import json
from pathlib import Path
import os
import time
import traceback




def save_data(dict_to_save, extracted_links, save_data_location, extracted_links_location):
    with open(save_data_location, "w", encoding="utf-8") as file:
        json.dump(dict_to_save, file, indent=4)

    with open(extracted_links_location, "w", encoding="utf-8") as file:
        for extraced_link in extracted_links:   
            file.write(extraced_link +'\n')

def load_data(data_location, extracted_links_location):
    json_file = Path(data_location)
    extracted_links_file = Path(extracted_links_location)
    loaded_datas = []
    extracted_links = []
    processed_links = []
    if json_file.is_file():
        with open(data_location, "r", encoding="utf-8") as file:
            loaded_datas = json.load(file)	
    if len(loaded_datas) != 0:
        for load_data in loaded_datas:
            processed_links.append(load_data["id_url"]) 
    if extracted_links_file.is_file():
        with open(extracted_links_location, "r", encoding="utf-8") as file:
            for extracted_link in file.readlines():
                extracted_links.append(extracted_link.strip()) 
    return loaded_datas, processed_links, extracted_links

def connect_url(url, time_out, retries, wait_between_call):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
    connect_counter = 0
    data_corrupt = True
    while data_corrupt and connect_counter < retries:
        try:
            response = requests.get(
                url=url, headers=headers, timeout=time_out)
            if response is not None:
                data_corrupt = False
                return response

        except requests.exceptions.RequestException as e:        
             connect_counter += 1
             print('\n Error connecting ... retrying in ' + str(wait_between_call) +' seconds... ' + str(e))
             time.sleep(wait_between_call)
    return None

def scrape_Wiki_article(url, _c_counter, _filter_links, _processed_links ,_loaded_datas, number_links_to_extract=1, first_run=False ):

    response = connect_url(url, time_out=10, retries=5, wait_between_call=5)
    if response == None:
        print( "Error ! ")
        return _loaded_datas, _filter_links
    soup = BeautifulSoup(response.content, 'html.parser')
    body_content = soup.find(id="bodyContent")
    text_content = soup.find(id="bodyContent")
    [s.extract() for s in text_content.select('iframe, script, table, figure, span.mw-editsection-bracket,\
                                        span.mw-editsection, div.reflist, div.catlinks, div.refbegin, div.vector-body-before-content,\
                                              div#contentSub, div.printfooter, span#منابع, span#پیوند_به_بیرون, sup.reference,\
                                              span#جستارهای_وابسته, span.lang-comment, a.external.text, style,\
                                              div.quotebox ')]
    text_content = text_content.text.replace("\u0654", "")
    if body_content is not None:
        title = soup.find(id="firstHeading")
        temp_dict = {}
        temp_dict.update({
            "id_url" : url, 
            "info": {"title": title.text,
             "body_text": text_content}
        })
        
        if not first_run:
            _c_counter +=1 
            _loaded_datas.append(temp_dict)
            progress =str(round(_c_counter / number_links_to_extract * 100, 2))
            print(progress + " % ", end=' ', flush=True)
        _processed_links.append(url)
        allLinks = body_content.find_all("a")
        for link in allLinks:
                if link.has_attr('href'):
                    if "/wiki/" in link['href'] and "wikipedia" not in link["href"] and "https://" not in link["href"] and \
                        "https://fa.wikipedia.org/" + link['href'] not in _filter_links and \
                        "%D9%88%DB%8C%DA%98%D9%87:%D9%88%DB%8C%D8%B1%D8%A7%DB%8C%D8%B4_%D8%B5%D9%81%D8%AD%D9%87" not in link['href'] and \
                        not link['href'].lower().endswith(".jpg") and not link['href'].lower().endswith(".png"):                                
                                _filter_links.append("https://fa.wikipedia.org/" + link['href'])                               
    if _c_counter >= number_links_to_extract:
        return _loaded_datas, _filter_links
    link_to_process = _filter_links[random.randint(0, len(_filter_links) - 1)]
    try:
        while link_to_process in _processed_links:
            if len(_processed_links) >= len(_filter_links):
                return _loaded_datas, _filter_links
            else:
                link_to_process = _filter_links[random.randint(0, len(_filter_links) - 1)]
        if (_c_counter) % 15 == 0 and not first_run:
            print("\nLets get some rest ! ...  (20 seconds)  " + str(_c_counter) + " Articles are added to the database !")
            time.sleep(20)

        return scrape_Wiki_article(link_to_process, _c_counter, _filter_links, _processed_links,_loaded_datas, 
                            first_run=False, number_links_to_extract=number_links_to_extract)
    except KeyboardInterrupt:
         return _loaded_datas, _filter_links
         print("Canceled ! ")

def generate_data(_processed_links, _loaded_datas, _extracted_links, number_links_to_extract=1,
            save_location='', save_extracted_location=''):
    c_counter = 0
    try:
        if len(_extracted_links) > 0:
            _url = _extracted_links[random.randint(0, len(_extracted_links) - 1)]
            _first_run=False
        else:
            _url = "https://fa.wikipedia.org/wiki/%D8%B5%D9%81%D8%AD%D9%87%D9%94_%D8%A7%D8%B5%D9%84%DB%8C"
            _first_run=True
        print(" Progress : ")

        ret_loaded_datas, ret_extracted_links = scrape_Wiki_article(_url, c_counter, _extracted_links, 
                   _processed_links, _loaded_datas, first_run=_first_run, number_links_to_extract=number_links_to_extract)

        print("\nSaving data : " + str (len(ret_loaded_datas)) + " Articles are saved in the database !")
        print("Saving data : " + str (len(ret_extracted_links)) + " Links are ready to extract !")
        save_data(ret_loaded_datas, ret_extracted_links, save_location, save_extracted_location)           
    except Exception as e:
        print(e.__repr__)
        print(str(e))
        print(traceback.format_exc())
    




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


