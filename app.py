python -m pip install --upgrade pip
pip install beautifulsoup4 
# Import necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_html(url):
    """Return the HTML content of the given URL."""
    response = requests.get(url)
    return response.text

def get_tag_contents(html, tag):
    """Return a list of contents of the given tag in the HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    return [tag.get_text() for tag in soup.find_all(tag)]

def calculate_similarity(texts):
    """Return the average cosine similarity of the given texts."""
    vectorizer = TfidfVectorizer().fit_transform(texts)
    pairwise_similarity = cosine_similarity(vectorizer)
    return pairwise_similarity.mean()

def score_keyword_distribution(url):
    """Return the relevancy scores of the h-tags in the HTML of the given URL."""
    html = get_html(url)
    scores = {}
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        contents = get_tag_contents(html, tag)
        scores[tag] = calculate_similarity(contents)
    return scores

# Streamlit code
st.title('SEO Keyword Distribution Scorer')
url = st.text_input('Enter a URL', '')
if url:
    scores = score_keyword_distribution(url)
    st.write(scores)
