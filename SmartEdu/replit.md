# Overview

This is an AI-powered personalized learning platform built with Streamlit that adapts educational content based on individual learner performance and behavior. The system provides interactive quizzes across multiple subjects (Mathematics, Science, English, History, Programming) with three difficulty levels, generates personalized feedback, and tracks learning progress through comprehensive analytics.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Streamlit-based UI**: Single-page application with wide layout configuration and expandable sidebar for navigation
- **Session State Management**: Persistent user data, quiz history, current quiz state, and learner profiles stored in Streamlit session state
- **Interactive Components**: Quiz interface, progress visualization, and analytics dashboard with Plotly charts

## Backend Architecture
- **Modular Design**: Separation of concerns with distinct modules for profiling, content adaptation, quiz content, feedback generation, and analytics
- **Component-based Structure**: Core components include LearnerProfiler, ContentAdapter, QuizContent, FeedbackGenerator, and Analytics classes
- **Caching Strategy**: Streamlit resource caching for component initialization to optimize performance

## Learning Intelligence System
- **Learner Profiling**: Machine learning-based profiling using scikit-learn (KMeans clustering, StandardScaler) to classify learning styles and determine appropriate difficulty levels
- **Content Adaptation Engine**: Dynamic content recommendation based on performance history, topic weaknesses, and learner profile characteristics
- **Feature Engineering**: Extraction of learning metrics including accuracy trends, time patterns, consistency scores, and improvement trajectories

## Data Management
- **In-Memory Storage**: Quiz content and user data stored in Python data structures and Streamlit session state
- **Question Banking**: Hierarchical organization of quiz questions by subject and difficulty level with explanations
- **Performance Tracking**: Comprehensive quiz history with timestamps, accuracy scores, timing data, and topic performance metrics

## Analytics and Feedback System
- **Real-time Analytics**: Performance trend analysis, topic-specific insights, and learning pattern recognition using pandas and numpy
- **Personalized Feedback**: Context-aware feedback generation based on performance levels, timing patterns, and learner characteristics
- **Visualization Engine**: Interactive charts and graphs using Plotly for progress tracking and performance analysis

# External Dependencies

## Core Framework
- **Streamlit**: Web application framework for the user interface and session management

## Data Science Libraries
- **pandas**: Data manipulation and analysis for quiz history and performance metrics
- **numpy**: Numerical computations and statistical analysis
- **scikit-learn**: Machine learning algorithms for learner profiling and clustering

## Visualization
- **Plotly Express & Graph Objects**: Interactive charting and data visualization for analytics dashboard

## Python Standard Libraries
- **datetime**: Time-based calculations and timestamp management
- **random**: Content randomization and feedback message selection
- **json**: Data serialization for configuration and state management
- **collections**: Advanced data structures (defaultdict) for performance tracking
- **time**: Performance timing and duration calculations

No external databases, APIs, or third-party services are currently integrated. The system operates entirely with in-memory data storage and local computation.