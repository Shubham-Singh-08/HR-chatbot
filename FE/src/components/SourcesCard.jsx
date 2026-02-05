export default function SourcesCard({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="bg-blue-50 rounded-2xl border border-blue-200 p-6 mt-4 animate-fade-in">
      <div className="flex items-center space-x-3 mb-4">
        <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
          <span className="text-white text-sm">📚</span>
        </div>
        <h3 className="text-lg font-semibold text-blue-800">Sources</h3>
      </div>
      <div className="flex flex-wrap gap-2">
        {sources.map((source, index) => (
          <span 
            key={index} 
            className="px-4 py-2 bg-white text-blue-700 rounded-full text-sm font-medium border border-blue-200 hover:bg-blue-100 transition-colors duration-200"
          >
            {source}
          </span>
        ))}
      </div>
    </div>
  );
}
