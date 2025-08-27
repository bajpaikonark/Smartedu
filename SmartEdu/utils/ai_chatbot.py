import os
import json
from openai import OpenAI

class AIChatbot:
    def __init__(self):
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-5"
        
        # System message to guide the AI tutor behavior
        self.system_message = {
            "role": "system",
            "content": """You are a friendly and knowledgeable AI tutor designed to help students learn about any topic they're curious about. Your role is to:

1. Engage students in educational conversations on any subject
2. Explain concepts in simple, easy-to-understand language
3. Encourage curiosity and critical thinking
4. Ask follow-up questions to deepen understanding
5. Provide examples and real-world applications
6. Be patient and supportive
7. Adapt your explanations to the student's level of understanding

Keep your responses conversational, encouraging, and educational. Use emojis sparingly to keep things friendly. If a student asks about something outside of educational topics, gently redirect them back to learning-focused discussions."""
        }
    
    def chat(self, user_message, chat_history=None):
        """
        Generate a response to the user's message
        
        Args:
            user_message (str): The user's message
            chat_history (list): Previous conversation history
            
        Returns:
            str: AI response
        """
        try:
            # Prepare messages for the API call
            messages = [self.system_message]
            
            # Add previous chat history if available
            if chat_history:
                messages.extend(chat_history)
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I'm sorry, I'm having trouble connecting right now. Please try again in a moment. Error: {str(e)}"
    
    def generate_topic_suggestions(self, student_profile=None):
        """
        Generate interesting topic suggestions for the student
        
        Args:
            student_profile (dict): Student's learning profile if available
            
        Returns:
            list: List of suggested topics for discussion
        """
        try:
            # Customize suggestions based on student profile
            prompt = "Generate 5 interesting educational topics that a student might want to discuss. "
            
            if student_profile:
                strengths = student_profile.get('strengths', [])
                weaknesses = student_profile.get('weaknesses', [])
                learning_style = student_profile.get('learning_style', 'unknown')
                
                if strengths:
                    prompt += f"The student is strong in: {', '.join(strengths)}. "
                if weaknesses:
                    prompt += f"The student could improve in: {', '.join(weaknesses)}. "
                
                prompt += f"Their learning style is: {learning_style}. "
            
            prompt += """
            Provide topics that are:
            1. Educational and engaging
            2. Suitable for curious students
            3. Encourage deeper thinking
            4. Cover diverse subjects
            
            Format as a JSON list of topics only, like: ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational content curator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            topics_data = json.loads(content)
            
            # Handle different possible JSON structures
            if isinstance(topics_data, list):
                return topics_data[:5]
            elif isinstance(topics_data, dict) and 'topics' in topics_data:
                return topics_data['topics'][:5]
            else:
                # Fallback topics if JSON parsing fails
                return [
                    "The Science Behind Everyday Things",
                    "History's Most Fascinating Mysteries",
                    "How Technology is Changing Our World",
                    "The Math in Art and Music",
                    "Environmental Science and Climate Change"
                ]
                
        except Exception as e:
            # Fallback topics if API call fails
            return [
                "Space Exploration and Astronomy",
                "The Human Body and Health",
                "World Cultures and Geography",
                "Computer Science and Programming",
                "Literature and Creative Writing"
            ]
    
    def generate_conversation_starters(self, topic):
        """
        Generate conversation starters for a specific topic
        
        Args:
            topic (str): The topic to generate starters for
            
        Returns:
            list: List of conversation starter questions
        """
        try:
            prompt = f"""Generate 3 engaging conversation starter questions about "{topic}" that would:
            1. Spark curiosity and interest
            2. Be appropriate for students
            3. Encourage deeper thinking
            4. Be open-ended rather than yes/no questions
            
            Format as a JSON list: ["Question 1?", "Question 2?", "Question 3?"]
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational conversation facilitator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            questions_data = json.loads(content)
            
            # Handle different possible JSON structures
            if isinstance(questions_data, list):
                return questions_data[:3]
            elif isinstance(questions_data, dict) and 'questions' in questions_data:
                return questions_data['questions'][:3]
            else:
                # Fallback questions
                return [
                    f"What's the most interesting thing you know about {topic}?",
                    f"How does {topic} connect to your daily life?",
                    f"What would you like to learn more about regarding {topic}?"
                ]
                
        except Exception as e:
            # Fallback questions if API call fails
            return [
                f"What's the most interesting thing you know about {topic}?",
                f"How does {topic} connect to your daily life?",
                f"What questions do you have about {topic}?"
            ]