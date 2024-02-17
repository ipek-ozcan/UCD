import requests
import urllib.request as libreq
import json
from bs4 import BeautifulSoup
import dois
import doi_scraper_unpaywall
import os
from PyPDF2 import PdfReader
from requests.exceptions import SSLError
import urllib.parse

'''
- Define separate client for each API in the list provided
- For each API, iterate through the DOIs
     - if the article from the DOI is fully downloaded, remove it from
       the list of DOIs
     - move onto the next API for the rest of the DOIs
     - continue this until either there are no DOIs left in the list
       or all of the APIs have been used
   
   OR
   
-For each DOI, iterate through the APIs
     - if the API works and the article is fully downloaded, add that DOI 
        to a list and move on to the next DOI
     - continue this until all of the DOIs have been iterated through
- Keep a record of which DOIs worked for which APIs in case something 
  goes wrong  
'''

def run(doi_lst, titles_for_next):
    titles = list(titles_for_next.values())
    folder_name = "article_txt_arxiv" ######################################### **RESET
    working_dois = []
    new_doi_lst = []
    empty_pdfs = []
    no_pdf = []
    no_article = []
    error_chars = "\\/*?\"<>|:"
    
    for i in range(len(titles)):  
                   
        title = titles[i]
        
        title_url = urllib.parse.quote_plus(title)
        # search url, get request, beautiful soup parse
        url = f'http://export.arxiv.org/api/query?search_query=ti:{title_url}&start=0&max_results=1'
        
        response = requests.get(url)
        
        soup = BeautifulSoup(response.content, 'xml')
        
        if response is not None:
            
            # find entry element 
            pdf_find = soup.find('link', rel = "alternate", type = 'text/html')
            
            # if link element found
            if pdf_find:
                pdf_link = pdf_find['href']
                
                # if link to find pdf is found, gather html content
                if pdf_link:
                    response = requests.get(pdf_link)
                    
                    if response.status_code == 200:
                        html_content = response.text
                
                # parse through html_content
                soup = BeautifulSoup(html_content, 'html.parser')
                pdf_element = soup.find('span', class_ = 'arxivid')
                
                # retrieve pdf link if available
                if pdf_element:
                    pdf_body = pdf_element.a.get_text(strip=True)
                    pdf_body = pdf_body.replace("arXiv:", "")
                    pdf_url = "https://arxiv.org/pdf/" + pdf_body + ".pdf"
                
                # if pdf link found, download full text
                if pdf_url: 
                   try: 
                       # downloads pdf to local file "downloaded_file" temporarily
                       doi_scraper_unpaywall.download_pdf(pdf_url)
    
                       # extract the text of the pdf
                       pdf_txt = doi_scraper_unpaywall.extract_text_pdf("downloaded_file.pdf")
    
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
                               f.write(f"PDF link: {pdf_url}")
                               f.write("\n")
                               f.write(f"URL: {url}\n")
                               f.write(f"DOI: {doi_lst[i]}\n")
                               f.write(pdf_txt)
                               f.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
                           working_dois.append(doi_lst[i])
                               
                       else: 
                           new_doi_lst.append(doi_lst[i])
                           empty_pdfs.append(doi_lst[i])

                       
                   except SSLError:
                       # add to list of dois to try for next API
                       new_doi_lst.append(doi_lst[i])
                       no_pdf.append(doi_lst[i])
                       with open('not_downloading_arxiv_urls.txt', 'a', encoding = 'utf-8') as f: ## **RESET
                           f.write(f"SSLError with URL: {url}\n") 
    
                   except UnicodeEncodeError:
                       # add to list of dois to try for next API
                       new_doi_lst.append(doi_lst[i])
                       no_pdf.append(doi_lst[i])
                       with open('not_downloading_arxiv_urls.txt', 'a', encoding = 'utf-8') as f:
                           f.write(f"UnicodeEncodeError with URL: {url}\n")
    
                   except Exception:
                       # add to list of dois to try for next API
                       new_doi_lst.append(doi_lst[i])
                       no_pdf.append(doi_lst[i])
                       with open('not_downloading_arxiv_urls.txt', 'a', encoding = 'utf-8') as f:
                           f.write(f"EOF marker not found error for {url}\n")
                   
                
            else:
                no_pdf.append(doi_lst[i])
                with open('arxiv_urls_not_downloading.txt', 'a', encoding = 'utf-8') as f:
                    f.write(f"No PDF for DOI: {doi_lst[i]}\n")
            
        else:
            no_article.append(doi_lst[i])
            with open('arxiv_urls_not_downloading.txt', 'a', encoding = 'utf-8') as f:
                f.write(f"Couldn't find an article with DOI {doi_lst[i]}\n")

    
    with open('stats_arxiv.txt','w', encoding = 'utf-8') as f: ################ **NEXT NUMBER**
      
        f.write(f"Number of DOIs with a PDF: {len(working_dois)} \n")
        f.write(f"Number of DOIs without a PDF: {len(no_pdf)} \n")
        f.write(f"Number of DOIs not found: {len(no_article)} \n")
        
        f.write(f"DOIs with a PDF: {len(working_dois)}\n")
        for i in range(len(working_dois)):
            f.write(f"{working_dois[i]}\n")
            
        f.write("\n")
        f.write(f"No PDF DOIs: {len(no_pdf)}\n")
        for doi in no_pdf:
            f.write(doi+"\n")
        
        f.write("\n")
        f.write(f"Article Not Found: {len(no_article)}\n")
        for doi in no_article:
            f.write(doi+"\n")  
         
        f.write("\n")
        f.write(f"Empty PDFs: {len(empty_pdfs)}\n")
        for doi in empty_pdfs:
            f.write(doi+"\n")
   
    return new_doi_lst 
        




















