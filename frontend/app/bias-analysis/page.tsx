'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import { BiasTable } from '@/components/bias-analysis/BiasTable'
import { ProfileComparison } from '@/components/bias-analysis/ProfileComparison'
import { Loader2 } from 'lucide-react'

export default function BiasAnalysisPage() {
  const [selectedMetricId, setSelectedMetricId] = useState<number | null>(null)

  const { data: metrics, isLoading, error } = useQuery({
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
        <span className="ml-2 text-gray-600">Loading bias analysis...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Data</h2>
        <p className="text-red-600">
          {error instanceof Error ? error.message : 'Failed to load bias analysis data'}
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Bias Analysis</h1>
        <p className="text-gray-600">
          Detailed bias findings across all test dimensions
        </p>
      </div>

      {(!metrics || metrics.length === 0) ? (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-blue-800 mb-2">No Bias Analysis Data Available</h2>
          <p className="text-blue-600 mb-4">
            No metrics have been calculated yet. To view bias analysis:
          </p>
          <ol className="list-decimal list-inside space-y-2 text-blue-700">
            <li>Generate synthetic student profiles</li>
            <li>Score profiles using both fair and biased models</li>
            <li>Calculate bias metrics</li>
            <li>Results will appear here</li>
          </ol>
          <p className="text-sm text-blue-600 mt-4">
            Use the API documentation at <a href="http://localhost:8000/docs" className="underline" target="_blank">http://localhost:8000/docs</a> to get started.
          </p>
        </div>
      ) : (
        <>
          <BiasTable
            metrics={metrics}
            onMetricSelect={setSelectedMetricId}
            selectedMetricId={selectedMetricId}
          />

          {selectedMetricId && (
            <ProfileComparison metricId={selectedMetricId} />
          )}
        </>
      )}
    </div>
  )
}

