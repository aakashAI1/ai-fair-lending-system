'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { TopFinding } from '@/lib/types/metrics'
import { getSeverityColor } from '@/lib/utils'
import { AlertTriangle } from 'lucide-react'

interface TopFindingsProps {
  findings: TopFinding[]
}

export function TopFindings({ findings }: TopFindingsProps) {
  // Normalize findings - ensure it's always an array
  const normalizedFindings = Array.isArray(findings) ? findings : []
  
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-gray-600" />
          Top Findings
        </CardTitle>
        <p className="text-sm text-gray-600">
          Critical bias issues requiring attention
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {normalizedFindings.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 mb-2">No findings available</p>
              <p className="text-xs text-gray-400">Calculate bias metrics to identify issues</p>
            </div>
          ) : (
            normalizedFindings.map((finding) => (
              <div
                key={finding.id}
                className={`p-4 rounded-lg border-2 ${getSeverityColor(finding.severity)}`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <AlertTriangle className={`h-5 w-5 ${
                      finding.severity === 'critical' ? 'text-red-600' :
                      finding.severity === 'high' ? 'text-orange-600' :
                      finding.severity === 'medium' ? 'text-yellow-600' :
                      'text-green-600'
                    }`} />
                    <span className="font-semibold capitalize">{finding.severity}</span>
                  </div>
                  <span className="text-sm text-gray-600 capitalize px-2 py-1 bg-gray-100 rounded">
                    {finding.dimension.replace(/_/g, ' ')}
                  </span>
                </div>
                <p className="text-sm text-gray-700 mb-3 font-medium">{finding.description}</p>
                <div className="flex items-center space-x-4 text-xs">
                  <div className="flex-1 bg-blue-50 p-2 rounded">
                    <span className="font-semibold text-blue-900">{finding.group1_name}:</span>
                    <span className="ml-1 text-blue-700">{typeof finding.group1_value === 'number' ? finding.group1_value.toFixed(2) : finding.group1_value}</span>
                  </div>
                  <span className="text-gray-400 font-semibold">vs</span>
                  <div className="flex-1 bg-purple-50 p-2 rounded">
                    <span className="font-semibold text-purple-900">{finding.group2_name}:</span>
                    <span className="ml-1 text-purple-700">{typeof finding.group2_value === 'number' ? finding.group2_value.toFixed(2) : finding.group2_value}</span>
                  </div>
                </div>
                <div className="mt-2 pt-2 border-t border-gray-200">
                  <span className="text-xs text-gray-500">Fairness Score: </span>
                  <span className="text-xs font-semibold text-gray-700">
                    {typeof finding.metric_value === 'number' ? finding.metric_value.toFixed(1) : 'N/A'}/100
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  )
}







