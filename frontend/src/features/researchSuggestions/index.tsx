import React from 'react';
import { ResearchSuggestionForm } from './components/ResearchSuggestionForm';
import { ResearchSuggestionResults } from './components/ResearchSuggestionResults';
import { useResearchSuggestions } from './hooks/useResearchSuggestions';

export const ResearchSuggestionsPage: React.FC = () => {
  const { data, isLoading, error, generateSuggestions } = useResearchSuggestions();

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Research Suggestions</h1>
        <p className="text-gray-600">
          Rapidly brainstorm emerging topics, research gaps, and study designs for your next biomedical project.
        </p>
      </div>

      <ResearchSuggestionForm onSubmit={generateSuggestions} isLoading={isLoading} />

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-r-lg">
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-red-700 font-medium">Error generating suggestions</p>
              <p className="text-sm text-red-600 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {data && <ResearchSuggestionResults response={data} />}
    </div>
  );
};
