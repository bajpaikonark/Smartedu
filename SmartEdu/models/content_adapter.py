import numpy as np
import random
from collections import defaultdict

class ContentAdapter:
    def __init__(self):
        self.difficulty_levels = ['beginner', 'intermediate', 'advanced']
        self.topics = ['Mathematics', 'Science', 'English', 'History', 'Programming']
        
    def get_next_content(self, quiz_history, learner_profile=None):
        """Recommend next content based on performance and profile"""
        if not quiz_history:
            return "Mathematics", "beginner"
        
        # Analyze recent performance
        recent_quizzes = quiz_history[-3:] if len(quiz_history) >= 3 else quiz_history
        
        # Get topic performance
        topic_performance = self._analyze_topic_performance(quiz_history)
        
        # Choose topic based on weaknesses or continuation
        recommended_topic = self._select_topic(topic_performance, recent_quizzes)
        
        # Adapt difficulty based on performance
        recommended_difficulty = self._adapt_difficulty(recent_quizzes, learner_profile)
        
        return recommended_topic, recommended_difficulty
    
    def _analyze_topic_performance(self, quiz_history):
        """Analyze performance across different topics"""
        topic_stats = defaultdict(lambda: {'scores': [], 'attempts': 0})
        
        for quiz in quiz_history:
            topic = quiz['topic']
            topic_stats[topic]['scores'].append(quiz['accuracy'])
            topic_stats[topic]['attempts'] += 1
        
        # Calculate averages and identify patterns
        topic_performance = {}
        for topic, stats in topic_stats.items():
            avg_score = np.mean(stats['scores'])
            recent_score = stats['scores'][-1] if stats['scores'] else 0
            attempts = stats['attempts']
            
            topic_performance[topic] = {
                'avg_score': avg_score,
                'recent_score': recent_score,
                'attempts': attempts,
                'needs_improvement': avg_score < 0.7
            }
        
        return topic_performance
    
    def _select_topic(self, topic_performance, recent_quizzes):
        """Select next topic based on performance analysis"""
        if not topic_performance:
            return random.choice(self.topics)
        
        # Find topics that need improvement
        weak_topics = [topic for topic, stats in topic_performance.items() 
                      if stats['needs_improvement']]
        
        if weak_topics:
            # Focus on weakest topic
            weakest_topic = min(weak_topics, 
                              key=lambda t: topic_performance[t]['avg_score'])
            return weakest_topic
        
        # If all topics are strong, continue with recent topic or explore new
        recent_topics = [quiz['topic'] for quiz in recent_quizzes]
        if recent_topics:
            recent_topic = recent_topics[-1]
            # 70% chance to continue, 30% to explore
            if random.random() < 0.7:
                return recent_topic
        
        # Explore less practiced topics
        topic_attempts = {topic: stats['attempts'] 
                         for topic, stats in topic_performance.items()}
        least_practiced = min(self.topics, 
                            key=lambda t: topic_attempts.get(t, 0))
        return least_practiced
    
    def _adapt_difficulty(self, recent_quizzes, learner_profile):
        """Adapt difficulty based on recent performance and learner profile"""
        if not recent_quizzes:
            return "beginner"
        
        # Calculate recent performance metrics
        recent_accuracy = np.mean([quiz['accuracy'] for quiz in recent_quizzes])
        recent_times = [quiz['avg_time_per_question'] for quiz in recent_quizzes]
        avg_time = np.mean(recent_times)
        
        # Get current difficulty from recent quizzes
        current_difficulties = [quiz.get('difficulty', 'beginner') for quiz in recent_quizzes]
        current_level_idx = self.difficulty_levels.index(
            max(set(current_difficulties), key=current_difficulties.count)
        )
        
        # Adaptation logic
        if recent_accuracy > 0.85 and avg_time < 20:
            # Performing very well - increase difficulty
            new_level_idx = min(current_level_idx + 1, len(self.difficulty_levels) - 1)
        elif recent_accuracy < 0.6:
            # Struggling - decrease difficulty
            new_level_idx = max(current_level_idx - 1, 0)
        else:
            # Maintain current level
            new_level_idx = current_level_idx
        
        # Consider learner profile if available
        if learner_profile:
            style = learner_profile.get('learning_style', 'average_learner')
            if style == 'fast_learner' and recent_accuracy > 0.8:
                new_level_idx = min(new_level_idx + 1, len(self.difficulty_levels) - 1)
            elif style == 'struggling_learner':
                new_level_idx = max(new_level_idx - 1, 0)
        
        return self.difficulty_levels[new_level_idx]
    
    def get_content_sequence(self, topic, difficulty, num_items=5):
        """Generate a sequence of content items for the given topic and difficulty"""
        # This would typically connect to a content database
        # For now, return a structured sequence
        
        sequence = {
            'topic': topic,
            'difficulty': difficulty,
            'items': []
        }
        
        # Generate content progression
        if difficulty == 'beginner':
            sequence['items'] = [
                {'type': 'concept_intro', 'content': f'Introduction to {topic}'},
                {'type': 'example', 'content': f'Basic examples in {topic}'},
                {'type': 'practice', 'content': f'Simple practice problems'},
                {'type': 'quiz', 'content': f'Assessment quiz'},
                {'type': 'review', 'content': f'Review and summary'}
            ]
        elif difficulty == 'intermediate':
            sequence['items'] = [
                {'type': 'review', 'content': f'Quick review of {topic} basics'},
                {'type': 'advanced_concept', 'content': f'Intermediate concepts'},
                {'type': 'application', 'content': f'Real-world applications'},
                {'type': 'problem_solving', 'content': f'Complex problem solving'},
                {'type': 'quiz', 'content': f'Comprehensive assessment'}
            ]
        else:  # advanced
            sequence['items'] = [
                {'type': 'advanced_theory', 'content': f'Advanced {topic} theory'},
                {'type': 'research', 'content': f'Current research in {topic}'},
                {'type': 'project', 'content': f'Applied project work'},
                {'type': 'peer_review', 'content': f'Peer collaboration'},
                {'type': 'mastery_test', 'content': f'Mastery assessment'}
            ]
        
        return sequence
    
    def get_teacher_recommendations(self, quiz_history, learner_profile):
        """Generate recommendations for teachers about a student"""
        recommendations = []
        
        if not quiz_history:
            recommendations.append("Student hasn't completed any assessments yet")
            return recommendations
        
        # Recent performance analysis
        recent_accuracy = np.mean([q['accuracy'] for q in quiz_history[-3:]])
        overall_accuracy = np.mean([q['accuracy'] for q in quiz_history])
        
        # Performance trend
        if len(quiz_history) >= 3:
            early_avg = np.mean([q['accuracy'] for q in quiz_history[:len(quiz_history)//2]])
            late_avg = np.mean([q['accuracy'] for q in quiz_history[len(quiz_history)//2:]])
            
            if late_avg > early_avg + 0.1:
                recommendations.append("✅ Student is showing consistent improvement")
            elif late_avg < early_avg - 0.1:
                recommendations.append("⚠️ Student performance is declining - consider intervention")
        
        # Learning style recommendations
        style = learner_profile.get('learning_style', 'unknown')
        if style == 'struggling_learner':
            recommendations.append("🎯 Provide additional support and scaffolding")
            recommendations.append("📚 Consider visual aids and step-by-step guidance")
        elif style == 'fast_learner':
            recommendations.append("🚀 Provide enrichment activities and advanced challenges")
        elif style == 'methodical_learner':
            recommendations.append("⏰ Allow extra time for thorough understanding")
        
        # Topic-specific recommendations
        strengths = learner_profile.get('strengths', [])
        weaknesses = learner_profile.get('weaknesses', [])
        
        if strengths:
            recommendations.append(f"💪 Leverage strengths in: {', '.join(strengths)}")
        if weaknesses:
            recommendations.append(f"📈 Focus improvement on: {', '.join(weaknesses)}")
        
        return recommendations
