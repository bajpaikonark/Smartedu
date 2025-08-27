import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

class LearnerProfiler:
    def __init__(self):
        self.scaler = StandardScaler()
        self.clusterer = KMeans(n_clusters=3, random_state=42)
        self.is_fitted = False
    
    def extract_features(self, quiz_history):
        """Extract learning features from quiz history"""
        if not quiz_history:
            return np.array([0.5, 30.0, 0.5, 0.0])  # Default features
        
        # Calculate metrics
        accuracies = [quiz['accuracy'] for quiz in quiz_history]
        avg_times = [quiz['avg_time_per_question'] for quiz in quiz_history]
        
        # Feature engineering
        avg_accuracy = np.mean(accuracies)
        avg_time_per_question = np.mean(avg_times)
        consistency = 1 - np.std(accuracies) if len(accuracies) > 1 else 1.0
        improvement_trend = self._calculate_trend(accuracies)
        
        return np.array([avg_accuracy, avg_time_per_question, consistency, improvement_trend])
    
    def _calculate_trend(self, values):
        """Calculate improvement trend using linear regression slope"""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        return slope
    
    def get_learner_profile(self, quiz_history):
        """Generate comprehensive learner profile"""
        features = self.extract_features(quiz_history)
        avg_accuracy, avg_time, consistency, trend = features
        
        # Classify learning style based on patterns
        learning_style = self._classify_learning_style(avg_accuracy, avg_time, consistency)
        
        # Determine current level
        current_level = self._determine_level(avg_accuracy, trend)
        
        # Generate learning pace
        pace = self._determine_pace(avg_time, avg_accuracy)
        
        # Identify strengths and weaknesses
        strengths, weaknesses = self._analyze_performance(quiz_history)
        
        return {
            'learning_style': learning_style,
            'current_level': current_level,
            'pace': pace,
            'avg_accuracy': avg_accuracy,
            'consistency': consistency,
            'improvement_trend': trend,
            'strengths': strengths,
            'weaknesses': weaknesses
        }
    
    def _classify_learning_style(self, accuracy, avg_time, consistency):
        """Classify learner into different learning styles"""
        if accuracy > 0.8 and avg_time < 15:
            return 'fast_learner'
        elif accuracy > 0.7 and consistency > 0.8:
            return 'steady_learner'
        elif accuracy < 0.6:
            return 'struggling_learner'
        elif avg_time > 30:
            return 'methodical_learner'
        else:
            return 'average_learner'
    
    def _determine_level(self, accuracy, trend):
        """Determine current proficiency level"""
        if accuracy > 0.85 and trend >= 0:
            return 'advanced'
        elif accuracy > 0.7:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _determine_pace(self, avg_time, accuracy):
        """Determine learning pace preference"""
        if avg_time < 15 and accuracy > 0.7:
            return 'fast'
        elif avg_time > 30:
            return 'slow'
        else:
            return 'moderate'
    
    def _analyze_performance(self, quiz_history):
        """Analyze strengths and weaknesses by topic"""
        if not quiz_history:
            return [], []
        
        topic_performance = {}
        for quiz in quiz_history:
            topic = quiz['topic']
            if topic not in topic_performance:
                topic_performance[topic] = []
            topic_performance[topic].append(quiz['accuracy'])
        
        # Calculate average performance per topic
        topic_averages = {topic: np.mean(scores) for topic, scores in topic_performance.items()}
        
        # Identify strengths (>75% accuracy) and weaknesses (<60% accuracy)
        strengths = [topic for topic, avg in topic_averages.items() if avg > 0.75]
        weaknesses = [topic for topic, avg in topic_averages.items() if avg < 0.60]
        
        return strengths, weaknesses
    
    def get_learning_recommendations(self, profile):
        """Generate personalized learning recommendations"""
        recommendations = []
        
        style = profile['learning_style']
        level = profile['current_level']
        pace = profile['pace']
        
        if style == 'fast_learner':
            recommendations.append("Consider advanced topics and challenge problems")
            recommendations.append("Try time-based challenges to maintain engagement")
        elif style == 'struggling_learner':
            recommendations.append("Focus on foundational concepts with visual aids")
            recommendations.append("Break down complex problems into smaller steps")
            recommendations.append("Use more interactive and hands-on learning materials")
        elif style == 'methodical_learner':
            recommendations.append("Provide detailed explanations and step-by-step solutions")
            recommendations.append("Allow extra time for practice and reflection")
        
        if profile['consistency'] < 0.5:
            recommendations.append("Work on consistency with regular practice sessions")
        
        if profile['improvement_trend'] < 0:
            recommendations.append("Review recent topics and identify knowledge gaps")
            recommendations.append("Consider additional support or tutoring")
        
        return recommendations
