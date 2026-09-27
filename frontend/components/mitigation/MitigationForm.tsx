'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { apiClient } from '@/lib/api-client'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useQuery } from '@tanstack/react-query'
import { Loader2, AlertCircle, CheckCircle2 } from 'lucide-react'

const mitigationSchema = z.object({
  test_run_id: z.string(),
  feedback_ids: z.array(z.number()),
  max_iterations: z.number().min(1).max(10).default(3),
  target_fairness_score: z.number().min(0).max(100).default(85),
})

type MitigationFormData = z.infer<typeof mitigationSchema>

interface MitigationFormProps {
  onMitigationComplete: (mitigationRunId: string, data?: any) => void
}

export function MitigationForm({ onMitigationComplete }: MitigationFormProps) {
  const [isRunning, setIsRunning] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  // Get test run ID from dashboard
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

  // Get all feedback entries
  const { data: feedbacks, isLoading: loadingFeedbacks } = useQuery({
    queryKey: ['feedbacks'],
    queryFn: async () => {
      const response = await apiClient.get('/feedback/')
      return response.data
    },
  })

  // Get bias metrics to show which feedback relates to which bias
  const { data: metrics } = useQuery({
    queryKey: ['metrics'],
    queryFn: async () => {
      try {
        const response = await apiClient.get('/metrics/')
        return response.data
      } catch {
        return []
      }
    },
  })

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<MitigationFormData>({
    resolver: zodResolver(mitigationSchema),
    defaultValues: {
      max_iterations: 5,  // Realistic: 5-10 iterations for gradual improvement (banking standard)
      target_fairness_score: 85,
      feedback_ids: [],
    },
  })

  // Auto-populate test run ID from dashboard
  useEffect(() => {
    if (dashboardData?.test_run_id && !watch('test_run_id')) {
      setValue('test_run_id', dashboardData.test_run_id)
    }
  }, [dashboardData, setValue, watch])

  const selectedFeedbackIds = watch('feedback_ids')
  const testRunId = watch('test_run_id')

  // Helper to get metric info for a feedback entry
  const getMetricInfo = (feedback: any) => {
    if (!metrics || !feedback.bias_metric_id) return null
    return metrics.find((m: any) => m.id === feedback.bias_metric_id)
  }

  const onSubmit = async (data: MitigationFormData) => {
    setSubmitError(null)
    setSuccessMessage(null)
    
    if (!data.feedback_ids || data.feedback_ids.length === 0) {
      setSubmitError('Please select at least one feedback entry to use for mitigation.')
      return
    }

    try {
      setIsRunning(true)
      // Mitigation can take 30-90 seconds with optimizations, use 3 minutes timeout
      const response = await apiClient.post('/mitigation/run', data, {
        timeout: 180000 // 3 minutes timeout (should be enough with optimizations)
      })
      setSuccessMessage(`Mitigation cycle completed! Run ID: ${response.data.mitigation_run_id}`)
      // Pass the full response data so we don't need to fetch again
      onMitigationComplete(response.data.mitigation_run_id, response.data)
    } catch (error: any) {
      console.error('Error running mitigation:', error)
      
      // Handle timeout specifically
      if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
        setSubmitError('Mitigation is taking longer than expected. This is normal for multiple iterations. Please check the results in a moment.')
        // Still try to get results if the request partially completed
        // The mitigation might have completed on the backend even if the response timed out
      } else {
        const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to run mitigation. Please try again.'
        setSubmitError(errorMessage)
      }
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Run Mitigation Cycle</CardTitle>
        <p className="text-sm text-gray-600">
          Iteratively improve fairness using GenAI-powered prompt refinement based on your feedback
        </p>
        <p className="text-xs text-gray-500 mt-1">
          The system makes conservative, incremental improvements (5-15% per iteration) to align with banking industry standards
        </p>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Test Run ID <span className="text-red-500">*</span>
            </label>
            <input
              {...register('test_run_id')}
              type="text"
              className={`w-full px-3 py-2 border rounded-md ${
                errors.test_run_id ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder={dashboardData?.test_run_id || "TEST_xxxxxxxx"}
            />
            {dashboardData?.test_run_id && (
              <p className="mt-1 text-xs text-blue-600">
                Auto-filled from dashboard: {dashboardData.test_run_id}
              </p>
            )}
            {errors.test_run_id && (
              <p className="mt-1 text-sm text-red-600">{errors.test_run_id.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Feedback Entries <span className="text-red-500">*</span>
              <span className="ml-2 text-xs font-normal text-gray-500">
                ({selectedFeedbackIds?.length || 0} selected)
              </span>
            </label>
            {loadingFeedbacks ? (
              <div className="flex items-center justify-center p-4 border border-gray-200 rounded-md">
                <Loader2 className="h-4 w-4 animate-spin text-blue-600 mr-2" />
                <span className="text-sm text-gray-600">Loading feedback...</span>
              </div>
            ) : !feedbacks || feedbacks.length === 0 ? (
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                <p className="text-sm text-yellow-800">
                  No feedback available. Please provide feedback on bias findings first.
                </p>
              </div>
            ) : (
              <div className="space-y-2 max-h-64 overflow-y-auto border border-gray-200 rounded-md p-3 bg-gray-50">
                {feedbacks.map((feedback: any) => {
                  const metric = getMetricInfo(feedback)
                  return (
                    <label 
                      key={feedback.id} 
                      className={`flex items-start space-x-3 p-2 rounded border cursor-pointer transition-colors ${
                        selectedFeedbackIds?.includes(feedback.id)
                          ? 'bg-blue-50 border-blue-300'
                          : 'bg-white border-gray-200 hover:bg-gray-50'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={selectedFeedbackIds?.includes(feedback.id) || false}
                        onChange={(e) => {
                          const current = selectedFeedbackIds || []
                          if (e.target.checked) {
                            setValue('feedback_ids', [...current, feedback.id])
                          } else {
                            setValue('feedback_ids', current.filter((id: number) => id !== feedback.id))
                          }
                        }}
                        className="mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-semibold text-gray-900">
                            Feedback #{feedback.id}
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
                          <span className="px-2 py-0.5 rounded text-xs bg-gray-200 text-gray-700">
                            Severity: {feedback.severity_rating}/5
                          </span>
                        </div>
                        {metric && (
                          <p className="text-xs text-gray-600 mb-1">
                            Bias: {metric.group1_name} vs {metric.group2_name} ({metric.dimension})
                          </p>
                        )}
                        {feedback.root_cause_analysis && (
                          <p className="text-xs text-gray-500 line-clamp-2">
                            {feedback.root_cause_analysis.substring(0, 100)}...
                          </p>
                        )}
                      </div>
                    </label>
                  )
                })}
              </div>
            )}
            {errors.feedback_ids && (
              <p className="mt-1 text-sm text-red-600">{errors.feedback_ids.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Iterations
              </label>
              <input
                {...register('max_iterations', { valueAsNumber: true })}
                type="number"
                min="1"
                max="10"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
              <p className="mt-1 text-xs text-gray-500">
                Recommended: 5-10 iterations for realistic gradual improvement (banking standard: 2-5% per iteration)
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Fairness Score
              </label>
              <input
                {...register('target_fairness_score', { valueAsNumber: true })}
                type="number"
                min="0"
                max="100"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
              <p className="mt-1 text-xs text-gray-500">
                Goal: 85/100 (industry standard)
              </p>
            </div>
          </div>

          {submitError && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-md flex items-start gap-2">
              <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-red-800">Error</p>
                <p className="text-sm text-red-700">{submitError}</p>
              </div>
            </div>
          )}

          {successMessage && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-md flex items-start gap-2">
              <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-green-800">Success</p>
                <p className="text-sm text-green-700">{successMessage}</p>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={isRunning || !testRunId || !selectedFeedbackIds || selectedFeedbackIds.length === 0}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isRunning ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Running Mitigation Cycle...
              </>
            ) : (
              'Run Mitigation Cycle'
            )}
          </button>

          {isRunning && (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
              <p className="text-sm text-blue-800 font-medium mb-2">Mitigation in Progress</p>
              <p className="text-xs text-blue-700 mb-2">
                This process may take 1-3 minutes as it iteratively improves fairness scores through multiple cycles.
                Each iteration makes conservative improvements (5-15%) to align with banking standards.
              </p>
              <p className="text-xs text-blue-600 italic">
                Note: If GenAI quota is exceeded, the system will automatically use deterministic scoring with refined logic based on your feedback.
              </p>
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  )
}







