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
    headings = [(tag.name, tag.get_text(strip=True)) for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    print(f"Headings: {headings}")  # Debug print
    scores = []
    last_heading = [None, None, None, None, None, None]
    for i in range(len(headings)):
        level = int(headings[i][0][1]) - 1
        if level > 0 and last_heading[level-1] is not None:
            score = calculate_similarity([last_heading[level-1][1], headings[i][1]])
            scores.append((last_heading[level-1][0], last_heading[level-1][1], headings[i][0], headings[i][1], score))
        last_heading[level] = headings[i]
    print(f"Scores: {scores}")  # Debug print
    return scores

# Streamlit code
st.title('SEO Keyword Distribution Scorer')
url = st.text_input('Enter a URL', '')
if url:
    scores = score_keyword_distribution(url)
    output = ""

    # Find h1 tag and add it to the output
    h1_tag = [tag for tag in scores if tag[0] == 'h1']
    if h1_tag:
        output += f"**{h1_tag[0][0]} ({h1_tag[0][1]})**\n\n"

    for parent_tag, parent_text, child_tag, child_text, score in scores:
        indent = "    " * (int(child_tag[1]) - 1)
        output += f"{indent}- **{child_tag} ({child_text})**: {score:.2f} (relevancy to {parent_tag} '{parent_text}')\n"
    st.markdown(output)

