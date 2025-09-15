# SAWA - Scientific Argumentative Writing Assistant

AI-powered Socratic writing coach implementing the Toulmin argumentation framework.

## Features

- **6-Stage Toulmin Framework**: Claim, Evidence, Reasoning, Backing, Qualifier, Rebuttal
- **AI-Powered Evaluation**: Intelligent feedback using OpenAI/Anthropic
- **Socratic Method**: Guided questioning for deeper understanding
- **4-Level Assessment**: Detailed rubric-based evaluation
- **Session Management**: Save and export your work

## Setup

1. Clone the repository
2. Install dependencies: `npm install`
3. Add API keys to `.env.local`:
   ```
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```
4. Run development server: `npm run dev`
5. Open http://localhost:3000

## Deployment

This project is configured for Vercel deployment:
1. Push to GitHub
2. Import to Vercel
3. Add environment variables
4. Deploy

## Architecture

- **Frontend**: Next.js 14 with TypeScript
- **AI Integration**: OpenAI GPT-4 / Anthropic Claude
- **Session Storage**: File-based (upgradeable to database)
- **Evaluation**: AI-driven with fallback rules

## Based On

Inspired by the SAWA prototype structure from GitHub, enhanced with modern AI capabilities.