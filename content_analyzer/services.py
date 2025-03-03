# services.py
from django.conf import settings
from transformers import pipeline
from keybert import KeyBERT
import torch
import numpy as np
from .models import ContentAnalysis, ContentKeyword, ContentHashtag
import re

class ContentAnalyzerService:
    def __init__(self):
        self.initialize_models()

    def initialize_models(self):
        """Initialize ML models with error handling"""
        try:
            self.sentiment_analyzer = pipeline("sentiment-analysis", 
                model="distilbert-base-uncased-finetuned-sst-2-english")
            self.kw_model = KeyBERT("sentence-transformers/all-MiniLM-L6-v2")
            self.toxicity_classifier = pipeline("text-classification", 
                model="martin-ha/toxic-comment-model")
        except Exception as e:
            print(f"Error initializing models: {e}")
            # Use simpler fallback methods if models fail to load

    def analyze_content(self, user, content, post_type='general'):
        """Main analysis method that creates and returns a ContentAnalysis instance"""
        try:
            # Perform basic analysis
            sentiment_result = self._analyze_sentiment(content)
            safety_result = self._check_content_safety(content)
            engagement_score = self._calculate_engagement_score(content)
            
            # Create ContentAnalysis instance
            analysis = ContentAnalysis.objects.create(
                user=user,
                content=content,
                post_type=post_type,
                sentiment=sentiment_result['label'],
                engagement_score=engagement_score['total_score'],
                safety_score=safety_result['toxicity_score'],
                is_safe=safety_result['is_safe'],
                improved_content=self._optimize_content(content, post_type)
            )

            # Save related data
            self._save_keywords(analysis)
            self._save_hashtags(analysis)

            return analysis

        except Exception as e:
            print(f"Error in content analysis: {e}")
            return None

    def _save_keywords(self, analysis):
        """Save extracted keywords to database"""
        keywords = self._extract_keywords(analysis.content)
        for kw in keywords:
            ContentKeyword.objects.create(
                analysis=analysis,
                keyword=kw,
                score=0.0  # You can add actual scoring logic here
            )

    def _save_hashtags(self, analysis):
        """Save hashtags to database"""
        hashtags = self._analyze_hashtags(analysis.content)
        for tag in hashtags['hashtags']:
            ContentHashtag.objects.create(
                analysis=analysis,
                hashtag=tag,
                is_suggested=False
            )

    # Analysis methods from original class, modified for Django
    def _analyze_sentiment(self, content):
        try:
            result = self.sentiment_analyzer(content)[0]
            return {
                'label': result['label'],
                'score': result['score']
            }
        except Exception:
            return {'label': 'neutral', 'score': 0.5}

    def _check_content_safety(self, content):
        try:
            result = self.toxicity_classifier(content)[0]
            return {
                'is_safe': result['label'] == 'neutral',
                'toxicity_score': result['score']
            }
        except Exception:
            return {'is_safe': True, 'toxicity_score': 0.0}

    def _calculate_engagement_score(self, content):
        # Simplified scoring for example
        length_score = min(1.0, len(content) / 500)
        hashtag_score = len(re.findall(r'#\w+', content)) / 10
        
        total_score = (length_score + hashtag_score) / 2
        return {
            'total_score': total_score,
            'breakdown': {
                'length_score': length_score,
                'hashtag_score': hashtag_score
            }
        }

    def _extract_keywords(self, content, top_n=5):
        try:
            keywords = self.kw_model.extract_keywords(
                content,
                keyphrase_ngram_range=(1, 2),
                stop_words='english',
                top_n=top_n
            )
            return [kw[0] for kw in keywords]
        except Exception:
            return []

    def _analyze_hashtags(self, content):
        hashtags = re.findall(r'#\w+', content)
        return {
            'hashtags': hashtags,
            'count': len(hashtags)
        }

    def _optimize_content(self, content, post_type):
        # Add basic content optimization logic here
        return content