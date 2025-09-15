"""
Script to seed the SAWA rubric with the exact framework from the PDF
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.sawa_rubric import SAWARubric

def seed_sawa_rubric():
    """Seed the SAWA rubric with the exact framework"""
    db = SessionLocal()
    
    try:
        # Clear existing rubric data
        db.query(SAWARubric).delete()
        
        # CLAIM RUBRIC
        claim_rubric = [
            {
                "facet": "claim",
                "level": 1,
                "level_name": "weak",
                "description": "No claim or factual statement",
                "example_responses": "GMO is food.\nClimate exists.\nVaccines exist.",
                "socratic_prompts": "What one-sentence position do you want to defend on this issue?",
                "feedback_templates": "Make it contestable by stating a position someone could reasonably doubt."
            },
            {
                "facet": "claim",
                "level": 2,
                "level_name": "developing",
                "description": "Vague or simplistic claim; lacks specificity or scope",
                "example_responses": "GMO food is safe.\nClimate change is happening.\nVaccines work.",
                "socratic_prompts": "Could you add a condition that makes it more precise?",
                "feedback_templates": "Could you add a condition that makes it more precise?"
            },
            {
                "facet": "claim",
                "level": 3,
                "level_name": "proficient",
                "description": "Clear, arguable, and specific claim",
                "example_responses": "Current evidence suggests GMO crops are safe for human health.\nClimate change is primarily caused by human greenhouse gas emissions.\nmRNA vaccines significantly reduce hospitalizations.",
                "socratic_prompts": "What one-sentence position do you want to defend on this issue?",
                "feedback_templates": "Make it contestable by stating a position someone could reasonably doubt."
            },
            {
                "facet": "claim",
                "level": 4,
                "level_name": "advanced",
                "description": "Nuanced, arguable, scoped claim that acknowledges limits or conditions",
                "example_responses": "GMO crops are safe for human health under most conditions, though outcomes may differ by crop trait.\nAnthropogenic greenhouse gases are the primary driver of climate change since the mid-20th century, though regional variability complicates short-term patterns.\nmRNA vaccines reduce hospitalizations by 80–95% in most populations, though effectiveness wanes over time and varies by variant.",
                "socratic_prompts": "Could you add a condition that makes it more precise?",
                "feedback_templates": "Could you add a condition that makes it more precise?"
            }
        ]
        
        # EVIDENCE RUBRIC
        evidence_rubric = [
            {
                "facet": "evidence",
                "level": 1,
                "level_name": "weak",
                "description": "No evidence or irrelevant fact",
                "example_responses": "People say GMOs are fine.\nIt's hotter outside.\nMy family didn't get sick after shots.",
                "socratic_prompts": "What specific information will you use to support your claim?",
                "feedback_templates": "Name at least one source type and one criterion (e.g., peer review, sample size)."
            },
            {
                "facet": "evidence",
                "level": 2,
                "level_name": "developing",
                "description": "One piece of evidence, limited specificity or no credibility check",
                "example_responses": "The FDA says GMOs are safe.\nA report shows climate change is real.\nOne CDC report says vaccines help.",
                "socratic_prompts": "Where does this evidence come from, and why should your audience trust it?",
                "feedback_templates": "Name at least one credible source type and why you trust it."
            },
            {
                "facet": "evidence",
                "level": 3,
                "level_name": "proficient",
                "description": "Multiple relevant pieces of evidence, some evaluation of credibility",
                "example_responses": "Two government reports and a meta-analysis found GMOs safe.\nNASA and NOAA datasets show global temperatures rose 1.2°C since pre-industrial times.\nMultiple clinical trials show reduced hospitalizations after vaccination.",
                "socratic_prompts": "What makes this evidence stronger than other data you could cite?",
                "feedback_templates": "Name at least one credible source type and why you trust it."
            },
            {
                "facet": "evidence",
                "level": 4,
                "level_name": "advanced",
                "description": "Multiple sources, triangulated, with explicit discussion of reliability and limitations",
                "example_responses": "Meta-analyses of feeding studies and government reports show GMOs safe, though heterogeneity and publication bias remain concerns.\nNASA and NOAA datasets plus ice core records show a 1.2°C rise; limitations include regional variation and measurement uncertainties.\nMeta-analysis of 20 studies shows 85–95% reduction in hospitalizations, though protection wanes after 6 months.",
                "socratic_prompts": "What are the potential weaknesses of this evidence?",
                "feedback_templates": "Name at least one credible source type and why you trust it."
            }
        ]
        
        # REASONING RUBRIC
        reasoning_rubric = [
            {
                "facet": "reasoning",
                "level": 1,
                "level_name": "weak",
                "description": "Restates evidence or claim without explanation",
                "example_responses": "Because the study says so.\nTemps went up, so it's climate change.\nThe numbers show it.",
                "socratic_prompts": "How does your evidence actually support your claim?",
                "feedback_templates": "State a general rule or mechanism linking the two."
            },
            {
                "facet": "reasoning",
                "level": 2,
                "level_name": "developing",
                "description": "Implicit or oversimplified reasoning",
                "example_responses": "If studies show no risk, GMOs must be safe.\nIf temperature increased, humans caused it.\nIf fewer people are in hospitals, vaccines must work.",
                "socratic_prompts": "What principle or mechanism makes the evidence count?",
                "feedback_templates": "Don't just repeat evidence—what rule makes it count for your claim?"
            },
            {
                "facet": "reasoning",
                "level": 3,
                "level_name": "proficient",
                "description": "Explicit principle or mechanism links evidence to claim",
                "example_responses": "If long-term studies across traits show no adverse effects, GMO safety can be inferred.\nBecause greenhouse gases trap heat and emissions rose, temperature increases point to human-caused warming.\nBecause vaccination coincided with reduced hospitalizations, vaccines reduce severe illness.",
                "socratic_prompts": "Could the same evidence support a different claim?",
                "feedback_templates": "Don't just repeat evidence—what rule makes it count for your claim?"
            },
            {
                "facet": "reasoning",
                "level": 4,
                "level_name": "advanced",
                "description": "Explicit, nuanced principle with acknowledgment of assumptions or limitations",
                "example_responses": "Because long-term multi-trait studies show no adverse effects, GMOs are likely safe, though monitoring is needed for trait-specific risks.\nGreenhouse gases trap heat; rising emissions explain warming, though regional variability and short-term anomalies exist.\nBecause immune responses triggered by vaccination reduce viral load, hospitalization risk decreases, though waning requires boosters.",
                "socratic_prompts": "What assumption are you making when you connect evidence to your claim?",
                "feedback_templates": "Don't just repeat evidence—what rule makes it count for your claim?"
            }
        ]
        
        # BACKING RUBRIC
        backing_rubric = [
            {
                "facet": "backing",
                "level": 1,
                "level_name": "weak",
                "description": "No backing provided",
                "example_responses": "Because experts said so.\nBecause scientists believe it.\nDoctors recommend it.",
                "socratic_prompts": "What broader scientific principle supports your reasoning?",
                "feedback_templates": "Name a theory, model, or prior finding that justifies your rule."
            },
            {
                "facet": "backing",
                "level": 2,
                "level_name": "developing",
                "description": "Vague appeal to authority",
                "example_responses": "Because studies prove it.\nBecause research supports it.\nScience says vaccines are good.",
                "socratic_prompts": "Which established theory or model justifies this link?",
                "feedback_templates": "Name a theory, model, or consensus that makes your reasoning trustworthy."
            },
            {
                "facet": "backing",
                "level": 3,
                "level_name": "proficient",
                "description": "Explicit principle, theory, or prior study cited as backing",
                "example_responses": "Toxicology principles justify GMO safety testing.\nThe greenhouse effect explains how GHGs trap heat.\nAdaptive immunity explains how vaccines provide long-term protection.",
                "socratic_prompts": "Is there a consensus statement or guideline that reinforces your warrant?",
                "feedback_templates": "Name a theory, model, or consensus that makes your reasoning trustworthy."
            },
            {
                "facet": "backing",
                "level": 4,
                "level_name": "advanced",
                "description": "Explicit principle plus supporting evidence or consensus with limitations acknowledged",
                "example_responses": "Toxicology principles and international risk-assessment frameworks justify GMO safety, though different crops may require tailored assessments.\nThe greenhouse effect, confirmed by climate models and consensus reports, explains warming, though local variability remains.\nAdaptive immunity, supported by immunology consensus and decades of evidence, explains vaccine protection, though waning requires boosters.",
                "socratic_prompts": "What prior studies or meta-analyses strengthen this reasoning?",
                "feedback_templates": "Name a theory, model, or consensus that makes your reasoning trustworthy."
            }
        ]
        
        # QUALIFIER RUBRIC
        qualifier_rubric = [
            {
                "facet": "qualifier",
                "level": 1,
                "level_name": "weak",
                "description": "Absolute claim, no qualifier",
                "example_responses": "GMOs are always safe.\nHumans always cause climate change.\nVaccines always work.",
                "socratic_prompts": "Does your claim hold in all cases or only under certain conditions?",
                "feedback_templates": "Calibrate scope using a condition or likelihood."
            },
            {
                "facet": "qualifier",
                "level": 2,
                "level_name": "developing",
                "description": "Implicit qualifier but vague",
                "example_responses": "GMOs are safe.\nHumans cause climate change.\nVaccines work.",
                "socratic_prompts": "How confident are you in your claim, based on current evidence?",
                "feedback_templates": "Science rarely deals in absolutes—restate with 'likely,' 'generally,' or under specific conditions."
            },
            {
                "facet": "qualifier",
                "level": 3,
                "level_name": "proficient",
                "description": "Explicit, conditional qualifier",
                "example_responses": "GMOs are generally safe for human health.\nHuman emissions are likely the primary driver of recent warming.\nmRNA vaccines reduce hospitalizations in most cases.",
                "socratic_prompts": "Can you phrase your claim using 'likely,' 'in most cases,' or 'under __ conditions'?",
                "feedback_templates": "Science rarely deals in absolutes—restate with 'likely,' 'generally,' or under specific conditions."
            },
            {
                "facet": "qualifier",
                "level": 4,
                "level_name": "advanced",
                "description": "Explicit qualifier with nuance tied to evidence limitations",
                "example_responses": "GMOs are generally safe, though trait-specific risks and environmental conditions may affect outcomes.\nHuman emissions are the primary cause since 1950, though regional variability complicates attribution.\nmRNA vaccines reduce hospitalizations by 80–95%, though protection wanes over time and varies by variant.",
                "socratic_prompts": "What limitations in your evidence make you cautious?",
                "feedback_templates": "Science rarely deals in absolutes—restate with 'likely,' 'generally,' or under specific conditions."
            }
        ]
        
        # REBUTTAL RUBRIC
        rebuttal_rubric = [
            {
                "facet": "rebuttal",
                "level": 1,
                "level_name": "weak",
                "description": "No counterargument mentioned",
                "example_responses": "There is no counterargument.\nEveryone agrees climate change is real.\nThere's no real counterargument.",
                "socratic_prompts": "What is the strongest counterargument to your claim?",
                "feedback_templates": "Strengthen the counter by using the best opposing case."
            },
            {
                "facet": "rebuttal",
                "level": 2,
                "level_name": "developing",
                "description": "Vague or strawman counterargument",
                "example_responses": "Some people don't like GMOs.\nSome say it's natural.\nSome people don't trust vaccines.",
                "socratic_prompts": "How might someone with a different perspective challenge your evidence?",
                "feedback_templates": "What would a knowledgeable opponent say?"
            },
            {
                "facet": "rebuttal",
                "level": 3,
                "level_name": "proficient",
                "description": "Identifies a credible counter and offers a limited response",
                "example_responses": "Some studies report enzyme differences, but results are inconsistent.\nSome argue warming is due to natural variability, but long-term attribution studies show anthropogenic causes dominate.\nSome argue vaccine effectiveness wanes, but evidence shows boosters restore it.",
                "socratic_prompts": "If a study contradicted your claim, how would you respond?",
                "feedback_templates": "What would a knowledgeable opponent say?"
            },
            {
                "facet": "rebuttal",
                "level": 4,
                "level_name": "advanced",
                "description": "Identifies a strong counter and provides a principled, nuanced response strategy",
                "example_responses": "Some studies show enzyme differences in GMO-fed animals; I would limit my claim by noting small samples and inconsistent protocols, so broader safety still holds.\nNatural variability explains short-term patterns, but attribution studies using multiple methods confirm anthropogenic forcing as the primary driver of long-term warming.\nEffectiveness wanes after 6 months; I would qualify my claim by time and note that boosters restore high protection levels.",
                "socratic_prompts": "How will you respond—by conceding, limiting scope, or offering a competing explanation?",
                "feedback_templates": "What would a knowledgeable opponent say?"
            }
        ]
        
        # Combine all rubric data
        all_rubric_data = claim_rubric + evidence_rubric + reasoning_rubric + backing_rubric + qualifier_rubric + rebuttal_rubric
        
        # Insert all rubric entries
        for rubric_data in all_rubric_data:
            rubric_entry = SAWARubric(**rubric_data)
            db.add(rubric_entry)
        
        db.commit()
        print("✅ SAWA rubric seeded successfully!")
        print(f"Added {len(all_rubric_data)} rubric entries across 6 facets")
        
    except Exception as e:
        print(f"❌ Error seeding SAWA rubric: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_sawa_rubric()
