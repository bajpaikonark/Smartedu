import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import defaultdict

class Analytics:
    def __init__(self):
        pass
    
    def generate_student_report(self, user_data):
        """Generate comprehensive analytics report for a student"""
        quiz_history = user_data['quiz_history']
        
        if not quiz_history:
            return {"error": "No quiz data available"}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame([
            {
                'timestamp': quiz['timestamp'],
                'topic': quiz['topic'],
                'difficulty': quiz['difficulty'],
                'accuracy': quiz['accuracy'],
                'total_time': quiz['total_time'],
                'avg_time_per_question': quiz['avg_time_per_question'],
                'correct_answers': quiz['correct_answers'],
                'total_questions': quiz['total_questions']
            }
            for quiz in quiz_history
        ])
        
        report = {
            'overview': self._generate_overview_stats(df),
            'performance_trends': self._analyze_performance_trends(df),
            'topic_analysis': self._analyze_topic_performance(df),
            'time_analysis': self._analyze_time_patterns(df),
            'learning_insights': self._generate_learning_insights(df)
        }
        
        return report
    
    def _generate_overview_stats(self, df):
        """Generate overview statistics"""
        return {
            'total_quizzes': len(df),
            'avg_accuracy': df['accuracy'].mean(),
            'best_accuracy': df['accuracy'].max(),
            'total_study_time': df['total_time'].sum(),
            'avg_quiz_time': df['total_time'].mean(),
            'topics_covered': df['topic'].nunique(),
            'date_range': {
                'start': df['timestamp'].min(),
                'end': df['timestamp'].max()
            }
        }
    
    def _analyze_performance_trends(self, df):
        """Analyze performance trends over time"""
        df_sorted = df.sort_values('timestamp')
        
        # Calculate rolling averages
        window_size = min(3, len(df))
        df_sorted['rolling_accuracy'] = df_sorted['accuracy'].rolling(window=window_size).mean()
        
        # Calculate improvement trend
        if len(df) >= 2:
            recent_performance = df_sorted.tail(3)['accuracy'].mean()
            early_performance = df_sorted.head(3)['accuracy'].mean()
            improvement_rate = recent_performance - early_performance
        else:
            improvement_rate = 0
        
        return {
            'improvement_rate': improvement_rate,
            'trend_direction': 'improving' if improvement_rate > 0.05 else 'stable' if improvement_rate > -0.05 else 'declining',
            'consistency': 1 - df['accuracy'].std(),  # Higher value = more consistent
            'recent_performance': df_sorted.tail(5)['accuracy'].mean(),
            'streak_analysis': self._calculate_streaks(df_sorted)
        }
    
    def _analyze_topic_performance(self, df):
        """Analyze performance by topic"""
        topic_stats = df.groupby('topic').agg({
            'accuracy': ['mean', 'std', 'count'],
            'total_time': 'mean',
            'timestamp': 'max'
        }).round(3)
        
        topic_stats.columns = ['avg_accuracy', 'accuracy_std', 'attempts', 'avg_time', 'last_attempt']
        
        # Identify strengths and weaknesses
        strengths = topic_stats[topic_stats['avg_accuracy'] > 0.75].index.tolist()
        weaknesses = topic_stats[topic_stats['avg_accuracy'] < 0.6].index.tolist()
        
        return {
            'topic_stats': topic_stats.to_dict('index'),
            'strengths': strengths,
            'weaknesses': weaknesses,
            'most_practiced': topic_stats['attempts'].idxmax() if not topic_stats.empty else None,
            'least_practiced': topic_stats['attempts'].idxmin() if not topic_stats.empty else None
        }
    
    def _analyze_time_patterns(self, df):
        """Analyze time-related patterns"""
        # Convert timestamps to datetime if they're not already
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.day_name()
        
        time_analysis = {
            'avg_time_per_question': df['avg_time_per_question'].mean(),
            'time_efficiency_trend': self._calculate_time_efficiency_trend(df),
            'preferred_study_hours': df.groupby('hour')['accuracy'].mean().to_dict(),
            'best_performance_day': df.groupby('day_of_week')['accuracy'].mean().idxmax() if len(df) > 0 else None,
            'speed_vs_accuracy_correlation': df['avg_time_per_question'].corr(df['accuracy'])
        }
        
        return time_analysis
    
    def _calculate_time_efficiency_trend(self, df):
        """Calculate if student is getting faster while maintaining accuracy"""
        if len(df) < 3:
            return 0
        
        df_sorted = df.sort_values('timestamp')
        
        # Split into early and recent periods
        split_point = len(df_sorted) // 2
        early_period = df_sorted.iloc[:split_point]
        recent_period = df_sorted.iloc[split_point:]
        
        early_time = early_period['avg_time_per_question'].mean()
        recent_time = recent_period['avg_time_per_question'].mean()
        
        early_accuracy = early_period['accuracy'].mean()
        recent_accuracy = recent_period['accuracy'].mean()
        
        # Efficiency improves if time decreases while accuracy stays same or improves
        time_improvement = (early_time - recent_time) / early_time if early_time > 0 else 0
        accuracy_change = recent_accuracy - early_accuracy
        
        # Weighted efficiency score
        efficiency_score = time_improvement + accuracy_change * 0.5
        
        return efficiency_score
    
    def _calculate_streaks(self, df_sorted):
        """Calculate success streaks"""
        # Define success as >70% accuracy
        successes = df_sorted['accuracy'] > 0.7
        
        current_streak = 0
        max_streak = 0
        temp_streak = 0
        
        for success in successes:
            if success:
                temp_streak += 1
                max_streak = max(max_streak, temp_streak)
            else:
                temp_streak = 0
        
        # Current streak (from the end)
        for success in reversed(successes.tolist()):
            if success:
                current_streak += 1
            else:
                break
        
        return {
            'current_streak': current_streak,
            'max_streak': max_streak,
            'success_rate': successes.mean()
        }
    
    def _generate_learning_insights(self, df):
        """Generate actionable learning insights"""
        insights = []
        
        # Performance insights
        if df['accuracy'].mean() > 0.8:
            insights.append("🌟 Strong overall performance! Consider advancing to more challenging topics.")
        elif df['accuracy'].mean() < 0.6:
            insights.append("📚 Focus on strengthening foundational concepts before moving forward.")
        
        # Time insights
        avg_time = df['avg_time_per_question'].mean()
        if avg_time > 30:
            insights.append("⏰ You tend to spend a lot of time on questions. Practice with time limits to improve speed.")
        elif avg_time < 10:
            insights.append("🏃 You work quickly! Make sure to read questions carefully to avoid careless mistakes.")
        
        # Consistency insights
        accuracy_std = df['accuracy'].std()
        if accuracy_std > 0.2:
            insights.append("📈 Your performance varies significantly. Try to identify what conditions help you perform best.")
        
        # Topic insights
        topic_performance = df.groupby('topic')['accuracy'].mean()
        if topic_performance.max() - topic_performance.min() > 0.3:
            insights.append(f"🎯 Large performance gap between topics. Focus on {topic_performance.idxmin()}.")
        
        # Recent trend insights
        if len(df) >= 5:
            recent_trend = df.tail(3)['accuracy'].mean() - df.head(3)['accuracy'].mean()
            if recent_trend > 0.1:
                insights.append("📈 Great improvement trend! Keep up the current study approach.")
            elif recent_trend < -0.1:
                insights.append("📉 Recent decline in performance. Consider reviewing recent topics or changing study methods.")
        
        return insights
    
    def generate_class_analytics(self, all_user_data):
        """Generate class-wide analytics for teachers"""
        if not all_user_data:
            return {"error": "No student data available"}
        
        # Collect all quiz data
        all_quizzes = []
        student_summaries = {}
        
        for username, user_data in all_user_data.items():
            quiz_history = user_data['quiz_history']
            if quiz_history:
                for quiz in quiz_history:
                    quiz_copy = quiz.copy()
                    quiz_copy['student'] = username
                    all_quizzes.append(quiz_copy)
                
                # Student summary
                df_student = pd.DataFrame(quiz_history)
                student_summaries[username] = {
                    'total_quizzes': len(quiz_history),
                    'avg_accuracy': df_student['accuracy'].mean(),
                    'last_activity': max(quiz['timestamp'] for quiz in quiz_history),
                    'topics_covered': df_student['topic'].nunique()
                }
        
        if not all_quizzes:
            return {"error": "No quiz data available"}
        
        df_all = pd.DataFrame(all_quizzes)
        
        class_analytics = {
            'overview': {
                'total_students': len(all_user_data),
                'active_students': len([u for u, d in all_user_data.items() if d['quiz_history']]),
                'total_quizzes': len(all_quizzes),
                'avg_class_accuracy': df_all['accuracy'].mean(),
                'total_study_time': df_all['total_time'].sum()
            },
            'performance_distribution': self._analyze_performance_distribution(df_all),
            'topic_analytics': self._analyze_class_topic_performance(df_all),
            'engagement_metrics': self._analyze_engagement_metrics(df_all, student_summaries),
            'at_risk_students': self._identify_at_risk_students(student_summaries, all_user_data)
        }
        
        return class_analytics
    
    def _analyze_performance_distribution(self, df):
        """Analyze how student performance is distributed"""
        return {
            'accuracy_quartiles': df['accuracy'].quantile([0.25, 0.5, 0.75]).to_dict(),
            'performance_categories': {
                'excellent': (df['accuracy'] > 0.85).sum(),
                'good': ((df['accuracy'] > 0.7) & (df['accuracy'] <= 0.85)).sum(),
                'needs_improvement': ((df['accuracy'] > 0.5) & (df['accuracy'] <= 0.7)).sum(),
                'struggling': (df['accuracy'] <= 0.5).sum()
            }
        }
    
    def _analyze_class_topic_performance(self, df):
        """Analyze class performance by topic"""
        topic_stats = df.groupby('topic').agg({
            'accuracy': ['mean', 'std', 'count'],
            'total_time': 'mean'
        }).round(3)
        
        topic_stats.columns = ['avg_accuracy', 'accuracy_std', 'total_attempts', 'avg_time']
        
        return {
            'topic_performance': topic_stats.to_dict('index'),
            'most_challenging': topic_stats['avg_accuracy'].idxmin() if not topic_stats.empty else None,
            'easiest': topic_stats['avg_accuracy'].idxmax() if not topic_stats.empty else None,
            'most_popular': topic_stats['total_attempts'].idxmax() if not topic_stats.empty else None
        }
    
    def _analyze_engagement_metrics(self, df, student_summaries):
        """Analyze student engagement patterns"""
        # Calculate engagement metrics
        avg_quizzes_per_student = df.groupby('student').size().mean()
        
        # Activity recency
        current_time = datetime.now()
        recent_activity = []
        for student, summary in student_summaries.items():
            days_since_last = (current_time - summary['last_activity']).days
            recent_activity.append(days_since_last)
        
        return {
            'avg_quizzes_per_student': avg_quizzes_per_student,
            'avg_days_since_last_activity': np.mean(recent_activity) if recent_activity else 0,
            'highly_engaged': len([s for s, summ in student_summaries.items() if summ['total_quizzes'] >= 5]),
            'inactive_students': len([days for days in recent_activity if days > 7])
        }
    
    def _identify_at_risk_students(self, student_summaries, all_user_data):
        """Identify students who might need additional support"""
        at_risk = []
        
        for username, summary in student_summaries.items():
            risk_factors = []
            
            # Low performance
            if summary['avg_accuracy'] < 0.6:
                risk_factors.append('low_performance')
            
            # Inactivity
            days_since_last = (datetime.now() - summary['last_activity']).days
            if days_since_last > 7:
                risk_factors.append('inactive')
            
            # Few attempts
            if summary['total_quizzes'] < 3:
                risk_factors.append('low_engagement')
            
            # Declining performance
            quiz_history = all_user_data[username]['quiz_history']
            if len(quiz_history) >= 3:
                recent_avg = np.mean([q['accuracy'] for q in quiz_history[-2:]])
                early_avg = np.mean([q['accuracy'] for q in quiz_history[:2]])
                if recent_avg < early_avg - 0.15:
                    risk_factors.append('declining_performance')
            
            if risk_factors:
                at_risk.append({
                    'student': username,
                    'risk_factors': risk_factors,
                    'current_accuracy': summary['avg_accuracy'],
                    'days_inactive': days_since_last
                })
        
        return at_risk
