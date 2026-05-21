# MindBridge AI Wellness Agent

An AI-powered wellness companion that supports mental health through empathetic conversations, mood tracking, and personalized guidance.

## Overview

MindBridge engages users in supportive dialogue, identifies emotional patterns, and offers evidence-based wellness recommendations while prioritizing privacy and ethical AI practices.

> **Note:** This is a wellness support tool, not a substitute for professional mental health care.

## Features

- Empathetic AI conversations via large language models
- Mood and sentiment tracking over time
- Personalized wellness insights
- Crisis detection with resource referrals
- Privacy-first design with local processing options

## Tech Stack

Python | LangChain | OpenAI API | scikit-learn | TensorFlow | FastAPI | SQLite/PostgreSQL | React/Streamlit

## Getting Started

```bash
git clone https://github.com/hinahammad/mindbridge-ai-wellness.git
cd mindbridge-ai-wellness
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn api.main:app --reload
