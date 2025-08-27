import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

from models.learner_profiler import LearnerProfiler
from models.content_adapter import ContentAdapter
from data.quiz_content import QuizContent
from utils.feedback_generator import FeedbackGenerator
from utils.analytics import Analytics
from utils.ai_chatbot import AIChatbot

# Configure page
st.set_page_config(
    page_title="AI Personalized Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'quiz_history' not in st.session_state:
    st.session_state.quiz_history = []
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_start_time' not in st.session_state:
    st.session_state.quiz_start_time = None
if 'learner_profile' not in st.session_state:
    st.session_state.learner_profile = None
if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'quiz'

# Initialize components
@st.cache_resource
def initialize_components():
    quiz_content = QuizContent()
    learner_profiler = LearnerProfiler()
    content_adapter = ContentAdapter()
    feedback_generator = FeedbackGenerator()
    analytics = Analytics()
    ai_chatbot = AIChatbot()
    return quiz_content, learner_profiler, content_adapter, feedback_generator, analytics, ai_chatbot

components = initialize_components()
quiz_content, learner_profiler, content_adapter, feedback_generator, analytics, ai_chatbot = components

def main():
    st.title("🎓 AI Personalized Learning Platform")
    st.markdown("---")
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox("Choose your role:", ["Student Portal", "Teacher Dashboard"])
        
        if page == "Student Portal" and st.session_state.selected_user:
            st.markdown("---")
            st.subheader("Learning Activities")
            activity = st.radio("Choose activity:", ["📝 Practice Quiz", "💬 AI Tutor Chat"], key="activity_selector")
            if activity == "📝 Practice Quiz":
                st.session_state.current_page = 'quiz'
            else:
                st.session_state.current_page = 'chat'
        
        if page == "Student Portal":
            st.subheader("Student Profile")
            user_name = st.text_input("Enter your name:", value=st.session_state.get('selected_user', ''))
            if user_name and user_name != st.session_state.get('selected_user'):
                st.session_state.selected_user = user_name
                if user_name not in st.session_state.user_data:
                    st.session_state.user_data[user_name] = {
                        'quiz_history': [],
                        'performance_metrics': {},
                        'learning_style': 'unknown',
                        'current_level': 'beginner'
                    }
                st.rerun()
    
    if page == "Student Portal":
        student_portal()
    else:
        teacher_dashboard()

def student_portal():
    if not st.session_state.selected_user:
        st.info("👈 Please enter your name in the sidebar to get started!")
        return
    
    user_name = st.session_state.selected_user
    user_data = st.session_state.user_data[user_name]
    
    # Initialize chat history for this user if not exists
    if user_name not in st.session_state.chat_history:
        st.session_state.chat_history[user_name] = []
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"Welcome back, {user_name}! 👋")
        
        # Display current learning profile
        if user_data['quiz_history']:
            profile = learner_profiler.get_learner_profile(user_data['quiz_history'])
            st.session_state.learner_profile = profile
            
            st.info(f"**Learning Profile:** {profile['learning_style'].title()} | **Level:** {profile['current_level'].title()}")
        
        # Show different content based on selected page
        if st.session_state.current_page == 'chat':
            ai_tutor_chat()
        else:
            # Quiz section
            st.subheader("📝 Practice Quiz")
            display_quiz_section(user_data)
    
    with col2:
        # Progress visualization
        st.subheader("📊 Your Progress")
        if user_data['quiz_history']:
            display_student_progress(user_data)
        else:
            st.info("Complete a quiz to see your progress!")

def display_quiz():
    quiz = st.session_state.current_quiz
    current_q = quiz['current_question']
    question = quiz['questions'][current_q]
    
    st.subheader(f"Question {current_q + 1} of {len(quiz['questions'])}")
    
    # Progress bar
    progress = (current_q) / len(quiz['questions'])
    st.progress(progress)
    
    # Question display
    st.markdown(f"**{question['question']}**")
    
    # Answer options
    answer = st.radio("Select your answer:", question['options'], key=f"q_{current_q}")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_q > 0:
            if st.button("⬅️ Previous"):
                quiz['current_question'] -= 1
                st.rerun()
    
    with col2:
        if st.button("💡 Hint"):
            hint = feedback_generator.generate_hint(question)
            st.info(f"💡 **Hint:** {hint}")
    
    with col3:
        if current_q < len(quiz['questions']) - 1:
            if st.button("➡️ Next"):
                # Record answer and timing
                quiz['answers'].append({
                    'question_id': current_q,
                    'answer': answer,
                    'correct': answer == question['correct_answer'],
                    'time_taken': time.time() - quiz['question_start_times'][-1]
                })
                quiz['current_question'] += 1
                quiz['question_start_times'].append(time.time())
                st.rerun()
        else:
            if st.button("✅ Finish Quiz", type="primary"):
                # Record final answer
                quiz['answers'].append({
                    'question_id': current_q,
                    'answer': answer,
                    'correct': answer == question['correct_answer'],
                    'time_taken': time.time() - quiz['question_start_times'][-1]
                })
                finish_quiz()

def finish_quiz():
    quiz = st.session_state.current_quiz
    user_name = st.session_state.selected_user
    
    # Calculate quiz metrics
    total_time = time.time() - quiz['start_time']
    correct_answers = sum(1 for ans in quiz['answers'] if ans['correct'])
    accuracy = correct_answers / len(quiz['answers'])
    avg_time_per_question = total_time / len(quiz['answers'])
    
    # Create quiz result
    quiz_result = {
        'timestamp': datetime.now(),
        'topic': quiz['topic'],
        'difficulty': quiz['difficulty'],
        'total_questions': len(quiz['questions']),
        'correct_answers': correct_answers,
        'accuracy': accuracy,
        'total_time': total_time,
        'avg_time_per_question': avg_time_per_question,
        'answers': quiz['answers']
    }
    
    # Store in user data
    st.session_state.user_data[user_name]['quiz_history'].append(quiz_result)
    
    # Generate personalized feedback
    feedback = feedback_generator.generate_feedback(quiz_result, st.session_state.learner_profile)
    
    # Display results
    st.success("🎉 Quiz completed!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score", f"{correct_answers}/{len(quiz['questions'])}", f"{accuracy:.1%}")
        st.metric("Time Taken", f"{total_time:.1f}s", f"{avg_time_per_question:.1f}s avg")
    
    with col2:
        st.subheader("📝 Personalized Feedback")
        st.write(feedback)
    
    # Clear current quiz
    st.session_state.current_quiz = None
    
    if st.button("🔄 Take Another Quiz"):
        st.rerun()

def display_student_progress(user_data):
    quiz_history = user_data['quiz_history']
    
    if len(quiz_history) == 0:
        return
    
    # Accuracy over time
    accuracies = [quiz['accuracy'] for quiz in quiz_history]
    dates = [quiz['timestamp'] for quiz in quiz_history]
    
    fig = px.line(x=dates, y=accuracies, title="Accuracy Over Time")
    fig.update_layout(yaxis=dict(range=[0, 1], tickformat='.0%'))
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent performance metrics
    if len(quiz_history) >= 3:
        recent_avg = np.mean(accuracies[-3:])
        st.metric("Recent Performance", f"{recent_avg:.1%}")

def teacher_dashboard():
    st.header("👩‍🏫 Teacher Dashboard")
    
    if not st.session_state.user_data:
        st.info("No student data available yet. Students need to complete quizzes first.")
        return
    
    # Student overview
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📊 Class Overview")
        total_students = len(st.session_state.user_data)
        active_students = len([user for user, data in st.session_state.user_data.items() if data['quiz_history']])
        
        st.metric("Total Students", total_students)
        st.metric("Active Students", active_students)
        
        # Student selection
        student_names = list(st.session_state.user_data.keys())
        selected_student = st.selectbox("Select Student for Details:", student_names)
    
    with col2:
        if selected_student:
            display_student_details(selected_student)
    
    # Class performance analytics
    st.subheader("📈 Class Performance Analytics")
    display_class_analytics()

def display_student_details(student_name):
    st.subheader(f"Student Profile: {student_name}")
    
    user_data = st.session_state.user_data[student_name]
    quiz_history = user_data['quiz_history']
    
    if not quiz_history:
        st.info("This student hasn't completed any quizzes yet.")
        return
    
    # Generate learner profile
    profile = learner_profiler.get_learner_profile(quiz_history)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Learning Style:** {profile['learning_style'].title()}")
        st.write(f"**Current Level:** {profile['current_level'].title()}")
        st.write(f"**Quizzes Completed:** {len(quiz_history)}")
        
        # Recent performance
        if len(quiz_history) >= 3:
            recent_accuracy = np.mean([q['accuracy'] for q in quiz_history[-3:]])
            st.metric("Recent Average", f"{recent_accuracy:.1%}")
    
    with col2:
        # Performance trend
        if len(quiz_history) > 1:
            accuracies = [quiz['accuracy'] for quiz in quiz_history]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=accuracies,
                mode='lines+markers',
                name='Accuracy',
                line=dict(color='#1f77b4')
            ))
            fig.update_layout(
                title=f"{student_name}'s Progress",
                yaxis_title="Accuracy",
                yaxis=dict(range=[0, 1], tickformat='.0%'),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("🎯 Recommendations")
    recommendations = content_adapter.get_teacher_recommendations(quiz_history, profile)
    for rec in recommendations:
        st.write(f"• {rec}")

def display_class_analytics():
    if not st.session_state.user_data:
        return
    
    # Collect all quiz data
    all_quizzes = []
    for user, data in st.session_state.user_data.items():
        for quiz in data['quiz_history']:
            quiz_copy = quiz.copy()
            quiz_copy['student'] = user
            all_quizzes.append(quiz_copy)
    
    if not all_quizzes:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average performance by topic
        topic_performance = {}
        for quiz in all_quizzes:
            topic = quiz['topic']
            if topic not in topic_performance:
                topic_performance[topic] = []
            topic_performance[topic].append(quiz['accuracy'])
        
        topics = list(topic_performance.keys())
        avg_accuracies = [np.mean(topic_performance[topic]) for topic in topics]
        
        fig = px.bar(x=topics, y=avg_accuracies, title="Average Performance by Topic")
        fig.update_layout(yaxis=dict(tickformat='.0%'))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Learning style distribution
        learning_styles = []
        for user, data in st.session_state.user_data.items():
            if data['quiz_history']:
                profile = learner_profiler.get_learner_profile(data['quiz_history'])
                learning_styles.append(profile['learning_style'])
        
        if learning_styles:
            style_counts = {}
            for style in learning_styles:
                style_counts[style] = style_counts.get(style, 0) + 1
            
            fig = px.pie(
                values=list(style_counts.values()),
                names=list(style_counts.keys()),
                title="Learning Style Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

def display_quiz_section(user_data):
    """Display the quiz section with topic selection and start quiz functionality"""
    if st.session_state.current_quiz is None:
        # Get adaptive content recommendation
        if user_data['quiz_history']:
            recommended_topic, difficulty = content_adapter.get_next_content(
                user_data['quiz_history'], 
                st.session_state.learner_profile
            )
        else:
            recommended_topic, difficulty = "Mathematics", "beginner"
        
        st.write(f"**Recommended Topic:** {recommended_topic}")
        st.write(f"**Difficulty Level:** {difficulty.title()}")
        
        col_start, col_topic = st.columns([1, 2])
        with col_start:
            if st.button("🚀 Start Quiz", type="primary"):
                questions = quiz_content.get_questions(recommended_topic, difficulty, num_questions=5)
                st.session_state.current_quiz = {
                    'questions': questions,
                    'current_question': 0,
                    'answers': [],
                    'start_time': time.time(),
                    'question_start_times': [time.time()],
                    'topic': recommended_topic,
                    'difficulty': difficulty
                }
                st.rerun()
        
        with col_topic:
            # Allow topic selection
            topics = quiz_content.get_available_topics()
            selected_topic = st.selectbox("Or choose a different topic:", topics, 
                                        index=topics.index(recommended_topic) if recommended_topic in topics else 0)
            if selected_topic != recommended_topic:
                if st.button("Start with selected topic"):
                    questions = quiz_content.get_questions(selected_topic, difficulty, num_questions=5)
                    st.session_state.current_quiz = {
                        'questions': questions,
                        'current_question': 0,
                        'answers': [],
                        'start_time': time.time(),
                        'question_start_times': [time.time()],
                        'topic': selected_topic,
                        'difficulty': difficulty
                    }
                    st.rerun()
    else:
        display_quiz()

def ai_tutor_chat():
    """Display the AI tutor chat interface"""
    st.subheader("💬 AI Tutor Chat")
    st.write("Ask me anything about any topic you're curious about! I'm here to help you learn.")
    
    user_name = st.session_state.selected_user
    chat_history = st.session_state.chat_history[user_name]
    
    # Display chat history
    if chat_history:
        st.subheader("📜 Conversation History")
        for i, message in enumerate(chat_history):
            if message['role'] == 'user':
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**AI Tutor:** {message['content']}")
        st.markdown("---")
    
    # Topic suggestions
    st.subheader("💡 Suggested Topics")
    if st.button("🔄 Get New Topic Suggestions"):
        profile = st.session_state.learner_profile
        suggestions = ai_chatbot.generate_topic_suggestions(profile)
        st.session_state.topic_suggestions = suggestions
    
    if 'topic_suggestions' in st.session_state:
        cols = st.columns(len(st.session_state.topic_suggestions))
        for i, topic in enumerate(st.session_state.topic_suggestions):
            with cols[i]:
                if st.button(f"💭 {topic}", key=f"topic_{i}"):
                    # Generate conversation starters for this topic
                    starters = ai_chatbot.generate_conversation_starters(topic)
                    if starters:
                        starter_text = f"I'm curious about {topic}. {starters[0]}"
                        # Add to chat and get response
                        chat_history.append({"role": "user", "content": starter_text})
                        response = ai_chatbot.chat(starter_text, chat_history[:-1])
                        chat_history.append({"role": "assistant", "content": response})
                        st.rerun()
    
    # Chat input
    st.subheader("💬 Ask a Question")
    user_input = st.text_area("Type your question or topic:", height=100, key="chat_input")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Send 📨", type="primary"):
            if user_input.strip():
                # Add user message to chat history
                chat_history.append({"role": "user", "content": user_input})
                
                # Get AI response
                with st.spinner("🤔 Thinking..."):
                    response = ai_chatbot.chat(user_input, chat_history[:-1])
                
                # Add AI response to chat history
                chat_history.append({"role": "assistant", "content": response})
                
                # Clear input and refresh
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history[user_name] = []
            st.rerun()
    
    # Show recent conversation
    if chat_history:
        st.subheader("💭 Recent Messages")
        # Show last few messages
        recent_messages = chat_history[-6:] if len(chat_history) > 6 else chat_history
        for message in recent_messages:
            if message['role'] == 'user':
                st.info(f"**You:** {message['content']}")
            else:
                st.success(f"**AI Tutor:** {message['content']}")

if __name__ == "__main__":
    main()
