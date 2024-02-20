import dois
import doi_scraper_unpaywall
import doi_scraper_elsapy
import doi_scraper_arxiv

# define all external information needed
## update config.json with personal api key through https://dev.elsevier.com/
upw_email = "ipekozcan2004@gmail.com"

## name of folder for txt files of full text of each article
folder_name = "article_txt_1"


# replace with txt file of DOIs (one DOI per line)
doi_lst = dois.store_dois("dois.txt")

# uncomment to decide number of DOIs from file to download (if applicable)
#DOI_LST = doi_lst[:100000]

DOI_LST = dois.rand_dois(doi_lst, 1000)

# try on unpaywall then get new DOI_LST
DOI_LST = doi_scraper_unpaywall.run(DOI_LST, upw_email)
#print(len(DOI_LST))

# try on elsapy then get new DOI_LST
DOI_LST, titles_for_next = doi_scraper_elsapy.run(DOI_LST)
#print(len(DOI_LST))

# try on arXiv
doi_scraper_arxiv.run(DOI_LST, titles_for_next)



