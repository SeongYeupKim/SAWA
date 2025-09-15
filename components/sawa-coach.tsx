'use client';

import { useState } from 'react';
import { Facet } from '@/lib/types';

interface Progress {
  completedStages: number;
  totalStages: number;
  currentStage: string;
  overallLevel: number;
}

export default function SAWACoach() {
  const [sessionId, setSessionId] = useState<string>('');
  const [topic, setTopic] = useState<string>('');
  const [currentQuestion, setCurrentQuestion] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [feedback, setFeedback] = useState<string>('');
  const [progress, setProgress] = useState<Progress | null>(null);
  const [loading, setLoading] = useState(false);
  const [started, setStarted] = useState(false);
  const [completed, setCompleted] = useState(false);

  const startSession = async () => {
    if (!topic.trim()) return;

    setLoading(true);
    try {
      const res = await fetch('/api/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      });

      const data = await res.json();
      setSessionId(data.sessionId);
      setCurrentQuestion(data.firstQuestion);
      setStarted(true);
      setFeedback('');
    } catch (error) {
      console.error('Failed to start session:', error);
      setFeedback('Failed to start session. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const submitResponse = async () => {
    if (!response.trim()) return;

    setLoading(true);
    try {
      const res = await fetch('/api/session/respond', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, response }),
      });

      const data = await res.json();

      if (data.evaluation) {
        const feedbackText = data.evaluation.passed
          ? `✅ Excellent! ${data.evaluation.feedback}`
          : `💭 ${data.evaluation.feedback}\n\nSuggestions:\n${data.evaluation.suggestions.map((s: string) => `• ${s}`).join('\n')}`;

        setFeedback(feedbackText);
      }

      if (data.nextQuestion) {
        setCurrentQuestion(data.nextQuestion);
      }

      if (data.progress) {
        setProgress(data.progress);
      }

      if (data.completed) {
        setCompleted(true);
        setCurrentQuestion('Congratulations! You have completed all stages of your argumentative essay framework.');
      }

      setResponse('');
    } catch (error) {
      console.error('Failed to submit response:', error);
      setFeedback('Failed to submit response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const exportPrepSheet = async () => {
    window.open(`/api/session/export?sessionId=${sessionId}`, '_blank');
  };

  const stageNames: Record<string, string> = {
    claim: 'Claim',
    evidence: 'Evidence',
    reasoning: 'Reasoning',
    backing: 'Backing',
    qualifier: 'Qualifier',
    rebuttal: 'Rebuttal',
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">SAWA - Scientific Argumentative Writing Assistant</h1>

      {!started ? (
        <div className="space-y-4">
          <div>
            <label htmlFor="topic" className="block text-sm font-medium mb-2">
              Enter your essay topic:
            </label>
            <input
              id="topic"
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g., The impact of AI on education"
              className="w-full p-3 border rounded-lg"
              disabled={loading}
            />
          </div>
          <button
            onClick={startSession}
            disabled={loading || !topic.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Starting...' : 'Start Writing Coach'}
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Progress Bar */}
          {progress && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="flex justify-between text-sm mb-2">
                <span>Stage: {stageNames[progress.currentStage]}</span>
                <span>{progress.completedStages} of {progress.totalStages} completed</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${(progress.completedStages / progress.totalStages) * 100}%` }}
                />
              </div>
            </div>
          )}

          {/* Current Question */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="font-semibold mb-2">Current Question:</h3>
            <p className="text-gray-700">{currentQuestion}</p>
          </div>

          {/* Feedback */}
          {feedback && (
            <div className={`p-4 rounded-lg ${feedback.startsWith('✅') ? 'bg-green-50' : 'bg-yellow-50'}`}>
              <pre className="whitespace-pre-wrap text-sm">{feedback}</pre>
            </div>
          )}

          {/* Response Input */}
          {!completed && (
            <div>
              <label htmlFor="response" className="block text-sm font-medium mb-2">
                Your Response:
              </label>
              <textarea
                id="response"
                value={response}
                onChange={(e) => setResponse(e.target.value)}
                rows={6}
                className="w-full p-3 border rounded-lg"
                placeholder="Type your response here..."
                disabled={loading}
              />
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-4">
            {!completed ? (
              <button
                onClick={submitResponse}
                disabled={loading || !response.trim()}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Submit Response'}
              </button>
            ) : (
              <button
                onClick={exportPrepSheet}
                className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Export Prep Sheet
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}