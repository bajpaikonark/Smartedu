import random

class QuizContent:
    def __init__(self):
        self.question_bank = {
            'Mathematics': {
                'beginner': [
                    {
                        'question': 'What is 5 + 3?',
                        'options': ['6', '7', '8', '9'],
                        'correct_answer': '8',
                        'explanation': '5 + 3 = 8. Addition is combining two numbers.'
                    },
                    {
                        'question': 'What is 12 - 4?',
                        'options': ['6', '7', '8', '9'],
                        'correct_answer': '8',
                        'explanation': '12 - 4 = 8. Subtraction means taking away.'
                    },
                    {
                        'question': 'What is 3 × 4?',
                        'options': ['10', '11', '12', '13'],
                        'correct_answer': '12',
                        'explanation': '3 × 4 = 12. Multiplication is repeated addition.'
                    },
                    {
                        'question': 'What is 15 ÷ 3?',
                        'options': ['4', '5', '6', '7'],
                        'correct_answer': '5',
                        'explanation': '15 ÷ 3 = 5. Division splits a number into equal parts.'
                    },
                    {
                        'question': 'Which number is larger: 17 or 19?',
                        'options': ['17', '19', 'They are equal', 'Cannot determine'],
                        'correct_answer': '19',
                        'explanation': '19 > 17. When comparing numbers, 19 is greater than 17.'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'What is 25% of 80?',
                        'options': ['15', '20', '25', '30'],
                        'correct_answer': '20',
                        'explanation': '25% of 80 = 0.25 × 80 = 20'
                    },
                    {
                        'question': 'Solve: 2x + 5 = 15',
                        'options': ['x = 3', 'x = 5', 'x = 7', 'x = 10'],
                        'correct_answer': 'x = 5',
                        'explanation': '2x + 5 = 15, so 2x = 10, therefore x = 5'
                    },
                    {
                        'question': 'What is the area of a rectangle with length 8 and width 6?',
                        'options': ['14', '28', '42', '48'],
                        'correct_answer': '48',
                        'explanation': 'Area = length × width = 8 × 6 = 48 square units'
                    },
                    {
                        'question': 'What is √64?',
                        'options': ['6', '7', '8', '9'],
                        'correct_answer': '8',
                        'explanation': '√64 = 8 because 8 × 8 = 64'
                    }
                ],
                'advanced': [
                    {
                        'question': 'What is the derivative of x² + 3x?',
                        'options': ['2x + 3', 'x + 3', '2x²', 'x² + 3'],
                        'correct_answer': '2x + 3',
                        'explanation': 'd/dx(x²) = 2x and d/dx(3x) = 3, so the derivative is 2x + 3'
                    },
                    {
                        'question': 'Solve the quadratic equation: x² - 5x + 6 = 0',
                        'options': ['x = 2, 3', 'x = 1, 6', 'x = -2, -3', 'x = 0, 5'],
                        'correct_answer': 'x = 2, 3',
                        'explanation': 'Factoring: (x-2)(x-3) = 0, so x = 2 or x = 3'
                    }
                ]
            },
            'Science': {
                'beginner': [
                    {
                        'question': 'What gas do plants absorb from the air?',
                        'options': ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Hydrogen'],
                        'correct_answer': 'Carbon Dioxide',
                        'explanation': 'Plants absorb CO₂ from the air for photosynthesis.'
                    },
                    {
                        'question': 'How many bones are in the adult human body?',
                        'options': ['196', '206', '216', '226'],
                        'correct_answer': '206',
                        'explanation': 'The adult human skeleton has 206 bones.'
                    },
                    {
                        'question': 'What is the chemical symbol for water?',
                        'options': ['H₂O', 'CO₂', 'O₂', 'NaCl'],
                        'correct_answer': 'H₂O',
                        'explanation': 'Water is composed of 2 hydrogen atoms and 1 oxygen atom.'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'What is the powerhouse of the cell?',
                        'options': ['Nucleus', 'Mitochondria', 'Ribosome', 'Chloroplast'],
                        'correct_answer': 'Mitochondria',
                        'explanation': 'Mitochondria produce ATP, the energy currency of cells.'
                    },
                    {
                        'question': 'What is the speed of light in vacuum?',
                        'options': ['3×10⁶ m/s', '3×10⁷ m/s', '3×10⁸ m/s', '3×10⁹ m/s'],
                        'correct_answer': '3×10⁸ m/s',
                        'explanation': 'Light travels at approximately 300,000,000 meters per second.'
                    }
                ],
                'advanced': [
                    {
                        'question': 'What is the molecular formula for glucose?',
                        'options': ['C₆H₁₂O₆', 'C₆H₆O₆', 'C₁₂H₂₂O₁₁', 'C₂H₅OH'],
                        'correct_answer': 'C₆H₁₂O₆',
                        'explanation': 'Glucose has 6 carbon, 12 hydrogen, and 6 oxygen atoms.'
                    }
                ]
            },
            'English': {
                'beginner': [
                    {
                        'question': 'What is the plural of "child"?',
                        'options': ['childs', 'children', 'childes', 'child'],
                        'correct_answer': 'children',
                        'explanation': '"Children" is the irregular plural form of "child".'
                    },
                    {
                        'question': 'Which word is a noun?',
                        'options': ['quickly', 'run', 'happiness', 'beautiful'],
                        'correct_answer': 'happiness',
                        'explanation': 'A noun is a person, place, thing, or idea. "Happiness" is an abstract noun.'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'Identify the metaphor: "Time is money"',
                        'options': ['Time and money are similar', 'Time is valuable like money', 'Time costs money', 'Money buys time'],
                        'correct_answer': 'Time is valuable like money',
                        'explanation': 'This metaphor compares time to money, suggesting both are valuable resources.'
                    }
                ],
                'advanced': [
                    {
                        'question': 'What literary device is used in "The wind whispered"?',
                        'options': ['Metaphor', 'Simile', 'Personification', 'Alliteration'],
                        'correct_answer': 'Personification',
                        'explanation': 'Personification gives human qualities (whispering) to non-human things (wind).'
                    }
                ]
            }
        }
    
    def get_available_topics(self):
        """Return list of available topics"""
        return list(self.question_bank.keys())
    
    def get_questions(self, topic, difficulty, num_questions=5):
        """Get questions for specified topic and difficulty"""
        if topic not in self.question_bank:
            topic = 'Mathematics'  # Default fallback
        
        if difficulty not in self.question_bank[topic]:
            difficulty = 'beginner'  # Default fallback
        
        available_questions = self.question_bank[topic][difficulty]
        
        # Select random questions (with replacement if needed)
        if len(available_questions) >= num_questions:
            selected_questions = random.sample(available_questions, num_questions)
        else:
            # If not enough questions, repeat some
            selected_questions = available_questions * (num_questions // len(available_questions) + 1)
            selected_questions = selected_questions[:num_questions]
        
        return selected_questions
    
    def add_question(self, topic, difficulty, question_data):
        """Add a new question to the bank"""
        if topic not in self.question_bank:
            self.question_bank[topic] = {}
        
        if difficulty not in self.question_bank[topic]:
            self.question_bank[topic][difficulty] = []
        
        self.question_bank[topic][difficulty].append(question_data)
    
    def get_question_stats(self):
        """Get statistics about the question bank"""
        stats = {}
        total_questions = 0
        
        for topic, difficulties in self.question_bank.items():
            topic_count = 0
            for difficulty, questions in difficulties.items():
                count = len(questions)
                topic_count += count
                total_questions += count
            stats[topic] = topic_count
        
        stats['total'] = total_questions
        return stats
