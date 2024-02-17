# -*- coding: utf-8 -*-
import random
import re
import requests

FILENAME = "dois.txt"

def store_dois(filename):
    # open file
    file = open(filename, 'r')
    
    # create cleaned list of dois
    dois = []
    for doi in file:
        doi = doi.replace(',', '')
        doi = doi.replace('\n', '')
        dois.append(doi)
    file.close()
    
    return dois
    
 
def store_pdfs(filename):
    pdf_file = open(filename, "r")
    pdfs = []
    for pdf in pdf_file:
        pdf = pdf.replace('\n', '')
        pdfs.append(pdf)
    pdf_file.close()
    
    return pdfs

def publishers(doi_lst):
    pub_dct = {}
    for i in range(10):
        doi = doi_lst[i]
        rest = re.search(r"/(.*)", doi)
        clean_rest = rest.group(1)
        pub_dct[doi] = clean_rest

    pub_dict_final = {}
    for key, value in pub_dct.items():
        if value[:2] == "j.":
            new_value = re.search(r"j\.\D*", value).group(0)
        else:
            new_value = value
        pub_dict_final[key] = new_value
        
    # easy to see output
    for key, value in pub_dict_final.items():    
        print(f"{key}: {value}")
               
                      
def rand_dois(dois, x):
    # gets a random list of 100 dois
    # list of dois, how many random dois wanted
    rand_dois = []
    rand_nums = []
    while len(rand_nums) < x: #1537
        rand_int = random.randint(0, len(dois) - 1)
        if rand_int not in rand_nums:
            rand_nums.append(rand_int)
    
    for i in range(len(rand_nums)):
        rand_doi = dois[rand_nums[i]]
        rand_dois.append(rand_doi)
    
    return rand_dois


def remove_first_8(dois):
    new_dois = []
    for i in range(len(dois)):
        new_dois.append(dois[i][8:])
        
    return new_dois


def same(words):
    '''
    Condenses like strings so that only the similarities between the strings
    are in final list
    
    '''
    string_lst = []
    
    # for every word in the list
    for i in range(len(words)-1):
        x = 0
        characters = []
        
        # for every letter in the word
        for x in range(min(len(words[i]), len(words[i + 1]))):
            
            # add matching letters to characters
            if words[i][x] == words[i+1][x]:
                characters.append(words[i][x])
                x += 1
            else: break
        
        # if characters list not empty or is an actual doi (gets rid of 'j.', '00')
        if not not characters and len(characters) > 3:
            full_string = ''.join(characters)
            
            # add the first doi to the list
            if not string_lst:
                
                # add the "cleaned" doi
                string_lst.append(full_string)

            
            else:
                
                # if there are lonely DOIs, add them too
                if words[i][:3] not in words[i-1] and words[i][:3] not in words[i+1]:
                    string_lst.append(words[i])

                # don't repeat
                for i in range(len(string_lst)):
                    if string_lst[i][:4] == full_string[:4]:
                        break
                    
                else: 
                    string_lst.append(full_string)
             
    return string_lst


def unique_keys_lst(file):
    dois = remove_first_8(store_dois(file))
    
    for i in range(1):
        dois = same(dois)
        
        
    with open('cleaned_dois.txt', 'w') as f:
        for item in dois:
            f.write(str(item) + '\n')


def get_random(file, x):
    # get a random number of dois
    # .txt with dois, number of random dois wanted
    
    dois = store_dois(file)
    lst = rand_dois(dois, x)
    return lst

'''
def one_of_each(file):

    unique_dois = []
    
    # go through each doi
    for i in range(len(file)):
             
        key = file[i][8:]
        # if its the first DOI
        if not unique_dois:
            unique_dois.append(file[i])
            continue
        
        for x in range(len(unique_dois)):
            # if the first few letters(4) are in the list of unique DOIs, continue
            
            if unique_dois[x][8:12] == key[:4]:
                break
        
        # otherwise, add it to the list
        else:
            unique_dois.append(file[i])
    
    with open('one_of_each.txt', 'w') as f:
        for item in unique_dois:
            f.write(str(item) + '\n')
            
    return unique_dois
'''
def download_pdf(url, destination):
    response = requests.get(url)
    response.raise_for_status()  # Make sure the request was successful
    with open(destination, 'wb') as output_file:
        output_file.write(response.content)
    

        
