'use client'

import { useState, useEffect } from 'react'
import { MitigationForm } from '@/components/mitigation/MitigationForm'
import { ComparisonTable } from '@/components/mitigation/ComparisonTable'
import { MitigationHistory } from '@/components/mitigation/MitigationHistory'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import { Loader2, Shield } from 'lucide-react'

interface UserInfo {
  role: string
}

export default function MitigationPage() {
  const [mitigationRunId, setMitigationRunId] = useState<string | null>(null)
  const [mitigationData, setMitigationData] = useState<any>(null)
  const [userRole, setUserRole] = useState<string | null>(null)
  const queryClient = useQueryClient()

  useEffect(() => {
    // Get user role from localStorage
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        const user: UserInfo = JSON.parse(userStr)
        setUserRole(user.role?.toLowerCase() || null)
      } catch (e) {
        console.error('Error parsing user data:', e)
      }
    }
  }, [])

  // Get dashboard data for test_run_id
  const { data: dashboardData } = useQuery({
    queryKey: ['dashboard'],
    queryFn: async () => {
      try {
        const response = await apiClient.get('/dashboard')
        return response.data
      } catch {
        return null
      }
    },
  })

  // Only fetch from API if we don't have the data yet (for page refreshes or if data wasn't passed)
  const { data: mitigationHistory, isLoading } = useQuery({
    queryKey: ['mitigation', mitigationRunId],
    queryFn: async () => {
      if (!mitigationRunId) return null
      const response = await apiClient.get(`/mitigation/history/${mitigationRunId}`)
      return response.data
    },
    enabled: !!mitigationRunId && !mitigationData,
  })

  const handleMitigationComplete = (newRunId: string, data?: any) => {
    setMitigationRunId(newRunId)
    // Use the data directly from the response if provided (avoids 401 error)
    if (data) {
      setMitigationData(data)
    }
    // Refresh the mitigation history list (only for admins)
    queryClient.invalidateQueries({ queryKey: ['mitigation-runs'] })
  }

  // Use the data from state if available, otherwise use the fetched data
  const displayData = mitigationData || mitigationHistory

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Bias Mitigation</h1>
        <p className="text-gray-600">
          Iterative improvement of fairness through GenAI-powered prompt refinement
        </p>
      </div>

      <MitigationForm onMitigationComplete={handleMitigationComplete} />

      {mitigationRunId && (
        <div className="mt-8">
          {isLoading ? (
            <div className="flex items-center justify-center h-64">
              <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
              <span className="ml-2 text-gray-600">Loading mitigation results...</span>
            </div>
          ) : (
            displayData && (
              <ComparisonTable 
                data={displayData} 
                testRunId={dashboardData?.test_run_id || null}
              />
            )
          )}
        </div>
      )}

      {/* Persistent Mitigation History - Admin Only */}
      <div className="mt-8">
        {userRole === 'admin' ? (
          <MitigationHistory />
        ) : (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
            <Shield className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Admin Access Required
            </h3>
            <p className="text-gray-600 mb-4">
              Mitigation logs are restricted to administrators only.
            </p>
            <p className="text-sm text-gray-500">
              Only users with admin privileges can view the complete history of mitigation runs.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}







