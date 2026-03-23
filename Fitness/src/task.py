import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def load_tasks(csv_file):
    df = pd.read_csv(csv_file)
    tasks = df.to_dict('records')
    return tasks

def top_10_tasks(csv_file):
    task = load_tasks(csv_file)
    lottery = random.sample(task,10)
    for i,item in enumerate(lottery):
        print(f"{i+1}. {item['task_name']}")

def find_similar_task(user_input,tasks):
    task_names = [t['task_name'] for t in tasks]

    vectorizer = TfidfVectorizer()
    all_text = task_names+[user_input]
    tfidf_matrix = vectorizer.fit_transform(all_text)

    # user input is last row
    user_vec = tfidf_matrix[-1]
    task_vec = tfidf_matrix[:-1]

    scores = cosine_similarity(user_vec,task_vec)[0]
    best_index = scores.argmax()
    best_score = scores[best_index]

    if best_score>0.3:
        return tasks[best_index]
    return None