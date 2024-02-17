from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
import dois
import json
import os
              

def download_dois(doi_lst):
    ## Load configuration
    con_file = open("config.json")
    config = json.load(con_file)
    con_file.close()
    
     
    ## Initialize client
    client = ElsClient(config['apikey'])
    client.inst_token = config['insttoken']
    
    
    text_lens = []
    title_to_download_y = []
    title_to_download_n = []
    title_to_download_f = []
    titles_for_next = {}
    
    # define folder to store article text in
    folder_name = "article_txt_1" ############################################# **RESET**
    
    for i in range(len(doi_lst)):
        try: 
            doi = doi_lst[i]
            doi_doc = FullDoc(doi = doi)
            
            if doi_doc.read(client):                
                # store og text in og_text (Full text, dict thing)
                og_text = doi_doc.data['originalText']
                
                ### what is name of title
                title = doi_doc.title
        
                og_text_len = len(og_text)
                
                if len(og_text) < 204:
                    #title_to_download_n[doi] = "No"
                    title_to_download_n.append(doi)
                    titles_for_next[title] = doi
                    
                else: 
                    title_to_download_y.append(doi)
                    
                    # define name of file
                    file_name = f"{title}.txt"
                    error_chars = "\\/*?\"<>|:"
                    for char in error_chars:
                        file_name = file_name.replace(char, "")
                    
                    # add folder to path for file name
                    file_path = os.path.join(folder_name, file_name)
                    
                    
                    # add text to file
                    with open(file_path, 'w', encoding = 'utf-8') as f:
                        f.write(f"Title: {title}\n")
                        f.write(f"DOI: {doi}\n")
                        f.write("\n" + og_text)
                        f.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

                # add to list of lens
                text_lens.append(og_text_len)        
                    
                
            else:
                text_lens.append("Read document failed.")
                title_to_download_f.append(doi)
        
        except:
            print("Error for doi:", doi, title)
     
    return title_to_download_y, title_to_download_n, title_to_download_f, text_lens, titles_for_next

      
def count_downloaded(text_lens):
    
    full_doc = 0
    doc_fail = 0
    not_full_doc = 0
    for i in range(len(text_lens)):
        if text_lens[i] == "Read document failed.": 
           doc_fail += 1
        if isinstance(text_lens[i], int):
            if text_lens[i] < 250:
                not_full_doc += 1
            if text_lens[i] > 250:
                full_doc += 1
    
    full_percent = full_doc
    not_full_percent = not_full_doc
    failed_percent = doc_fail
    
    return full_percent, not_full_percent, failed_percent
  
    
def run(doi_lst):
    '''
    Run this for full program

    Parameters
    ----------
    doi_lst : list
        A list of DOIs to try.

    Returns
    -------
    None.

    '''
    doi_stats = download_dois(doi_lst)
    downloaded_dois_y, downloaded_dois_n, downloaded_dois_f, text_lens, titles_for_next = doi_stats
    counts = count_downloaded(text_lens)
    
    with open('stats_elsapy_1.txt', 'w') as f: ############################### **RESET
        f.write(f"DOI downloaded with full text: {counts[0]} \n")
        f.write(f"DOI downloaded without full text: {counts[1]} \n")
        f.write(f"DOI downloaded failed: {counts[2]} \n")
        
        f.write("\n")
        
        f.write("Full downloaded DOIs: \n")
        for item in doi_stats[0]:
            f.write(str(item) + '\n')
           
        f.write("\n")
        
        f.write("Not downloaded DOIs: \n")
        for item in doi_stats[1]:
            f.write(str(item) + '\n')
          
        f.write("\n") 
          
        f.write("Download failed DOIs: \n")
        for item in doi_stats[2]:
            f.write(str(item) + '\n')    
    
    new_doi_lst = downloaded_dois_n
    for doi in downloaded_dois_f:
        new_doi_lst.append(doi)
    
    return new_doi_lst, titles_for_next

  
        
def main():
    doi_lst = dois.store_dois("one_of_each.txt")
    DOI_LST = dois.rand_dois(doi_lst, 1000)
    
    doi_stats = download_dois(DOI_LST)
    downloaded_dois_y, downloaded_dois_n, downloaded_dois_f, text_lens = doi_stats[3]
    counts = count_downloaded(text_lens)
    
    with open('stats_elsapy.txt', 'w') as f: ################################# **RESET
        
        f.write(f"DOI downloaded with full text: {counts[0]} \n")
        f.write(f"DOI downloaded without full text: {counts[1]} \n")
        f.write(f"DOI downloaded failed: {counts[2]} \n")
        
        f.write("\n")
        
        f.write("Full downloaded DOIs: \n")
        for item in doi_stats[0]:
            f.write(str(item) + '\n')
           
        f.write("\n")
        
        f.write("Not downloaded DOIs: \n")
        for item in doi_stats[1]:
            f.write(str(item) + '\n')
          
        f.write("\n") 
          
        f.write("Download failed DOIs: \n")
        for item in doi_stats[2]:
            f.write(str(item) + '\n') 
    
    
    
    
    
    
    
    