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
    vectorizer = TfidfVectorizer().fit_transform(texts)
    pairwise_similarity = cosine_similarity(vectorizer)
    return pairwise_similarity.mean()



def score_keyword_distribution(url):
    """Return the relevancy scores of the h-tags in the HTML of the given URL."""
    html = get_html(url)
    scores = defaultdict(list)
    prev_tag_contents = {tag: [] for tag in ['h1', 'h2', 'h3', 'h4', 'h5']}
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        contents = get_tag_contents(html, tag)
        for content in contents:
            if tag != 'h1':
                prev_tag = f'h{int(tag[1]) - 1}'
                scores[f'{prev_tag}-{tag}'].append(calculate_similarity(prev_tag_contents[prev_tag] + [content]))
            prev_tag_contents[tag].append(content)
    avg_scores = {tag_pair: sum(scores) / len(scores) for tag_pair, scores in scores.items() if scores}
    return avg_scores

    
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
    scores = {}
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        contents = get_tag_contents(html, tag)
        if contents:  # check if contents is not empty
            scores[tag] = calculate_similarity(contents)
        else:
            scores[tag] = 0  # assign default score if contents is empty
    return scores

# Streamlit code
st.title('SEO Keyword Distribution Scorer')
url = st.text_input('Enter a URL', '')
if url:
    scores = score_keyword_distribution(url)
    st.write(scores)
