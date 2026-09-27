'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api-client'
import { DashboardResponse } from '@/lib/types/metrics'
import { KPICards } from '@/components/dashboard/KPICards'
import { BiasHeatmap } from '@/components/dashboard/BiasHeatmap'
import { TopFindings } from '@/components/dashboard/TopFindings'
import DataUpload from '@/components/dashboard/DataUpload'
import { Loader2 } from 'lucide-react'

export default function DashboardPage() {
  const [data, setData] = useState<DashboardResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setIsLoading(true)
        const response = await apiClient.get('/dashboard')
        setData(response.data)
        setError(null)
      } catch (err: any) {
        console.error('Error fetching dashboard:', err)
        setError(err)
        // Set empty data on error
        setData({
          kpi_metrics: {
            approval_parity: 0,
            interest_gap: 0,
            collateral_gap: 0,
            fairness_score: 0,
            severity: 'low' as any
          },
          top_findings: [],
          heatmap_data: {},
          test_run_id: '',
          last_updated: new Date().toISOString()
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchDashboard()
    
    // Refresh when component becomes visible (user navigates back to dashboard)
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        fetchDashboard()
      }
    }
    
    // Refresh every 5 seconds to get latest data
    const interval = setInterval(() => {
      fetchDashboard()
    }, 5000)
    
    document.addEventListener('visibilitychange', handleVisibilityChange)
    
    return () => {
      clearInterval(interval)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, []) // Empty dependency array - only run on mount

  // Show loading state
  if (isLoading) {
    return (
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">
            Real-time bias metrics and fairness validation results
          </p>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <div className="flex items-center mb-4">
              <Loader2 className="h-5 w-5 animate-spin text-blue-600 mr-2" />
              <h2 className="text-lg font-semibold text-blue-800">Loading dashboard data...</h2>
            </div>
          <p className="text-blue-600 mb-4">
            Fetching data from backend...
          </p>
          <div className="bg-white p-4 rounded border border-blue-200 mt-4">
            <p className="text-sm font-semibold text-blue-900 mb-2">Quick Links:</p>
            <p className="text-xs text-blue-700 mb-2">
              API Documentation: <a href="http://localhost:8000/docs" className="underline font-mono" target="_blank" rel="noopener noreferrer">http://localhost:8000/docs</a>
            </p>
            <p className="text-xs text-blue-700">
              Backend Health: <a href="http://localhost:8000/health" className="underline font-mono" target="_blank" rel="noopener noreferrer">http://localhost:8000/health</a>
            </p>
          </div>
        </div>
      </div>
    )
  }

  // Show dashboard with data (or empty state if no data)
  if (!data) {
    return (
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">
            Real-time bias metrics and fairness validation results
          </p>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Dashboard</h2>
          <p className="text-red-600">
            {error instanceof Error ? error.message : 'Failed to load dashboard data. Please refresh the page.'}
          </p>
        </div>
      </div>
    )
  }

  // Show dashboard with data (backend always returns kpi_metrics structure)
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">
          Real-time bias metrics and fairness validation results
        </p>
      </div>

      {/* Data Upload Section - Always visible at top */}
      <DataUpload />

      {/* Metrics Section - Always show (backend always returns kpi_metrics structure) */}
      {data.kpi_metrics && <KPICards metrics={data.kpi_metrics} />}

      {/* Heatmap and Findings - Always show, components handle empty states */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <div>
          <BiasHeatmap heatmapData={data.heatmap_data || {}} />
        </div>
        <div>
          <TopFindings findings={data.top_findings || []} />
        </div>
      </div>
    </div>
  )
}

