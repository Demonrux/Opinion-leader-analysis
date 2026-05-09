# Social Posts Analyzer

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Transformers](https://img.shields.io/badge/-Transformers-yellow)](https://huggingface.co/)

**Система для сбора, классификации и визуализации постов из Telegram-каналов с выделением социально значимых тем.**

Проект предназначен для автоматического анализа контента Telegram-каналов (в частности, лидеров общественного мнения) с использованием Zero-Shot классификации и построением наглядных графиков.

---

## Возможности

| Функция | Описание |
|---------|----------|
| **Парсинг** | Сбор постов из публичных открытых каналов через API |
| **Классификация** | Zero-Shot модель `mDeBERTa-v3` определяет тему поста (политика, волонтёрство, экология и др.) |
| **Визуализация** | Построение графиков: распределение тем, просмотры, хронология |
| **Аналитика** | Сравнение динамики подписчиков с виральностью постов |
| **Экспорт** | Сохранение результатов в JSON и PNG |

---

## Архитектура
<img width="911" height="1097" alt="image" src="https://github.com/user-attachments/assets/3991be5d-30de-47b0-b21c-a7ce0e3e23df" />

## Настройка параметров

| Параметр | Файл | Описание |
|----------|------|----------|
| `API_ID`, `API_HASH`, `PHONE` | `main.py` / `config.py` | Данные из [my.telegram.org](https://my.telegram.org) |
| `CHANNEL` | `main.py` | Имя канала для парсинга (например, `durov`) |
| `POSTS_LIMIT` | `main.py` | Максимум постов для сбора (до 1000) |
| `CONFIDENCE_THRESHOLD` | `analyze()` | Порог уверенности модели (0.3-0.7) |
| `COLORS` | `config.py` | Цветовая схема графиков |
| `STOP_WORDS` | `config.py` | Стоп-слова для очистки текста |
| `OUTPUT_DIR` | `config.py` | Папка для сохранения результатов |

## Технологии

| Библиотека | Назначение | Версия |
|------------|------------|--------|
| `telethon` | Асинхронный парсинг Telegram API | 1.34+ |
| `transformers` | Zero-Shot классификация (Hugging Face) | 4.30+ |
| `pandas` | Обработка и группировка данных | 1.5+ |
| `matplotlib` | Построение графиков | 3.5+ |
| `seaborn` | Улучшенная визуализация | 0.12+ |
| `wordcloud` | Облако ключевых слов | 1.9+ |
| `scikit-learn` | Векторизация текста (LDA) | 1.2+ |
| `torch` | Бэкенд для модели | 2.0+ |
| `tqdm` | Прогресс-бары | 4.65+ |

### Пример результатов

<img width="2379" height="1330" alt="image" src="https://github.com/user-attachments/assets/6d649234-7b58-4687-a45e-16a29a711acd" />

<img width="1800" height="900" alt="image" src="https://github.com/user-attachments/assets/dee93958-1d23-4b7a-bbbd-9dab9e425986" />

<img width="1800" height="900" alt="image" src="https://github.com/user-attachments/assets/23da9b36-2aa1-44ba-ac0d-c0d0d9e41a0c" />

<img width="2383" height="1180" alt="image" src="https://github.com/user-attachments/assets/56c9a3a1-ff43-474c-83ff-6b6dc192d273" />



