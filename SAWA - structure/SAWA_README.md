# SAWA - Scientific Argumentative Writing Assistant

## 🎯 **Complete Implementation of Your CER + Toulmin Framework**

I have now **completely rebuilt** the system to reflect your exact SAWA concepts and processes from the PDF. This is no longer a generic chatbot - it's your specific scientific argumentative writing assistant.

## ✅ **What's Now Implemented (Exactly from Your PDF)**

### **1. Core Framework**
- **CER (Claim–Evidence–Reasoning)** as the core structure
- **Toulmin extensions** (Backing, Qualifier, Rebuttal)
- **6 sequential stages**: Claim → Evidence → Reasoning → Backing → Qualifier → Rebuttal
- **Socratic questioning** with targeted prompts for each stage
- **4-level analytic rubric** (1=weak, 2=developing, 3=proficient, 4=advanced)

### **2. Socratic Questioning System**
- **One-move-at-a-time prompts** tied to specific argumentative roles
- **Explicit checks for completeness** before advancing
- **Minimal feedback phrased as "principled nudges"** when answers miss threshold
- **Immediate return to questions** after feedback

### **3. Evaluation & Feedback Logic**
- **Internal analytic rubric** with 4 levels per facet
- **Default behavior is questioning** - only pivots to feedback when below threshold
- **Preserves student agency** while preventing unproductive loops
- **Readiness gate**: Advance only when each facet reaches Level 3+ (proficient)

### **4. Prep Sheet Generation**
- **Concise prep sheet** with fields: Claim, Evidence Plan, Reasoning/Warrant, Backing, Qualifier, Rebuttal Plan
- **Student-owned statements** that can be copied into essays
- **Fixed structure** for clarity and consistency

### **5. Qualifier Patterns & Sentence Stems**
- **Certainty scale**: always → almost always → generally → often → sometimes → rarely
- **Probability scale**: certainly → very likely → likely → possible → unlikely
- **Sentence stems** for qualified claims
- **Feedback triggers** for absolute language

### **6. Rebuttal Strategies**
- **4 response strategies**: Concede with boundary, Limit scope, Offer competing mechanism, Challenge credibility
- **Socratic prompts** to move beyond dismissive counters
- **Sentence stems** for professional rebuttals

### **7. Reasoning Schemes**
- **Causal/mechanistic reasoning**
- **Correlation reasoning**
- **Expert opinion reasoning**
- **Analogical reasoning**
- **Consequence reasoning**

## 🚀 **How to Test Your SAWA System**

### **Quick Test (No Database Required)**
```bash
# Install minimal dependencies
pip install fastapi uvicorn

# Run the SAWA test server
python test_sawa.py
```

Then visit: **http://localhost:8000/docs**

### **Full System with Database**
```bash
# Install all dependencies
pip install -r requirements.txt

# Set up database and seed rubric
python scripts/seed_sawa_rubric.py

# Run the full system
python run_server.py
```

## 📋 **API Endpoints (Your Exact Framework)**

### **Start SAWA Conversation**
```bash
POST /api/sawa/start
{
  "topic": "GMO safety"
}
```

### **Process Student Response**
```bash
POST /api/sawa/respond
{
  "conversation_id": 1,
  "content": "GMOs are generally safe for human consumption"
}
```

### **Get Rubric Information**
```bash
GET /api/sawa/rubric/claim
GET /api/sawa/rubric/evidence
GET /api/sawa/rubric/reasoning
GET /api/sawa/rubric/backing
GET /api/sawa/rubric/qualifier
GET /api/sawa/rubric/rebuttal
```

### **Get Reasoning Schemes**
```bash
GET /api/sawa/reasoning-schemes
GET /api/sawa/qualifier-patterns
GET /api/sawa/rebuttal-strategies
```

## 🔄 **Example Conversation Flow**

1. **Start**: "What one-sentence position do you want to defend on this issue?"
2. **Student**: "GMOs are safe"
3. **SAWA**: "Could you add a condition that makes it more precise?"
4. **Student**: "GMOs are generally safe for human consumption"
5. **SAWA**: "What specific information will you use to support your claim?"
6. **Continue through all 6 stages...**
7. **Final**: Generate prep sheet with all responses

## 📊 **Rubric Implementation**

Each stage is evaluated using your exact 4-level rubric:

- **Level 1 (Weak)**: Below threshold, triggers feedback
- **Level 2 (Developing)**: Below threshold, triggers feedback  
- **Level 3 (Proficient)**: Meets threshold, advances to next stage
- **Level 4 (Advanced)**: Exceeds threshold, advances to next stage

## 🎯 **Key Features from Your PDF**

### **Boundaries & Safety**
- ✅ No co-writing or paragraph generation
- ✅ No invention of evidence beyond student proposals
- ✅ No style/grammar coaching (content-and-logic only)
- ✅ Transparent decline when asked for unverified evidence

### **Interaction Design**
- ✅ Fine interaction grain (one targeted question per turn)
- ✅ Limited branching to smallest necessary correction
- ✅ 12-18 turn typical completion
- ✅ Student-owned statements for prep sheet

### **Success Criteria**
- ✅ Declarative, arguable claim
- ✅ Evidence plan with source type + evaluation criterion
- ✅ Explicit warrant linking evidence to claim
- ✅ Named backing (theory/model/prior finding)
- ✅ Calibrated qualifier matching evidence strength
- ✅ Serious counterargument + response strategy

## 🔧 **Files Created for Your Framework**

- **`app/main_sawa.py`** - Simplified SAWA implementation
- **`app/services/sawa_service.py`** - Core CER + Toulmin logic
- **`app/models/sawa_conversation.py`** - Conversation state management
- **`app/models/sawa_message.py`** - Socratic dialogue tracking
- **`app/models/sawa_rubric.py`** - 4-level evaluation rubric
- **`app/routers/sawa.py`** - API endpoints
- **`app/schemas/sawa.py`** - Data models
- **`scripts/seed_sawa_rubric.py`** - Rubric data seeding
- **`test_sawa.py`** - Test server

## 🎉 **This is Now Your Exact SAWA System**

The system now implements:
- Your specific conversation flow
- Your exact Socratic questions
- Your precise evaluation criteria
- Your feedback pivot logic
- Your prep sheet format
- Your qualifier patterns
- Your rebuttal strategies
- Your reasoning schemes

**This is no longer a generic chatbot - it's your SAWA framework brought to life!**

Try it out with: `python test_sawa.py` and visit `http://localhost:8000/docs`
