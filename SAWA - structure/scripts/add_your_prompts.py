"""
Script to add your original SAWA prompt concepts and processes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.prompt import Prompt
from app.models.user import User
from app.core.auth import get_password_hash

def add_your_prompts():
    """Add your original prompt concepts and processes"""
    db = SessionLocal()
    
    try:
        # Get or create a teacher user
        teacher = db.query(User).filter(User.username == "teacher").first()
        if not teacher:
            teacher = User(
                email="teacher@sawa.edu",
                username="teacher",
                full_name="Dr. Science Teacher",
                hashed_password=get_password_hash("teacher123"),
                is_teacher=True
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
        
        # ADD YOUR ORIGINAL PROMPT CONCEPTS HERE
        your_prompts = [
            {
                "title": "YOUR_PROMPT_TITLE_1",
                "content": "YOUR_PROMPT_CONTENT_1 - Replace this with your actual prompt content",
                "category": "YOUR_CATEGORY_1",  # e.g., "scientific_method", "argumentation", "evidence_evaluation"
                "difficulty_level": "YOUR_LEVEL_1",  # "beginner", "intermediate", "advanced"
                "subject_area": "YOUR_SUBJECT_1",  # e.g., "biology", "chemistry", "physics"
                "expected_elements": '["element1", "element2", "element3"]'  # JSON string of expected elements
            },
            {
                "title": "YOUR_PROMPT_TITLE_2",
                "content": "YOUR_PROMPT_CONTENT_2 - Replace this with your actual prompt content",
                "category": "YOUR_CATEGORY_2",
                "difficulty_level": "YOUR_LEVEL_2",
                "subject_area": "YOUR_SUBJECT_2",
                "expected_elements": '["element1", "element2", "element3"]'
            },
            # Add more prompts as needed
        ]
        
        for prompt_data in your_prompts:
            prompt = Prompt(
                **prompt_data,
                created_by=teacher.id
            )
            db.add(prompt)
        
        db.commit()
        print("✅ Your original prompts added successfully!")
        print(f"Added {len(your_prompts)} prompts")
        
    except Exception as e:
        print(f"❌ Error adding prompts: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("📝 Adding your original SAWA prompt concepts and processes...")
    print("⚠️  Please edit this script to include your actual prompt content")
    add_your_prompts()
