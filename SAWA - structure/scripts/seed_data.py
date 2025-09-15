"""
Script to seed the database with sample prompts and data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import user, prompt, conversation, message, feedback
from app.models.user import User
from app.models.prompt import Prompt
from app.core.auth import get_password_hash

def create_sample_data():
    """Create sample data for the SAWA application"""
    db = SessionLocal()
    
    try:
        # Create sample teacher user
        teacher_user = User(
            email="teacher@sawa.edu",
            username="teacher",
            full_name="Dr. Science Teacher",
            hashed_password=get_password_hash("teacher123"),
            is_teacher=True
        )
        db.add(teacher_user)
        db.commit()
        db.refresh(teacher_user)
        
        # Create sample student user
        student_user = User(
            email="student@sawa.edu",
            username="student",
            full_name="Science Student",
            hashed_password=get_password_hash("student123"),
            is_teacher=False
        )
        db.add(student_user)
        db.commit()
        db.refresh(student_user)
        
        # Create sample prompts
        sample_prompts = [
            {
                "title": "Climate Change and Greenhouse Gases",
                "content": "Write a scientific argument about the role of greenhouse gases in climate change. Your argument should include: 1) A clear thesis statement, 2) Evidence from scientific studies, 3) Explanation of the greenhouse effect, 4) Discussion of human activities that contribute to greenhouse gas emissions, and 5) A conclusion that summarizes your position.",
                "category": "environmental_science",
                "difficulty_level": "intermediate",
                "subject_area": "environmental_science",
                "expected_elements": '["thesis", "evidence", "greenhouse_effect", "human_activities", "conclusion"]'
            },
            {
                "title": "Evolution and Natural Selection",
                "content": "Present a scientific argument explaining how natural selection drives evolution. Your response should address: 1) The basic principles of natural selection, 2) Evidence for evolution from fossil records, 3) Examples of natural selection in action, 4) How genetic variation contributes to evolution, and 5) Why evolution is considered a scientific theory.",
                "category": "biology",
                "difficulty_level": "intermediate",
                "subject_area": "biology",
                "expected_elements": '["natural_selection_principles", "fossil_evidence", "examples", "genetic_variation", "scientific_theory"]'
            },
            {
                "title": "Photosynthesis and Energy Flow",
                "content": "Explain the process of photosynthesis and its importance in energy flow through ecosystems. Include: 1) The chemical equation for photosynthesis, 2) The role of chlorophyll and light energy, 3) How photosynthesis contributes to the carbon cycle, 4) The relationship between photosynthesis and cellular respiration, and 5) Why plants are considered primary producers.",
                "category": "biology",
                "difficulty_level": "beginner",
                "subject_area": "biology",
                "expected_elements": '["chemical_equation", "chlorophyll_role", "carbon_cycle", "cellular_respiration", "primary_producers"]'
            },
            {
                "title": "Atomic Structure and Chemical Bonding",
                "content": "Describe the structure of atoms and explain how chemical bonds form between atoms. Your argument should cover: 1) The basic structure of atoms (protons, neutrons, electrons), 2) How the periodic table is organized, 3) Types of chemical bonds (ionic, covalent, metallic), 4) Examples of each type of bond, and 5) How bonding affects the properties of compounds.",
                "category": "chemistry",
                "difficulty_level": "intermediate",
                "subject_area": "chemistry",
                "expected_elements": '["atomic_structure", "periodic_table", "bond_types", "examples", "compound_properties"]'
            },
            {
                "title": "Newton's Laws of Motion",
                "content": "Explain Newton's three laws of motion and provide real-world examples of each. Include: 1) A clear statement of each law, 2) Mathematical relationships where applicable, 3) Everyday examples that demonstrate each law, 4) How the laws work together in complex situations, and 5) Why these laws are fundamental to understanding motion.",
                "category": "physics",
                "difficulty_level": "beginner",
                "subject_area": "physics",
                "expected_elements": '["law_statements", "mathematical_relationships", "examples", "complex_situations", "fundamental_importance"]'
            }
        ]
        
        for prompt_data in sample_prompts:
            prompt = Prompt(
                **prompt_data,
                created_by=teacher_user.id
            )
            db.add(prompt)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
