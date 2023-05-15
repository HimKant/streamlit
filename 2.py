import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd


def search_for_terms(url, search_terms):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for term in search_terms:
        for tag in soup.find_all(string=lambda text: term.lower() in text.lower()):
            if tag.parent.name == "a" and tag.parent.get("href") not in results:
                results.append((term, tag.parent.get("href")))
    return results


st.title("Website Keyword Search Tool")
url = st.text_input("Enter a website URL (e.g. https://www.example.com):")
search_terms = st.text_input("Enter search keywords separated by commas:")

if st.button("Search"):
    if not url:
        st.error("Please enter a website URL.")
    elif not search_terms:
        st.error("Please enter at least one search keyword.")
    else:
        search_terms = [term.strip() for term in search_terms.split(",")]
        results = search_for_terms(url, search_terms)
        if not results:
            st.warning("No results found.")
        else:
            st.success("Results found:")
            data = {"Keyword": [r[0] for r in results], "Link": [r[1] for r in results]}
            df = pd.DataFrame(data)
            st.table(df)