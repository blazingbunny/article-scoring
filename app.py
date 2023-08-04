# Import necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

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
    if texts and any(t.strip() for t in texts):  # Check if texts is not empty and contains more than just whitespace
        vectorizer = TfidfVectorizer().fit_transform(texts)
        pairwise_similarity = cosine_similarity(vectorizer)
        return pairwise_similarity.mean()
    else:
        return 0

def score_keyword_distribution(url):
    """Return the relevancy scores of the h-tags in the HTML of the given URL."""
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    headings = [(tag.name, tag.get_text()) for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    print(f"Headings: {headings}")  # Debug print
    scores = []
    for i in range(1, len(headings)):
        if int(headings[i][0][1]) > int(headings[i-1][0][1]):
            score = calculate_similarity([headings[i-1][1], headings[i][1]])
            scores.append((headings[i-1][0], headings[i-1][1], headings[i][0], headings[i][1], score))
    print(f"Scores: {scores}")  # Debug print
    return scores

# Streamlit code
st.title('SEO Keyword Distribution Scorer')
url = st.text_input('Enter a URL', '')
if url:
    scores = score_keyword_distribution(url)
    st.text(scores)
