import json
import re
import os
import sys
import itertools
import time
import pandas as pd
from transformers import pipeline
from tqdm import tqdm
from typing import Tuple
from base_analyzer import BaseAnalyzer


# ==== MODEL SETTINGS ====
CONFIDENCE_THRESHOLD = 0.6
MIN_TEXT_LENGTH = 30
MAX_TEXT_LENGTH = 1000
# ========================


class TelegramAnalyzer(BaseAnalyzer):
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.posts = json.load(f)
        print(f"Loaded {len(self.posts)} posts from {os.path.basename(json_file)}")

        print("Loading model - ", end=" ", flush=True)
        spinner = itertools.cycle(['|', '/', '-', '\\'])
        for _ in range(30):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
        self.classifier = pipeline(
            "zero-shot-classification",
            model="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
            device=0
        )
        print("OK")

        self.categories = [
            "волонтёрство и добровольческая помощь",
            "патриотизм и историческая память (бессмертный полк, 9 мая, ветераны)",
            "военные действия и помощь фронту",
            "государственная политика и выборы",
            "образование и молодёжная политика",
            "социальные проблемы (медицина, пенсии, ЖКХ)",
            "экономика и бюджет",
            "чрезвычайные происшествия",
            "экология и климат",
            "наука и технологии",
            "культура (театры, музеи, концерты)",
            "спорт",
            "развлечения и юмор",
            "личное и бытовое"
        ]
        self.non_social = ["развлечения и юмор", "личное и бытовое"]

        self.stop_words = {
            'bezposhady', 'artemmetelev', 'https', 'http', 'com', 'ru', 'ua', 'by', 'kz',
            'это', 'все', 'так', 'вот', 'который', 'еще', 'уже', 'быть', 'сказать',
            'стать', 'очень', 'можно', 'нужно', 'там', 'тут', 'потом', 'тогда', 'себя',
            'свой', 'эти', 'этот', 'как', 'для', 'без', 'до', 'по', 'из', 'за', 'от',
            'у', 'о', 'об', 'при', 'между', 'через', 'или', 'и', 'в', 'на', 'с', 'к',
            'а', 'но', 'что', 'чтобы', 'год', 'года', 'лет', 'рублей', 'тысяч', 'миллионов',
            'добро', 'сегодня', 'вместе', 'регионов', 'поддержку', 'центров', 'участие',
            '2022', '2023', '2024', '2025', '2026', 'мывместе'
        }

        self.df = None

    @staticmethod
    def clean_text(text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r'\b[a-z0-9]{10,}\b', '', text)
        text = re.sub(r'bezposhady|artemmetelev', '', text)
        text = re.sub(r'[^a-zа-яё\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def classify_post(self, text: str) -> Tuple[str, float]:
        if len(text) < MIN_TEXT_LENGTH:
            return "недостаточно данных", 0.0
        clean = self.clean_text(text)
        if len(clean) < MIN_TEXT_LENGTH:
            return "недостаточно данных", 0.0
        try:
            result = self.classifier(clean[:MAX_TEXT_LENGTH], self.categories)
            return result['labels'][0], result['scores'][0]
        except Exception as e:
            print(f"Error: {e}")
            return "error", 0.0

    def analyze(self, confidence_threshold: float = CONFIDENCE_THRESHOLD):
        print("Classifying posts...")
        results = []

        for post in tqdm(self.posts, desc="Classifying", unit="post"):
            text = post.get('text', '')
            topic, confidence = self.classify_post(text)
            results.append({
                'text': text[:400],
                'date': post.get('date', ''),
                'views': post.get('views', 0),
                'topic': topic,
                'confidence': confidence,
                'is_social': (confidence >= confidence_threshold and topic not in self.non_social)
            })

        self.df = pd.DataFrame(results)
        return self.df

    def get_socially_significant(self):
        if self.df is None:
            raise ValueError("Call analyze() first")
        return self.df[self.df['is_social'] == True]

    def print_stats(self):
        if self.df is None:
            print("Call analyze() first")
            return
        significant = self.get_socially_significant()
        print("\n___STATISTICS___\n")
        print(f"Total posts: {len(self.df)}")
        print(f"Socially significant: {len(significant)} ({len(significant) / len(self.df) * 100:.1f}%)")

