# API CLient for Unpaywall
# Requires email
# call run() for full program

import requests
import dois
from PyPDF2 import PdfReader
from requests.exceptions import SSLError
import os

def get_urls(doi_lst, upw_email):
    '''
    Retrieves information and URLs associated with a list of DOIs

    Parameters
    ----------
    doi_lst : list
        A list of DOIs

    Returns
    -------
    urls_from_dois : list
        A list of DOIs that successfully outputted a pdf.
    urls : list
        A list of the pdfs corresponding to the downloaded_dois list.
    no_pdf_dois : list
        A list of DOIs that did not successfully output a pdf.
    num_error_dois : list
        A list of DOIs that were not included in the database.
    dois_with_pdf : int
        Number of DOIs with pdf.
    dois_without_pdf : int
        Number of DOIs that did not have a corresponding pdf.
    dois_not_in_database  : int
        Number of DOIs not in the database.
    titles : list
        List of titles associated with the DOIs

    '''
    # initialize lists and counts
    urls_from_dois = []
    urls = []
    no_pdf_dois = []
    num_error_dois = []
    titles = []
    dois_with_pdf = 0
    dois_without_pdf = 0
    dois_not_in_database  = 0
    
    for i in range(len(doi_lst)):
        
        doi = doi_lst[i]
        email = upw_email  # Replace with your email. Required by Unpaywall.
        
        response = requests.get(f"https://api.unpaywall.org/v2/{doi}?email={email}")
        
        # Ensure we got a valid response
        if response.status_code == 200:
            # Parse the response as JSON
            data = response.json()
        
            # Access specific fields in the JSON data
            
            location = data["best_oa_location"]
            
            if location is not None:
                # add to list for that DOI
                url = location['url']
                title = data["title"]
                #journal_name = data["journal_name"]
                #is_oa = data["is_oa"]
                
                dois_with_pdf += 1
                urls_from_dois.append(doi)
                urls.append(url)
                titles.append(title)
                
            else:
                dois_without_pdf += 1
                no_pdf_dois.append(doi)
                
        else:
            dois_not_in_database  += 1
            num_error_dois.append(doi)
        
        
    if not not urls_from_dois:
            return urls_from_dois, urls, no_pdf_dois, num_error_dois, dois_with_pdf, dois_without_pdf, dois_not_in_database , titles


def write_stats(urls_from_dois, urls, no_pdf_dois, num_error_dois, dois_with_pdf, dois_without_pdf, dois_not_in_database, empty_pdfs):
    '''
    Writes DOIs, URLs, and download rates into unpaywall_download_stats.txt
  
    Parameters
    ----------
    urls_from_dois : list
        A list of DOIs that successfully outputted a pdf.
    urls : list
        A list of the pdfs corresponding to the downloaded_dois list.
    no_pdf_dois : list
        A list of DOIs that did not successfully output a pdf.
    num_error_dois : list
        A list of DOIs that were not included in the database.
    dois_with_pdf : int
        Number of DOIs with pdf.
    dois_without_pdf : int
        Number of DOIs that did not have a corresponding pdf.
    dois_not_in_database  : int
        Number of DOIs not in the database.
  
    Returns
    -------
    None.
  
    '''
    with open('stats_upw_download_1.txt', 'w', encoding = 'utf-8') as f: ###### **NEXT NUMBER**
        f.write(f"DOIs with PDF: {dois_with_pdf}\nNot Downloaded: {dois_without_pdf}\n404 Error: {dois_not_in_database}\nEmpty PDFs: {len(empty_pdfs)}\n")
        f.write(f"Percent of DOIs with a PDF: {dois_with_pdf / (dois_with_pdf + dois_without_pdf + dois_not_in_database )}\n\n")
        
        f.write("DOIs with a PDF:\n")
        for i in range(len(urls_from_dois)):
            f.write(f"{urls_from_dois[i]}, {urls[i]}\n")
            
        f.write("\n")
        f.write("Not Downloaded DOIs:\n")
        for doi in no_pdf_dois:
            f.write(doi+"\n")
        
        f.write("\n")
        f.write("404 Error:\n")
        for doi in num_error_dois:
            f.write(doi+"\n")  
         
        f.write("\n")
        f.write("Empty PDFs:\n")
        for doi in empty_pdfs:
            f.write(doi+"\n")


def write_urls(urls):
    '''
    Writes a list of urls into upw_download_pdf.txt

    Parameters
    ----------
    urls_from_dois : list
        A list of DOIs that successfully outputted a url.
    urls : list
        A list of the urls corresponding to the urls_from_dois list.
    no_pdf_dois : list
        A list of DOIs that did not successfully output a pdf.
    num_error_dois : list
        A list of DOIs that were not included in the database.
    dois_with_pdf : int
        Number of DOIs with pdf.
    dois_without_pdf : int
        Number of DOIs that did not have a corresponding pdf.
    dois_not_in_database : int
        Number of DOIs not in the database.

    Returns
    -------
    None.

    '''
            
    with open('upw_list_of_urls.txt', 'a', encoding = 'utf-8') as f:       
        for i in range(len(urls)):
            f.write(f"{urls[i]}\n") 
            
 
def extract_text_pdf(pdf):
    '''
    Extracts the full text of the pdf
    
    Parameters
    ----------
    pdf : local file pdf
        pdf from local file.

    Returns
    -------
    text : string
        The full text of the pdf.

    '''
    # open pdf
    pdf = PdfReader(pdf)
    
    # initialize text
    text = ''
    
    # add text to string
    for page in pdf.pages:
        text += page.extract_text()
          
    return text
  
        
def download_pdf(pdf):
    '''
    Downloads the full text of the provided pdf

    Parameters
    ----------
    pdf_file : .txt
        List of pdfs

    Returns
    -------
    None.

    '''
    # gets pdf
    response = requests.get(pdf)
    
    # makes sure successful
    if response.status_code == 200: 
        # downloads to local file pdf
        with open('downloaded_file.pdf', 'wb') as f:
            f.write(response.content)

   
def run(doi_lst, upw_email):
    '''
    Run this for full program

    Parameters
    ----------
    doi_lst : list
        A list of all DOIs to iterate through.

    Returns
    -------
    new_doi_lst : list
        A list of the DOIs that didn't work for the next API to try

    '''
    error_chars = "\\/*?\"<>|:"
    
    # gets the info for each DOI
    url_info = get_urls(doi_lst, upw_email)
    urls_from_dois, urls, no_pdf_dois, num_error_dois, \
        dois_with_pdf, dois_without_pdf, dois_not_in_database, titles = url_info
    
    
    # initialize a new doi list for next API to try and add dois w no url
    new_doi_lst = no_pdf_dois
    
    # initialize list for empty pdfs
    empty_pdfs = []
    
    # add num_error_dois to the list for next API to try
    for i in range(len(num_error_dois)):
        new_doi_lst.append(num_error_dois[i])
        
    # writes the urls into 'upw_download_pdf_test.txt'
    write_urls(urls)  

    # define folder for all txt files to go to
    folder_name = "article_txt_1" ############################################# **RESET
         
    for i in range(len(urls)):
        url = urls[i]
        
        try: 
            # downloads pdf to local file "downloaded_file" temporarily
            download_pdf(url)

            # extract the text of the pdf
            pdf_txt = extract_text_pdf("downloaded_file.pdf")
            
            if len(pdf_txt) > 100:
                # define name of file
                file_name = f"{titles[i]}.txt"
                for char in error_chars:
                    file_name = file_name.replace(char, "")
                
                # add folder to path for file name
                file_path = os.path.join(folder_name, file_name)
                
                # add to txt file
                with open(file_path, 'w', encoding = 'utf-8') as f: 
                    f.write(f"Title: {titles[i]}\n")
                    f.write(f"URL: {url}\n")
                    f.write(f"DOI: {urls_from_dois[i]}\n")
                    f.write(pdf_txt)
                    f.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    
            else: 
                new_doi_lst.append(urls_from_dois[i])
                empty_pdfs.append(urls_from_dois[i])

        except SSLError:
            # add to list of dois to try for next API
            new_doi_lst.append(urls_from_dois[i])
            
            with open('not_downloading_upw_urls.txt', 'a', encoding = 'utf-8') as f: ## RESET
                f.write(f"SSLError with URL: {url}\n \
                        DOI: {urls_from_dois[i]}") 
            
        except UnicodeEncodeError:
            # add to list of dois to try for next API
            new_doi_lst.append(urls_from_dois[i])
            
            with open('not_downloading_upw_urls.txt', 'a', encoding = 'utf-8') as f:
                f.write(f"UnicodeEncodeError with URL: {url}\n \
                        DOI: {urls_from_dois[i]}")
                
        except Exception:
            # add to list of dois to try for next API
            new_doi_lst.append(urls_from_dois[i])
            
            with open('not_downloading_upw_urls.txt', 'a', encoding = 'utf-8') as f:
                f.write(f"EOF marker not found error for {url}\n \
                        DOI: {urls_from_dois[i]}")
    
    # write the stats for future reference
    write_stats(urls_from_dois, urls, no_pdf_dois, num_error_dois, \
        dois_with_pdf, dois_without_pdf, dois_not_in_database, empty_pdfs)
        
    return new_doi_lst
    

'''   
def main():
    # open file of DOIs and decide number to download
    doi_lst = dois.store_dois("one_of_each.txt")
    DOI_LST = dois.rand_dois(doi_lst, 10)
    
    # gets the urls
    url_info = get_urls(DOI_LST)
    
    # assign the returns to names
    urls_from_dois, urls, no_pdf_dois, num_error_dois, \
        dois_with_pdf, dois_without_pdf, dois_not_in_database, titles = url_info
     
    # write pdfs into a txt file ('upw_list_of_urls_test.txt')
    write_urls(urls)    
    

    # define folder for all txt to go to
    folder_name = "article_txt"
        
    
    for i in range(len(urls)):
        url = urls[i]
        
        try: 
            # downloads pdf to local file "downloaded_file" temporarily
            download_pdf(url)

            # extract the text of the pdf
            pdf_txt = extract_text_pdf("downloaded_file.pdf")
            
            # define name of file
            file_name = f"{titles[i]}.txt"
            
            # add folder to path for file name
            file_path = os.path.join(folder_name, file_name)
            
            # add to txt file
            with open(file_path, 'w', encoding = 'utf-8') as f:
                f.write(f"Title: {titles[i]}\n")
                f.write(f"URL: {url}\n")
                f.write(pdf_txt)
                f.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
              
            
        except SSLError:
            with open('upw_urls_not_downloading.txt', 'a', encoding = 'utf-8') as f:
                f.write(f"SSLError with URL: {url}\n")
            
        except UnicodeEncodeError:
            with open('upw_urls_not_downloading.txt', 'a', encoding = 'utf-8') as f:
                f.write(f"UnicodeEncodeError with URL: {url}\n")
                
        except Exception:
            with open('upw_urls_not_downloading.txt', 'a', encoding = 'utf-8') as f:
                f.write(f"EOF marker not found error for {url}\n")

'''  

        
        
        