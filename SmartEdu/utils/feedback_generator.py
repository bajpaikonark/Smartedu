import random

class FeedbackGenerator:
    def __init__(self):
        self.encouragement_messages = [
            "Great job! Keep up the excellent work! 🌟",
            "You're making fantastic progress! 🎉",
            "Excellent understanding! You've got this! 💪",
            "Outstanding performance! Keep learning! 🚀",
            "Wonderful work! Your effort is paying off! 👏"
        ]
        
        self.improvement_messages = [
            "Good effort! Let's practice a bit more to strengthen understanding. 📚",
            "You're on the right track! A little more practice will help. 💪",
            "Nice try! Review the concepts and you'll get it next time. 🔄",
            "Keep working at it! Progress comes with practice. 📈",
            "Don't give up! Every mistake is a learning opportunity. 🌱"
        ]
        
        self.struggling_messages = [
            "It's okay to find this challenging. Let's break it down step by step. 🧩",
            "Learning takes time. Let's try a different approach. 🔍",
            "Don't worry! Let's review the basics and build up from there. 🏗️",
            "Everyone learns at their own pace. You're doing fine! 🌿",
            "Let's take it slow and focus on understanding each concept. 🎯"
        ]
    
    def generate_feedback(self, quiz_result, learner_profile=None):
        """Generate personalized feedback based on quiz performance"""
        accuracy = quiz_result['accuracy']
        total_time = quiz_result['total_time']
        avg_time = quiz_result['avg_time_per_question']
        topic = quiz_result['topic']
        
        feedback_parts = []
        
        # Performance-based feedback
        if accuracy >= 0.8:
            feedback_parts.append(random.choice(self.encouragement_messages))
            feedback_parts.append(f"You scored {accuracy:.0%} on {topic}!")
            
            if avg_time < 15:
                feedback_parts.append("You completed the quiz quickly and accurately. Consider trying more advanced topics! 🚀")
            else:
                feedback_parts.append("You took your time to think through each question carefully. Excellent approach! 🤔")
                
        elif accuracy >= 0.6:
            feedback_parts.append(random.choice(self.improvement_messages))
            feedback_parts.append(f"You scored {accuracy:.0%} on {topic}. You're getting there!")
            
            # Specific suggestions based on performance
            incorrect_count = int((1 - accuracy) * quiz_result['total_questions'])
            feedback_parts.append(f"Focus on reviewing the {incorrect_count} concepts you missed.")
            
        else:
            feedback_parts.append(random.choice(self.struggling_messages))
            feedback_parts.append(f"You scored {accuracy:.0%} on {topic}. Let's work on building a stronger foundation.")
            feedback_parts.append("I recommend reviewing the basic concepts before trying again.")
        
        # Time-based feedback
        if avg_time > 45:
            feedback_parts.append("💡 Tip: Try to trust your first instinct more often. Overthinking can sometimes lead to changing correct answers.")
        elif avg_time < 10:
            feedback_parts.append("💡 Tip: Take a moment to read each question carefully before answering.")
        
        # Learner profile-based feedback
        if learner_profile:
            style_feedback = self._get_style_specific_feedback(learner_profile, accuracy)
            if style_feedback:
                feedback_parts.append(style_feedback)
        
        return " ".join(feedback_parts)
    
    def _get_style_specific_feedback(self, profile, accuracy):
        """Generate feedback specific to learning style"""
        style = profile.get('learning_style', 'unknown')
        
        style_messages = {
            'fast_learner': {
                'high': "Since you learn quickly, try exploring related advanced topics! 🎓",
                'low': "You usually excel quickly. Take your time to ensure you understand the fundamentals. 🔍"
            },
            'methodical_learner': {
                'high': "Your careful, methodical approach is paying off! 📚",
                'low': "Continue with your systematic approach. Consider reviewing each concept thoroughly. 📖"
            },
            'struggling_learner': {
                'high': "Great improvement! Your hard work is showing results! 🌟",
                'low': "Remember, learning takes time. Try breaking down complex problems into smaller steps. 🧩"
            },
            'steady_learner': {
                'high': "Your consistent effort is excellent! Keep maintaining this steady pace. 📈",
                'low': "Stay consistent with your learning approach. Regular practice will help. 🔄"
            }
        }
        
        performance_level = 'high' if accuracy >= 0.7 else 'low'
        
        if style in style_messages:
            return style_messages[style][performance_level]
        
        return None
    
    def generate_hint(self, question):
        """Generate a helpful hint for a question"""
        hints = [
            "Think about the key concepts involved in this question. 🤔",
            "Try to eliminate obviously wrong answers first. ❌",
            "Break down the problem into smaller parts. 🧩",
            "Consider what you already know about this topic. 💭",
            "Read the question carefully - sometimes the answer is in the details. 👀",
            "Think step by step through the problem. 📝"
        ]
        
        # Try to generate a more specific hint based on question content
        question_text = question['question'].lower()
        
        if 'calculate' in question_text or 'solve' in question_text:
            return "Work through this step by step. What operations do you need to perform? 🔢"
        elif 'what is' in question_text:
            return "Think about the definition or formula that applies here. 📚"
        elif 'which' in question_text or 'identify' in question_text:
            return "Compare each option carefully against what you know. ⚖️"
        elif any(op in question_text for op in ['+', '-', '×', '÷', '*', '/']):
            return "Remember the order of operations (PEMDAS/BODMAS). Calculate step by step. 🧮"
        else:
            return random.choice(hints)
    
    def generate_encouragement(self, streak_count=0, improvement_trend=0):
        """Generate encouraging messages based on learning patterns"""
        messages = []
        
        if streak_count >= 3:
            messages.append(f"🔥 Amazing! You're on a {streak_count}-quiz success streak!")
        elif streak_count >= 2:
            messages.append(f"⭐ Great! You're building momentum with {streak_count} strong performances!")
        
        if improvement_trend > 0.1:
            messages.append("📈 Your scores are improving consistently! Keep up the great work!")
        elif improvement_trend > 0:
            messages.append("🌱 You're showing steady progress. Every step counts!")
        
        if not messages:
            messages.append("🌟 Remember: every expert was once a beginner. Keep learning!")
        
        return " ".join(messages)
    
    def generate_study_tips(self, weak_areas, strong_areas):
        """Generate study tips based on performance areas"""
        tips = []
        
        if strong_areas:
            tips.append(f"💪 Your strengths in {', '.join(strong_areas)} show you have great potential!")
        
        if weak_areas:
            tips.append(f"🎯 Focus your study time on {', '.join(weak_areas)} for maximum improvement.")
            tips.append("📅 Try spending 15-20 minutes daily on challenging topics.")
            tips.append("🔄 Review these areas regularly to build long-term retention.")
        
        # General study tips
        general_tips = [
            "📝 Take notes while learning to improve retention.",
            "🧠 Try teaching concepts to someone else - it reinforces your understanding.",
            "⏰ Use spaced repetition - review material at increasing intervals.",
            "🎯 Set small, achievable daily learning goals.",
            "💡 Connect new concepts to things you already know."
        ]
        
        tips.append(random.choice(general_tips))
        
        return tips
