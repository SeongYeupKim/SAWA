# SAWA - Scientific Argumentative Writing Assistant

## 🎯 **Your Exact CER + Toulmin Framework Implementation**

This is your complete SAWA system implementing the exact framework from your PDF. No generic chatbot - this is your specific scientific argumentative writing assistant.

## ✅ **What's Implemented (From Your PDF)**

### **Core Framework**
- **CER (Claim–Evidence–Reasoning)** as the core structure
- **Toulmin extensions** (Backing, Qualifier, Rebuttal)
- **6 sequential stages**: Claim → Evidence → Reasoning → Backing → Qualifier → Rebuttal
- **Socratic questioning** with your exact prompts
- **4-level analytic rubric** (1=weak, 2=developing, 3=proficient, 4=advanced)

### **Your Specific Features**
- **One-move-at-a-time prompts** tied to specific argumentative roles
- **Minimal feedback phrased as "principled nudges"** when below threshold
- **Readiness gate**: Advance only when Level 3+ (proficient)
- **Prep sheet generation** with your exact format
- **Qualifier patterns** and sentence stems
- **Rebuttal strategies** (concede, limit scope, competing mechanism, challenge credibility)
- **Reasoning schemes** (causal, correlation, expert opinion, analogy, consequence)

## 🚀 **Quick Start**

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Run SAWA**
```bash
python test_sawa.py
```

Then visit: **http://localhost:8000/docs**

## 📋 **API Usage**

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

### **Get Framework Resources**
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

## 📁 **Project Structure**

```
SAWA - structure/
├── app/
│   ├── main.py                 # Main SAWA application
│   ├── models/
│   │   ├── user.py            # User model
│   │   ├── sawa_conversation.py  # SAWA conversation model
│   │   ├── sawa_message.py    # SAWA message model
│   │   └── sawa_rubric.py     # SAWA rubric model
│   ├── services/
│   │   └── sawa_service.py    # Core SAWA logic
│   ├── routers/
│   │   ├── auth.py            # Authentication
│   │   └── sawa.py            # SAWA endpoints
│   ├── schemas/
│   │   ├── user.py            # User schemas
│   │   └── sawa.py            # SAWA schemas
│   └── core/
│       ├── config.py          # Configuration
│       └── auth.py            # Authentication utilities
├── scripts/
│   └── seed_sawa_rubric.py    # Rubric data seeding
├── test_sawa.py               # Test server
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🎉 **This is Your SAWA System**

The system implements:
- Your specific conversation flow
- Your exact Socratic questions
- Your precise evaluation criteria
- Your feedback pivot logic
- Your prep sheet format
- Your qualifier patterns
- Your rebuttal strategies
- Your reasoning schemes

**This is your exact SAWA framework brought to life!**

## 🔧 **Development**

### **Run Tests**
```bash
python test_sawa.py
```

### **Access Documentation**
Visit `http://localhost:8000/docs` when the server is running.

### **API Testing**
Use the interactive documentation at `/docs` or test with curl:

```bash
# Start conversation
curl -X POST "http://localhost:8000/api/sawa/start" \
  -H "Content-Type: application/json" \
  -d '{"topic": "GMO safety"}'

# Respond to question
curl -X POST "http://localhost:8000/api/sawa/respond" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 1, "content": "GMOs are generally safe for human consumption"}'
```

## 📝 **License**

This project implements your specific SAWA framework for scientific argumentative writing assistance.