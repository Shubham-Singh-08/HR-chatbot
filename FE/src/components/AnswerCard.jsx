export default function AnswerCard({ answer }) {
  if (!answer) return null;

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 mt-6 animate-fade-in">
      <div className="flex items-center space-x-3 mb-4">
        <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center">
          <span className="text-white text-sm">✓</span>
        </div>
        <h3 className="text-lg font-semibold text-gray-800">Answer</h3>
      </div>
      <div className="prose prose-blue max-w-none">
        <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{answer}</p>
      </div>
    </div>
  );
}
