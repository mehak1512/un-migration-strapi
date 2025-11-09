# main.py
from crawler import crawl_site
from llama_parser import summarize_with_llama
from push_to_strapi import push_to_strapi

def main():
    pages = crawl_site()

    for page in pages:
        print(f"Processing: {page['url']}")
        summary = summarize_with_llama(page["content"], page["url"])
        push_to_strapi(summary)

if __name__ == "__main__":
    main()
