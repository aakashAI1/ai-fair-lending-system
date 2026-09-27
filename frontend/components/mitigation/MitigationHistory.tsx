'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Eye, Loader2, Calendar, TrendingUp, Target } from 'lucide-react'
import { MitigationDetailModal } from './MitigationDetailModal'

interface MitigationRun {
  mitigation_run_id: string
  created_at: string
  total_iterations: number
  initial_score: number
  final_score: number
  total_improvement: number
  improvement_percentage: number
  target_achieved: boolean
  feedback_ids: number[]
}

export function MitigationHistory() {
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null)

  const { data: runs, isLoading, error, refetch } = useQuery({
    queryKey: ['mitigation-runs'],
    queryFn: async () => {
      const response = await apiClient.get('/mitigation/')
      return response.data as MitigationRun[]
    },
    retry: (failureCount, error: any) => {
      // Don't retry on 401 or 403 errors (auth/permission issues)
      if (error?.response?.status === 401 || error?.response?.status === 403) {
        return false
      }
      return failureCount < 3
    },
  })

  // Handle 401 Unauthorized or 403 Forbidden (non-admin access)
  if (error && ((error as any)?.response?.status === 401 || (error as any)?.response?.status === 403)) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Mitigation History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-red-600 font-medium mb-2">Access Denied</p>
            <p className="text-gray-500 text-sm">
              {error?.response?.status === 401 
                ? 'Authentication required. Please log in again.'
                : 'Only administrators can view mitigation logs.'}
            </p>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-center h-32">
            <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
            <span className="ml-2 text-gray-600">Loading mitigation history...</span>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!runs || runs.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Mitigation History</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500 text-center py-8">
            No mitigation cycles have been run yet. Run a mitigation cycle to see results here.
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Mitigation History</CardTitle>
          <p className="text-sm text-gray-600 mt-1">
            All mitigation cycles that have been run, with persistent results
          </p>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {runs.map((run) => (
              <div
                key={run.mitigation_run_id}
                className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-md transition-all"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-lg text-gray-900">
                        {run.mitigation_run_id}
                      </h3>
                      {run.target_achieved && (
                        <span className="px-2 py-0.5 bg-green-100 text-green-800 rounded-full text-xs font-medium flex items-center gap-1">
                          <Target className="h-3 w-3" />
                          Target Achieved
                        </span>
                      )}
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                      <div className="flex items-center gap-2 text-sm">
                        <Calendar className="h-4 w-4 text-gray-400" />
                        <span className="text-gray-600">
                          {new Date(run.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <div className="text-sm">
                        <span className="text-gray-500">Iterations: </span>
                        <span className="font-medium">{run.total_iterations}</span>
                      </div>
                      <div className="text-sm">
                        <span className="text-gray-500">Initial: </span>
                        <span className="font-medium">{run.initial_score.toFixed(1)}</span>
                      </div>
                      <div className="text-sm">
                        <span className="text-gray-500">Final: </span>
                        <span className="font-semibold text-green-600">
                          {run.final_score.toFixed(1)}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-1 text-sm">
                        <TrendingUp className="h-4 w-4 text-blue-600" />
                        <span className="text-gray-600">Improvement: </span>
                        <span className="font-semibold text-blue-600">
                          +{run.improvement_percentage.toFixed(2)}%
                        </span>
                        <span className="text-gray-500 ml-1">
                          ({run.total_improvement.toFixed(1)} points)
                        </span>
                      </div>
                      <div className="text-xs text-gray-500">
                        {run.feedback_ids?.length || 0} feedback entries used
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => setSelectedRunId(run.mitigation_run_id)}
                    className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors flex items-center gap-2"
                  >
                    <Eye className="h-4 w-4" />
                    See Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {selectedRunId && (
        <MitigationDetailModal
          mitigationRunId={selectedRunId}
          onClose={() => {
            setSelectedRunId(null)
            refetch()
          }}
        />
      )}
    </>
  )
}
