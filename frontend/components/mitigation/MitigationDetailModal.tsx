'use client'

import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import { X, Loader2, User, Calendar, AlertCircle } from 'lucide-react'
import { MitigationInfographic } from './MitigationInfographic'

interface MitigationDetailModalProps {
  mitigationRunId: string
  onClose: () => void
}

export function MitigationDetailModal({ mitigationRunId, onClose }: MitigationDetailModalProps) {
  const { data: detail, isLoading } = useQuery({
    queryKey: ['mitigation-detail', mitigationRunId],
    queryFn: async () => {
      const response = await apiClient.get(`/mitigation/detail/${mitigationRunId}`)
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
          <div className="flex items-center justify-center h-32">
            <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
            <span className="ml-2 text-gray-600">Loading details...</span>
          </div>
        </div>
      </div>
    )
  }

  if (!detail) {
    return null
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Mitigation Details</h2>
            <p className="text-sm text-gray-600 mt-1">{mitigationRunId}</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Infographic */}
          <MitigationInfographic 
            mitigationRunId={mitigationRunId}
          />

          {/* Summary */}
          <div className="grid grid-cols-4 gap-4 p-4 bg-gradient-to-r from-blue-50 to-green-50 rounded-lg border border-blue-200">
            <div>
              <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Initial Score</p>
              <p className="text-2xl font-bold text-gray-900">
                {detail.initial_fairness_score?.toFixed(1) || '0.0'}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Final Score</p>
              <p className="text-2xl font-bold text-green-600">
                {detail.final_fairness_score?.toFixed(1) || '0.0'}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Improvement</p>
              <p className="text-2xl font-bold text-blue-600">
                +{detail.improvement_percentage?.toFixed(2) || '0.00'}%
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {detail.total_improvement?.toFixed(1) || '0.0'} points
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Iterations</p>
              <p className="text-2xl font-bold text-gray-900">{detail.total_iterations || 0}</p>
            </div>
          </div>

          {/* Feedback Section */}
          {detail.feedbacks && detail.feedbacks.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <User className="h-5 w-5" />
                Employee Feedback ({detail.feedbacks.length} entries)
              </h3>
              <div className="space-y-4">
                {detail.feedbacks.map((feedback: any) => (
                  <div
                    key={feedback.id}
                    className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-semibold text-gray-900">
                            {feedback.annotator_name || 'Unknown Employee'}
                          </span>
                          <span className="px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-xs">
                            {feedback.annotator_role || 'Unknown Role'}
                          </span>
                          <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                            feedback.is_discriminatory === 'yes'
                              ? 'bg-red-100 text-red-800'
                              : feedback.is_discriminatory === 'partially'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-green-100 text-green-800'
                          }`}>
                            {feedback.is_discriminatory}
                          </span>
                          <span className="px-2 py-0.5 bg-gray-200 text-gray-700 rounded text-xs">
                            Severity: {feedback.severity_rating}/5
                          </span>
                        </div>
                        {feedback.created_at && (
                          <div className="flex items-center gap-1 text-xs text-gray-500">
                            <Calendar className="h-3 w-3" />
                            {new Date(feedback.created_at).toLocaleString()}
                          </div>
                        )}
                      </div>
                    </div>

                    {feedback.root_cause_analysis && (
                      <div className="mb-3">
                        <p className="text-xs font-semibold text-gray-700 mb-1">Root Cause Analysis:</p>
                        <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded border border-gray-200">
                          {feedback.root_cause_analysis}
                        </p>
                      </div>
                    )}

                    {feedback.suggested_mitigation && (
                      <div>
                        <p className="text-xs font-semibold text-gray-700 mb-1">Suggested Mitigation:</p>
                        <p className="text-sm text-gray-700 bg-blue-50 p-3 rounded border border-blue-200">
                          {feedback.suggested_mitigation}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Iterations Section */}
          {detail.iterations && detail.iterations.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Iteration Details</h3>
              <div className="space-y-4">
                {detail.iterations.map((iteration: any, index: number) => (
                  <div
                    key={iteration.id}
                    className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold text-gray-900">
                        Iteration #{iteration.iteration_number}
                      </h4>
                      <div className="flex items-center gap-4 text-sm">
                        <div>
                          <span className="text-gray-500">Before: </span>
                          <span className="font-medium">{iteration.before_fairness_score?.toFixed(1)}</span>
                        </div>
                        <div>
                          <span className="text-gray-500">After: </span>
                          <span className="font-semibold text-green-600">
                            {iteration.after_fairness_score?.toFixed(1)}
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-500">Improvement: </span>
                          <span className="font-semibold text-blue-600">
                            +{iteration.improvement_percentage?.toFixed(2)}%
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3 text-sm">
                      <div>
                        <p className="text-xs text-gray-500 mb-1">Approval Parity</p>
                        <p>
                          <span className="text-gray-600">{iteration.before_approval_parity?.toFixed(3)}</span>
                          {' → '}
                          <span className="font-semibold text-green-600">
                            {iteration.after_approval_parity?.toFixed(3)}
                          </span>
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 mb-1">Interest Gap</p>
                        <p>
                          <span className="text-gray-600">{iteration.before_interest_gap?.toFixed(2)}%</span>
                          {' → '}
                          <span className="font-semibold text-green-600">
                            {iteration.after_interest_gap?.toFixed(2)}%
                          </span>
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 mb-1">Collateral Gap</p>
                        <p>
                          <span className="text-gray-600">{iteration.before_collateral_gap?.toFixed(2)}%</span>
                          {' → '}
                          <span className="font-semibold text-green-600">
                            {iteration.after_collateral_gap?.toFixed(2)}%
                          </span>
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 mb-1">Prompt Version</p>
                        <p className="font-mono text-xs text-gray-700">{iteration.prompt_version}</p>
                      </div>
                    </div>

                    {iteration.prompt_changes && (
                      <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded">
                        <p className="text-xs font-semibold text-yellow-800 mb-1">Changes Made:</p>
                        <p className="text-xs text-yellow-900">{iteration.prompt_changes}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}
