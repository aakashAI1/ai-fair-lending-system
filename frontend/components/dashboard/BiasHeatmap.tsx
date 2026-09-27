'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { getSeverityColor } from '@/lib/utils'
import { AlertTriangle } from 'lucide-react'

interface BiasHeatmapProps {
  heatmapData: Record<string, Record<string, number>>
}

const severityOrder = ['critical', 'high', 'medium', 'low']
const severityLabels = {
  'critical': 'Critical',
  'high': 'High',
  'medium': 'Medium',
  'low': 'Low'
}

const getIntensityColor = (severity: string, count: number) => {
  if (count === 0) return 'bg-gray-100 text-gray-400'
  
  const colors = {
    'critical': count > 0 ? 'bg-red-600 text-white' : 'bg-red-100 text-red-600',
    'high': count > 0 ? 'bg-orange-500 text-white' : 'bg-orange-100 text-orange-600',
    'medium': count > 0 ? 'bg-yellow-500 text-white' : 'bg-yellow-100 text-yellow-600',
    'low': count > 0 ? 'bg-blue-500 text-white' : 'bg-blue-100 text-blue-600',
  }
  return colors[severity as keyof typeof colors] || 'bg-gray-200 text-gray-600'
}

export function BiasHeatmap({ heatmapData }: BiasHeatmapProps) {
  // Normalize heatmapData - ensure it's always an object
  const normalizedData = heatmapData && typeof heatmapData === 'object' ? heatmapData : {}
  const dimensions = Object.keys(normalizedData)
  
  // Show empty state if no dimensions
  if (dimensions.length === 0) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-gray-400" />
            Bias Heatmap
          </CardTitle>
          <p className="text-sm text-gray-600">
            Severity distribution across test dimensions
          </p>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-gray-500 mb-2">No heatmap data available</p>
            <p className="text-xs text-gray-400">Calculate bias metrics to see severity distribution across dimensions</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="shadow-sm w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-gray-600" />
          Bias Heatmap
        </CardTitle>
        <p className="text-sm text-gray-600">
          Severity distribution across test dimensions
        </p>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b-2 border-gray-200">
                <th className="text-left p-3 font-semibold text-gray-700">Dimension</th>
                {severityOrder.map((severity) => (
                  <th
                    key={severity}
                    className="text-center p-3 font-semibold text-gray-700"
                  >
                    {severityLabels[severity as keyof typeof severityLabels]}
                  </th>
                ))}
                <th className="text-center p-3 font-semibold text-gray-700">Total</th>
              </tr>
            </thead>
            <tbody>
              {dimensions.map((dimension, idx) => {
                const total = severityOrder.reduce((sum, sev) => {
                  return sum + (normalizedData[dimension]?.[sev] || 0)
                }, 0)
                
                return (
                  <tr 
                    key={dimension} 
                    className={`border-b border-gray-100 hover:bg-gray-50 transition-colors ${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}`}
                  >
                    <td className="p-3 font-medium text-gray-900 capitalize">
                      {dimension.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </td>
                    {severityOrder.map((severity) => {
                      const count = normalizedData[dimension]?.[severity] || 0
                      return (
                        <td key={severity} className="p-3 text-center">
                          <span
                            className={`inline-flex items-center justify-center min-w-[3rem] px-3 py-1.5 rounded-lg text-sm font-semibold ${getIntensityColor(severity, count)}`}
                          >
                            {count}
                          </span>
                        </td>
                      )
                    })}
                    <td className="p-3 text-center">
                      <span className="inline-flex items-center justify-center min-w-[3rem] px-3 py-1.5 rounded-lg text-sm font-semibold bg-gray-200 text-gray-700">
                        {total}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
        
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500">
            <strong>Legend:</strong> Numbers represent the count of bias findings at each severity level for each dimension.
            Higher numbers in critical/high categories indicate areas requiring immediate attention.
          </p>
        </div>
      </CardContent>
    </Card>
  )
}







