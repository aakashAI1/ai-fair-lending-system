'use client'

import { FeedbackForm } from '@/components/feedback/FeedbackForm'
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import { Loader2 } from 'lucide-react'

export default function FeedbackPage() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: async () => {
      const response = await apiClient.get('/metrics/')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading metrics...</span>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Human Feedback</h1>
        <p className="text-gray-600">
          Provide feedback on bias findings to improve fairness
        </p>
      </div>

      {(!metrics || metrics.length === 0) ? (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-blue-800 mb-2">No Feedback Data Available</h2>
          <p className="text-blue-600 mb-4">
            No bias metrics available for feedback. To provide feedback:
          </p>
          <ol className="list-decimal list-inside space-y-2 text-blue-700">
            <li>Generate and score profiles</li>
            <li>Calculate bias metrics</li>
            <li>Review findings in the Bias Analysis page</li>
            <li>Provide feedback here to improve fairness</li>
          </ol>
          <p className="text-sm text-blue-600 mt-4">
            Use the API documentation at <a href="http://localhost:8000/docs" className="underline" target="_blank">http://localhost:8000/docs</a> to get started.
          </p>
        </div>
      ) : (
        <FeedbackForm metrics={metrics} />
      )}
    </div>
  )
}

