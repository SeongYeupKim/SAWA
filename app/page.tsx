import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              SAWA
            </h1>
            <p className="text-xl text-gray-600 mb-2">
              Scientific Argumentative Writing Assistant
            </p>
            <p className="text-lg text-gray-500">
              AI-Powered Socratic Writing Coach v2.0
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 gap-6 mb-12">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-3 text-blue-600">
                🎯 Toulmin Framework
              </h3>
              <p className="text-gray-600">
                Master the six essential components of argumentation: Claim, Evidence, Reasoning, Backing, Qualifier, and Rebuttal.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-3 text-blue-600">
                🤖 AI-Powered Evaluation
              </h3>
              <p className="text-gray-600">
                Get intelligent, context-aware feedback from advanced AI that understands your argument&apos;s nuances.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-3 text-blue-600">
                💭 Socratic Method
              </h3>
              <p className="text-gray-600">
                Learn through guided questioning that helps you discover insights rather than being told answers.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-3 text-blue-600">
                📊 4-Level Assessment
              </h3>
              <p className="text-gray-600">
                Track your progress with detailed rubric-based evaluation from Underdeveloped to Excellent.
              </p>
            </div>
          </div>

          {/* Process Steps */}
          <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
            <h2 className="text-2xl font-bold mb-6 text-center">
              Your Writing Journey
            </h2>
            <div className="space-y-4">
              {[
                { step: 1, title: 'Claim', desc: 'Develop a specific, contestable argument' },
                { step: 2, title: 'Evidence', desc: 'Plan reliable data to support your claim' },
                { step: 3, title: 'Reasoning', desc: 'Connect evidence to claim logically' },
                { step: 4, title: 'Backing', desc: 'Ground reasoning in established theory' },
                { step: 5, title: 'Qualifier', desc: 'Acknowledge limitations and conditions' },
                { step: 6, title: 'Rebuttal', desc: 'Address counterarguments effectively' },
              ].map((item) => (
                <div key={item.step} className="flex items-start">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold">
                    {item.step}
                  </div>
                  <div className="ml-4">
                    <h3 className="font-semibold">{item.title}</h3>
                    <p className="text-gray-600 text-sm">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* CTA */}
          <div className="text-center">
            <Link
              href="/coach"
              className="inline-block px-8 py-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition shadow-lg"
            >
              Start Writing Coach →
            </Link>
            <p className="mt-4 text-gray-500 text-sm">
              No sign-up required • AI-powered feedback • Export your work
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}