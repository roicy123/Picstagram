from django.core.exceptions import ValidationError
from django.conf import settings
import requests
import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import tensorflow as tf
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob
from PIL import Image
import io
import logging

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ContentAnalyzer:
    """
    Content analyzer for social media posts.
    Analyzes text and images for reach optimization and inappropriate content.
    """
    def __init__(self):
        # Load pre-trained models
        self.toxicity_model = self._load_toxicity_model()
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.sentiment_model = TextBlob
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize image analysis model
        self.image_model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=True)
        self.image_labels = self._load_imagenet_labels()
        
        # Hashtag and keyword popularity data (would be updated periodically)
        self.popular_hashtags = self._load_popular_hashtags()
        
        # Inappropriate content patterns
        self.inappropriate_patterns = [
            r'(?i)\b(porn|explicit|nude|obscene)\b',
            r'(?i)\b(hate|racist|sexist|discriminat)\w*\b',
            r'(?i)\b(violence|assault|attack)\w*\b',
            # Add more patterns as needed
        ]

    def _load_toxicity_model(self):
        """Load pre-trained toxicity detection model"""
        try:
            model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
            return model
        except Exception as e:
            logger.error(f"Failed to load toxicity model: {e}")
            return None

    def _load_imagenet_labels(self):
        """Load ImageNet labels for image classification"""
        try:
            labels_path = tf.keras.utils.get_file(
                'ImageNetLabels.txt',
                'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
            with open(labels_path) as f:
                labels = f.readlines()
            return [l.strip() for l in labels]
        except Exception as e:
            logger.error(f"Failed to load ImageNet labels: {e}")
            return []

    def _load_popular_hashtags(self):
        """Load current popular hashtags (would be updated periodically)"""
        # In a real implementation, this would fetch from an API or database
        return {
            "photography": 0.9,
            "nature": 0.85,
            "travel": 0.83,
            "food": 0.82,
            "fitness": 0.8,
            "sunset": 0.78,
            "art": 0.77,
            "style": 0.76,
            "summer": 0.75,
            "beauty": 0.74,
        }

    def analyze_text(self, text):
        """Analyze text content for optimization and inappropriate content"""
        results = {
            "is_appropriate": True,
            "recommendations": [],
            "sentiment_score": 0,
            "reach_score": 0,
            "suggested_hashtags": [],
            "issues": []
        }
        
        # Check for inappropriate content
        for pattern in self.inappropriate_patterns:
            if re.search(pattern, text):
                results["is_appropriate"] = False
                results["issues"].append("Detected potentially inappropriate content")
                break
        
        # Sentiment analysis
        sentiment = self.sentiment_model(text)
        results["sentiment_score"] = sentiment.sentiment.polarity
        
        # If extremely negative, flag it
        if results["sentiment_score"] < -0.7:
            results["recommendations"].append("Consider using more positive language to improve engagement")
        
        # Text length analysis
        words = word_tokenize(text)
        if len(words) < 5:
            results["recommendations"].append("Caption is too short. Longer captions tend to get more engagement")
        elif len(words) > 200:
            results["recommendations"].append("Caption is very long. Consider shortening to improve readability")
        
        # Hashtag analysis
        hashtags = re.findall(r'#(\w+)', text)
        if not hashtags:
            results["recommendations"].append("Add relevant hashtags to increase visibility")
        elif len(hashtags) > 30:
            results["recommendations"].append("Too many hashtags may look spammy. Limit to 5-15 relevant hashtags")
        
        # Suggest popular hashtags based on content
        content_words = [w.lower() for w in words if w.lower() not in self.stop_words and len(w) > 3]
        for word in content_words:
            if word in self.popular_hashtags and word not in hashtags:
                results["suggested_hashtags"].append(word)
        
        # Calculate reach score (simplified)
        reach_factors = [
            0.7 if 5 <= len(words) <= 100 else 0.3,  # Length factor
            0.8 if 5 <= len(hashtags) <= 15 else 0.4,  # Hashtag factor
            0.7 if results["sentiment_score"] > 0 else 0.5,  # Sentiment factor
        ]
        results["reach_score"] = sum(reach_factors) / len(reach_factors)
        
        return results

    def analyze_image(self, image_file):
        """Analyze image content for optimization and inappropriate content"""
        results = {
            "is_appropriate": True,
            "recommendations": [],
            "content_classification": [],
            "reach_score": 0,
            "issues": []
        }
        
        try:
            # Process image
            img = Image.open(image_file)
            img = img.convert('RGB')
            img = img.resize((224, 224))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
            img_array = tf.expand_dims(img_array, 0)
            
            # Run image classification
            predictions = self.image_model.predict(img_array)
            top_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)[0]
            
            # Check for inappropriate content
            problematic_categories = ['bikini', 'brassiere', 'negligee', 'weapon', 'gun', 'knife', 'rifle', 'revolver', 'assault_rifle', 'firearm']
            for _, label, score in top_predictions:
                results["content_classification"].append({"label": label, "score": float(score)})
                if label in problematic_categories and score > 0.3:
                    results["is_appropriate"] = False
                    results["issues"].append(f"Detected potentially inappropriate content ({label})")
            
            # Image quality analysis
            width, height = img.size
            if width < 800 or height < 800:
                results["recommendations"].append("Image resolution is low. Higher resolution images perform better")
            
            # Calculate reach score (simplified)
            reach_factors = [
                0.8 if width >= 1080 and height >= 1080 else 0.5,  # Resolution factor
                0.7,  # Placeholder for aesthetic score
            ]
            results["reach_score"] = sum(reach_factors) / len(reach_factors)
            
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            results["issues"].append(f"Failed to analyze image: {str(e)}")
            results["is_appropriate"] = False  # Fail safe
        
        return results

    def analyze_post(self, text, image_file=None):
        """Analyze full post content (text and image)"""
        results = {
            "is_appropriate": True,
            "recommendations": [],
            "reach_score": 0,
            "text_analysis": None,
            "image_analysis": None
        }
        
        # Analyze text
        if text:
            text_results = self.analyze_text(text)
            results["text_analysis"] = text_results
            results["recommendations"].extend(text_results["recommendations"])
            if not text_results["is_appropriate"]:
                results["is_appropriate"] = False
        
        # Analyze image
        if image_file:
            image_results = self.analyze_image(image_file)
            results["image_analysis"] = image_results
            results["recommendations"].extend(image_results["recommendations"])
            if not image_results["is_appropriate"]:
                results["is_appropriate"] = False
        
        # Calculate overall reach score
        if text and image_file:
            results["reach_score"] = (results["text_analysis"]["reach_score"] + results["image_analysis"]["reach_score"]) / 2
        elif text:
            results["reach_score"] = results["text_analysis"]["reach_score"]
        elif image_file:
            results["reach_score"] = results["image_analysis"]["reach_score"]
        
        # Deduplicate recommendations
        results["recommendations"] = list(set(results["recommendations"]))
        
        return results

    def use_external_api(self, text=None, image_url=None):
        """Use Sightengine API for content analysis"""
        if not hasattr(settings, 'CONTENT_ANALYSIS_API_KEY') or not hasattr(settings, 'CONTENT_ANALYSIS_API_SECRET'):
            return {"error": "API credentials not configured"}

        api_user = settings.CONTENT_ANALYSIS_API_KEY
        api_secret = settings.CONTENT_ANALYSIS_API_SECRET
        endpoint = "https://api.sightengine.com/1.0/check.json"

        payload = {
            "api_user": api_user,
            "api_secret": api_secret,
        }

        if text:
            payload["text"] = text  # Sightengine doesn't natively support text moderation, so consider an alternative API.

        if image_url:
            payload["url"] = image_url
            payload["models"] = "nudity, offensive, weapon, gore"  # Adjust models based on your needs

        try:
            response = requests.get(endpoint, params=payload)
            result = response.json()
            return result
        except Exception as e:
            logger.error(f"Error using Sightengine API: {e}")
            return {"error": str(e)}



# Django integration
def validate_content(text=None, image=None):
    """Content validation function to be used in forms and models"""
    analyzer = ContentAnalyzer()
    results = analyzer.analyze_post(text, image)
    
    if not results["is_appropriate"]:
        issues = []
        if "text_analysis" in results and results["text_analysis"].get("issues"):
            issues.extend(results["text_analysis"]["issues"])
        if "image_analysis" in results and results["image_analysis"].get("issues"):
            issues.extend(results["image_analysis"]["issues"])
        raise ValidationError(f"Content violates community guidelines: {', '.join(issues)}")
    
    return results