import json
import os
import re
from collections import defaultdict

def load_concepts(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    concepts = []
    for section in data:
        for concept in section.get("concepts", []):
            concepts.append({
                "id": concept["id"],
                "lemmas": [l.lower() for l in concept.get("lemmas", [])]
            })
    return concepts


def read_article(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().lower()


def tokenize(text):
    # простая токенизация
    return re.findall(r'\w+', text.lower())


def score_article(article_tokens, lemmas):
    # считаем, сколько лемм встретилось
    score = 0
    token_set = set(article_tokens)
    
    for lemma in lemmas:
        if lemma in token_set:
            score += 1
    
    return score


def match_articles(concepts, articles_dir, threshold=2):
    result = defaultdict(list)
    
    for root, _, files in os.walk(articles_dir):
        for file in files:
            if not file.endswith(('.md', '.txt')):
                continue
            
            path = os.path.join(root, file)
            text = read_article(path)
            tokens = tokenize(text)
            
            for concept in concepts:
                score = score_article(tokens, concept["lemmas"])
                
                if score >= threshold:
                    result[concept["id"]].append(path)
    
    return result


if __name__ == "__main__":
    # "../../../WEB/2.1_society/how_and_where_find_friends/articles"
    concepts_path = "./concepts.json"
    articles_dir = "../../../WEB/5.1_technology_and_digital_literacy/information and media literacy/articles"

    concepts = load_concepts(concepts_path)
    matches = match_articles(concepts, articles_dir)

    print(json.dumps(matches, ensure_ascii=False, indent=2))