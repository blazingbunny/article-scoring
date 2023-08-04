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

def calculate_similarity(text1, text2):
    """Return whether text2 contains any of the words from text1."""
    text1_words = set(text1.lower().split())
    text2_words = set(text2.lower().split())
    common_words = text1_words & text2_words
    return len(common_words) / len(text1_words)

def score_keyword_distribution(url):
    """Return the relevancy scores of the h-tags and p-tags in the HTML of the given URL."""
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    headings = [(tag.name, tag.get_text(strip=True)) for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    paragraphs = [(tag.name, tag.get_text(strip=True)) for tag in soup.find_all('p')]
    print(f"Headings: {headings}")  # Debug print
    scores = []
    last_heading = [None, None, None, None, None, None]
    for i in range(len(headings)):
        level = int(headings[i][0][1]) - 1  # Level for headings
        if level > 0 and last_heading[level-1] is not None:
            score = calculate_similarity(last_heading[level-1][1], headings[i][1])
            scores.append((last_heading[level-1][0], last_heading[level-1][1], headings[i][0], headings[i][1], score))
        last_heading[level] = headings[i]
    for i in range(len(paragraphs)):  # Level for paragraphs
        score = calculate_similarity(last_heading[5][1], paragraphs[i][1])  # Compare paragraph with last h6 heading
        scores.append((last_heading[5][0], last_heading[5][1], paragraphs[i][0], paragraphs[i][1], score))
    print(f"Scores: {scores}")  # Debug print
    return scores



import pandas as pd

# Streamlit code
st.title('SEO Keyword Distribution Scorer')
url = st.text_input('Enter a URL', '')
if url:
    scores = score_keyword_distribution(url)

    # Convert scores to a DataFrame
    df_scores = pd.DataFrame(scores, columns=['Parent Tag', 'Parent Text', 'Child Tag', 'Child Text', 'Score'])

    # Display the DataFrame as a table
    st.table(df_scores)
