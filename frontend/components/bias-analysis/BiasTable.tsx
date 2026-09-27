'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { BiasMetric, TestDimension, SeverityLevel } from '@/lib/types/metrics'
import { getSeverityColor } from '@/lib/utils'
import { BiasDetailsModal } from './BiasDetailsModal'

interface BiasTableProps {
  metrics: BiasMetric[]
  onMetricSelect: (metricId: number) => void
  selectedMetricId: number | null
}

export function BiasTable({ metrics, onMetricSelect, selectedMetricId }: BiasTableProps) {
  const [filterDimension, setFilterDimension] = useState<TestDimension | 'all'>('all')
  const [filterSeverity, setFilterSeverity] = useState<SeverityLevel | 'all'>('all')
  const [detailedMetric, setDetailedMetric] = useState<BiasMetric | null>(null)

  const filteredMetrics = metrics.filter((metric) => {
    if (filterDimension !== 'all' && metric.dimension !== filterDimension) {
      return false
    }
    if (filterSeverity !== 'all' && metric.severity !== filterSeverity) {
      return false
    }
    return true
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle>Bias Findings</CardTitle>
        <div className="flex space-x-4 mt-4">
          <select
            value={filterDimension}
            onChange={(e) => setFilterDimension(e.target.value as TestDimension | 'all')}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm"
          >
            <option value="all">All Dimensions</option>
            {Object.values(TestDimension).map((dim) => (
              <option key={dim} value={dim}>
                {dim.replace('_', ' ').toUpperCase()}
              </option>
            ))}
          </select>
          <select
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value as SeverityLevel | 'all')}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm"
          >
            <option value="all">All Severities</option>
            {Object.values(SeverityLevel).map((sev) => (
              <option key={sev} value={sev}>
                {sev.toUpperCase()}
              </option>
            ))}
          </select>
        </div>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left p-3 font-medium text-gray-700">ID</th>
                <th className="text-left p-3 font-medium text-gray-700">Dimension</th>
                <th className="text-left p-3 font-medium text-gray-700">Groups</th>
                <th className="text-left p-3 font-medium text-gray-700">Approval Parity</th>
                <th className="text-left p-3 font-medium text-gray-700">Interest Gap</th>
                <th className="text-left p-3 font-medium text-gray-700">Fairness Score</th>
                <th className="text-left p-3 font-medium text-gray-700">Severity</th>
                <th className="text-left p-3 font-medium text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredMetrics.map((metric, index) => (
                <tr
                  key={metric.id}
                  className={`border-b border-gray-100 hover:bg-gray-50 cursor-pointer ${
                    selectedMetricId === metric.id ? 'bg-blue-50' : ''
                  }`}
                  onClick={() => onMetricSelect(metric.id)}
                >
                  <td className="p-3 text-sm text-gray-900 font-medium">{index + 1}</td>
                  <td className="p-3 text-sm text-gray-700 capitalize">
                    {metric.dimension.replace('_', ' ')}
                  </td>
                  <td className="p-3 text-sm text-gray-700">
                    {metric.group1_name} vs {metric.group2_name}
                  </td>
                  <td className="p-3 text-sm text-gray-900">
                    {metric.approval_parity.toFixed(2)}
                  </td>
                  <td className="p-3 text-sm text-gray-900">
                    {metric.interest_rate_disparity.toFixed(2)}%
                  </td>
                  <td className="p-3 text-sm text-gray-900">
                    {metric.overall_fairness_score.toFixed(1)}
                  </td>
                  <td className="p-3">
                    <span
                      className={`inline-block px-2 py-1 rounded text-xs font-medium capitalize ${getSeverityColor(metric.severity)}`}
                    >
                      {metric.severity}
                    </span>
                  </td>
                  <td className="p-3">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        // Select the metric to show ProfileComparison
                        onMetricSelect(metric.id)
                        // Also open the detailed modal
                        const selected = filteredMetrics.find(m => m.id === metric.id)
                        if (selected) {
                          setDetailedMetric(selected)
                        }
                      }}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredMetrics.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No metrics found matching the filters
            </div>
          )}
        </div>
      </CardContent>

      {/* Detailed Modal */}
      {detailedMetric && (
        <BiasDetailsModal
          metric={detailedMetric}
          onClose={() => setDetailedMetric(null)}
        />
      )}
    </Card>
  )
}







