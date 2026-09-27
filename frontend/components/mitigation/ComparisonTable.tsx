'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { MitigationInfographic } from './MitigationInfographic'

interface ComparisonTableProps {
  data: {
    mitigation_run_id: string
    iterations: any[]
    initial_fairness_score: number
    final_fairness_score: number
    total_improvement?: number
    improvement_percentage?: number
    target_achieved: boolean
  }
  testRunId?: string
}

export function ComparisonTable({ data, testRunId }: ComparisonTableProps) {
  const [expandedIteration, setExpandedIteration] = useState<number | null>(null)

  // Calculate improvement percentage (ensure always positive)
  const improvementPercentage = data.improvement_percentage ?? 
    (data.initial_fairness_score > 0 
      ? Math.max(0, ((data.final_fairness_score - data.initial_fairness_score) / data.initial_fairness_score) * 100)
      : 0)

  return (
    <>
      {/* Infographic - Show first */}
      <MitigationInfographic 
        mitigationRunId={data.mitigation_run_id} 
        testRunId={testRunId}
      />
      
      <Card className="mt-6">
      <CardHeader>
        <CardTitle>Mitigation Results - Iterative Improvement</CardTitle>
        <div className="flex items-center justify-between mt-2">
          <p className="text-sm text-gray-600">
            Total Improvement: <span className="font-semibold text-green-600">+{improvementPercentage.toFixed(2)}%</span>
          </p>
          {data.target_achieved ? (
            <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold flex items-center gap-2">
              <span>✓</span> Target Achieved
            </span>
          ) : (
            <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">
              In Progress
            </span>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left p-3 font-medium text-gray-700">Iteration</th>
                <th className="text-left p-3 font-medium text-gray-700">Before</th>
                <th className="text-left p-3 font-medium text-gray-700">After</th>
                <th className="text-left p-3 font-medium text-gray-700">Improvement</th>
                <th className="text-left p-3 font-medium text-gray-700">Status</th>
                <th className="text-left p-3 font-medium text-gray-700">Details</th>
              </tr>
            </thead>
            <tbody>
              {data.iterations.map((iteration, index) => (
                <>
                  <tr key={index} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                    <td className="p-3 text-sm font-medium text-gray-900">
                      #{iteration.iteration_number}
                    </td>
                    <td className="p-3 text-sm text-gray-700">
                      {iteration.before_fairness_score?.toFixed(1) || 'N/A'}
                    </td>
                    <td className="p-3 text-sm font-semibold text-gray-900">
                      {iteration.after_fairness_score.toFixed(1)}
                    </td>
                    <td className="p-3">
                      <span className="text-sm text-green-600 font-semibold">
                        +{Math.max(0, iteration.improvement_percentage || 0).toFixed(2)}%
                      </span>
                    </td>
                    <td className="p-3">
                      {iteration.target_achieved ? (
                        <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">
                          ✓ Target
                        </span>
                      ) : (
                        <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs font-medium">
                          Progress
                        </span>
                      )}
                    </td>
                    <td className="p-3">
                      <button
                        onClick={() => setExpandedIteration(expandedIteration === iteration.iteration_number ? null : iteration.iteration_number)}
                        className="text-blue-600 hover:text-blue-800 text-xs font-medium"
                      >
                        {expandedIteration === iteration.iteration_number ? 'Hide' : 'Show'} Details
                      </button>
                    </td>
                  </tr>
                  {expandedIteration === iteration.iteration_number && (
                    <tr>
                      <td colSpan={6} className="p-4 bg-blue-50 border-b border-gray-200">
                        <div className="space-y-3">
                          <div>
                            <p className="text-xs font-semibold text-gray-700 mb-1">Prompt Version:</p>
                            <p className="text-xs text-gray-600">{iteration.prompt_version}</p>
                          </div>
                          {iteration.prompt_changes && (
                            <div>
                              <p className="text-xs font-semibold text-gray-700 mb-1">Changes Made:</p>
                              <p className="text-xs text-gray-600">{iteration.prompt_changes}</p>
                            </div>
                          )}
                          <div className="grid grid-cols-3 gap-4 pt-2 border-t border-blue-200">
                            <div>
                              <p className="text-xs text-gray-600">Approval Parity</p>
                              <p className="text-sm font-semibold">
                                {iteration.before_approval_parity?.toFixed(2) || 'N/A'} → {iteration.after_approval_parity?.toFixed(2)}
                              </p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-600">Interest Gap</p>
                              <p className="text-sm font-semibold">
                                {iteration.before_interest_gap?.toFixed(2) || 'N/A'}% → {iteration.after_interest_gap?.toFixed(2)}%
                              </p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-600">Collateral Gap</p>
                              <p className="text-sm font-semibold">
                                {iteration.before_collateral_gap?.toFixed(2) || 'N/A'}% → {iteration.after_collateral_gap?.toFixed(2)}%
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
        </div>
        
        <div className="mt-6 p-6 bg-gradient-to-r from-blue-50 to-green-50 rounded-lg border border-blue-200">
          <div className="grid grid-cols-3 gap-6">
            <div>
              <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Initial Score</p>
              <p className="text-3xl font-bold text-gray-900">
                {data.initial_fairness_score.toFixed(1)}
              </p>
              <p className="text-xs text-gray-500 mt-1">Before mitigation</p>
            </div>
            <div>
              <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Final Score</p>
              <p className="text-3xl font-bold text-green-600">
                {data.final_fairness_score.toFixed(1)}
              </p>
              <p className="text-xs text-gray-500 mt-1">After {data.iterations.length} iterations</p>
            </div>
            <div>
              <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Total Improvement</p>
              <p className="text-3xl font-bold text-blue-600">
                +{improvementPercentage.toFixed(1)}%
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {Math.max(0, (data.final_fairness_score - data.initial_fairness_score)).toFixed(1)} points gained
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
    </>
  )
}







