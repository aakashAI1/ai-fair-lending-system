'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { apiClient } from '@/lib/api-client'
import { BiasMetric } from '@/lib/types/metrics'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { getSeverityColor } from '@/lib/utils'
import { Sparkles, Loader2, CheckCircle } from 'lucide-react'

const feedbackSchema = z.object({
  bias_metric_id: z.number(),
  is_discriminatory: z.enum(['yes', 'no', 'partially']),
  root_cause_analysis: z.string().optional(),
  severity_rating: z.number().min(1).max(5),
  suggested_mitigation: z.string().optional(),
  annotator_name: z.string().optional(),
  annotator_role: z.string().optional(),
})

type FeedbackFormData = z.infer<typeof feedbackSchema>

interface FeedbackFormProps {
  metrics: BiasMetric[]
}

export function FeedbackForm({ metrics }: FeedbackFormProps) {
  const [selectedMetricId, setSelectedMetricId] = useState<number | null>(null)
  const [submitted, setSubmitted] = useState(false)
  const [loadingSuggestions, setLoadingSuggestions] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState<any>(null)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch,
  } = useForm<FeedbackFormData>({
    resolver: zodResolver(feedbackSchema),
    defaultValues: {
      severity_rating: 3,
      is_discriminatory: 'yes', // Default value to prevent validation error
      bias_metric_id: undefined,
    },
  })

  // Update bias_metric_id when a metric is selected
  useEffect(() => {
    if (selectedMetricId) {
      setValue('bias_metric_id', selectedMetricId, { shouldValidate: true })
    }
  }, [selectedMetricId, setValue])

  const onSubmit = async (data: FeedbackFormData) => {
    setSubmitError(null)
    try {
      await apiClient.post('/feedback/', data)
      setSubmitted(true)
      setSelectedMetricId(null)
      setAiSuggestions(null)
      reset({
        severity_rating: 3,
        is_discriminatory: 'yes',
      })
      setTimeout(() => setSubmitted(false), 3000)
    } catch (error: any) {
      console.error('Error submitting feedback:', error)
      const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to submit feedback. Please try again.'
      setSubmitError(errorMessage)
      // Scroll to error message
      setTimeout(() => {
        const errorElement = document.querySelector('[data-feedback-error]')
        errorElement?.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 100)
    }
  }

  const selectedMetric = metrics.find((m) => m.id === selectedMetricId)

  const generateAISuggestions = async () => {
    if (!selectedMetricId) return
    
    // Toggle: if suggestions are already shown for this metric, hide them
    if (aiSuggestions && !loadingSuggestions) {
      setAiSuggestions(null)
      return
    }
    
    setLoadingSuggestions(true)
    setAiSuggestions(null)
    
    try {
      // Get tailored suggestions for this specific bias metric
      const response = await apiClient.post(`/feedback/suggest-mitigation/${selectedMetricId}`)
      if (response.data && response.data.suggestions) {
        setAiSuggestions(response.data)
      } else {
        // Fallback suggestions if response structure is unexpected
        setAiSuggestions({
          suggestions: [
            {
              title: "Remove Geographic Bias",
              description: "Eliminate geographic location from scoring criteria. Focus on merit-based factors only.",
              expected_impact: "Improve approval parity",
              implementation_complexity: "medium"
            },
            {
              title: "Standardize Interest Rates",
              description: "Set baseline interest rates based only on credit score and loan amount.",
              expected_impact: "Reduce interest rate disparity",
              implementation_complexity: "low"
            }
          ]
        })
      }
    } catch (error: any) {
      console.error('Error generating AI suggestions:', error)
      // Show user-friendly error message
      const errorMessage = error?.response?.data?.detail || error?.message || "Unable to generate suggestions"
      setAiSuggestions({
        suggestions: [
          {
            title: "Error Generating Suggestions",
            description: `Could not generate AI suggestions: ${errorMessage}. Please try again or provide manual suggestions.`,
            expected_impact: "N/A",
            implementation_complexity: "N/A"
          }
        ],
        error: true
      })
    } finally {
      setLoadingSuggestions(false)
    }
  }
  
  // Clear suggestions when a different metric is selected
  useEffect(() => {
    setAiSuggestions(null)
  }, [selectedMetricId])

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Select Bias Finding</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {metrics.map((metric) => (
              <button
                key={metric.id}
                onClick={() => setSelectedMetricId(metric.id)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-colors ${
                  selectedMetricId === metric.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-900">
                    {metric.group1_name} vs {metric.group2_name}
                  </span>
                  <span
                    className={`px-2 py-1 rounded text-xs font-medium capitalize ${getSeverityColor(metric.severity)}`}
                  >
                    {metric.severity}
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  {metric.dimension.replace('_', ' ')} - Approval Parity: {metric.approval_parity.toFixed(2)}
                </p>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Provide Feedback</CardTitle>
        </CardHeader>
        <CardContent>
          {selectedMetric ? (
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <input 
                type="hidden" 
                {...register('bias_metric_id', { required: true, valueAsNumber: true })} 
                value={selectedMetric.id || ''} 
              />

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Is this discriminatory? <span className="text-red-500">*</span>
                </label>
                <select
                  {...register('is_discriminatory')}
                  className={`w-full px-3 py-2 border rounded-md ${
                    errors.is_discriminatory ? 'border-red-500' : 'border-gray-300'
                  }`}
                >
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                  <option value="partially">Partially</option>
                </select>
                {errors.is_discriminatory && (
                  <p className="mt-1 text-sm text-red-600">{errors.is_discriminatory.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Root Cause Analysis
                </label>
                <textarea
                  {...register('root_cause_analysis')}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Explain why this bias occurred..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Severity Rating (1-5)
                </label>
                <input
                  type="range"
                  {...register('severity_rating', { valueAsNumber: true })}
                  min="1"
                  max="5"
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>1 - Low</span>
                  <span>5 - Critical</span>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Suggested Mitigation
                  </label>
                  <button
                    type="button"
                    onClick={generateAISuggestions}
                    disabled={loadingSuggestions || !selectedMetric}
                    className={`flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-md border transition-colors ${
                      aiSuggestions && !loadingSuggestions
                        ? 'text-gray-600 bg-gray-50 border-gray-300 hover:bg-gray-100'
                        : 'text-blue-600 bg-blue-50 border-blue-200 hover:bg-blue-100'
                    } disabled:opacity-50 disabled:cursor-not-allowed`}
                  >
                    {loadingSuggestions ? (
                      <>
                        <Loader2 className="h-3 w-3 animate-spin" />
                        Generating...
                      </>
                    ) : aiSuggestions ? (
                      <>
                        <Sparkles className="h-3 w-3" />
                        Hide Suggestions
                      </>
                    ) : (
                      <>
                        <Sparkles className="h-3 w-3" />
                        Get AI Suggestions
                      </>
                    )}
                  </button>
                </div>
                
                {/* AI Suggestions Display */}
                {aiSuggestions && aiSuggestions.suggestions && (
                  <div className={`mb-3 space-y-2 p-3 rounded-md border ${aiSuggestions.error ? 'bg-red-50 border-red-200' : 'bg-blue-50 border-blue-200'}`}>
                    <p className={`text-xs font-semibold mb-2 flex items-center gap-1 ${aiSuggestions.error ? 'text-red-900' : 'text-blue-900'}`}>
                      <Sparkles className="h-3 w-3" />
                      {aiSuggestions.error ? 'Error:' : 'AI Suggestions:'}
                    </p>
                    {aiSuggestions.suggestions.map((suggestion: any, idx: number) => (
                      <div
                        key={idx}
                        className={`p-2 rounded text-xs border ${aiSuggestions.error 
                          ? 'bg-red-100 border-red-200' 
                          : 'bg-white border-blue-100 cursor-pointer hover:bg-blue-50 transition-colors'}`}
                        onClick={() => {
                          if (!aiSuggestions.error) {
                            setValue('suggested_mitigation', suggestion.description)
                          }
                        }}
                      >
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex-1">
                            <p className={`font-semibold mb-1 ${aiSuggestions.error ? 'text-red-900' : 'text-gray-900'}`}>
                              {suggestion.title}
                            </p>
                            <p className={`text-xs leading-relaxed ${aiSuggestions.error ? 'text-red-700' : 'text-gray-600'}`}>
                              {suggestion.description}
                            </p>
                            {!aiSuggestions.error && suggestion.expected_impact && (
                              <div className="flex gap-3 mt-1.5 text-xs text-gray-500">
                                <span>Impact: {suggestion.expected_impact}</span>
                                {suggestion.implementation_complexity && (
                                  <span>Complexity: {suggestion.implementation_complexity}</span>
                                )}
                              </div>
                            )}
                          </div>
                          {!aiSuggestions.error && (
                            <CheckCircle className="h-4 w-4 text-blue-600 flex-shrink-0 mt-0.5" />
                          )}
                        </div>
                      </div>
                    ))}
                    {!aiSuggestions.error && (
                      <p className="text-xs text-blue-700 mt-2 italic">Click on any suggestion to use it</p>
                    )}
                  </div>
                )}
                
                <textarea
                  {...register('suggested_mitigation')}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Suggest how to fix this bias... (Click 'Get AI Suggestions' for recommendations)"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Annotator Name
                  </label>
                  <input
                    {...register('annotator_name')}
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Role
                  </label>
                  <select
                    {...register('annotator_role')}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md bg-white"
                  >
                    <option value="">Select a role</option>
                    <option value="loan_officer">Loan Officer</option>
                    <option value="risk_analyst">Risk Analyst</option>
                    <option value="compliance_officer">Compliance Officer</option>
                    <option value="data_scientist">Data Scientist</option>
                  </select>
                </div>
              </div>

              {/* Display form validation errors */}
              {Object.keys(errors).length > 0 && (
                <div className="bg-red-50 border border-red-200 rounded-md p-3 text-red-800 text-sm" data-feedback-error>
                  <p className="font-semibold mb-1">Please fix the following errors:</p>
                  <ul className="list-disc list-inside space-y-1">
                    {errors.is_discriminatory && (
                      <li>Discriminatory assessment is required</li>
                    )}
                    {errors.severity_rating && (
                      <li>Severity rating is required</li>
                    )}
                    {errors.bias_metric_id && (
                      <li>Bias metric is required</li>
                    )}
                  </ul>
                </div>
              )}

              {/* Display submission error */}
              {submitError && (
                <div className="bg-red-50 border border-red-200 rounded-md p-3 text-red-800 text-sm" data-feedback-error>
                  <p className="font-semibold">Error submitting feedback:</p>
                  <p>{submitError}</p>
                </div>
              )}

              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={!selectedMetric}
              >
                Submit Feedback
              </button>

              {submitted && (
                <div className="bg-green-50 border border-green-200 rounded-md p-3 text-green-800 text-sm">
                  Feedback submitted successfully!
                </div>
              )}
            </form>
          ) : (
            <div className="text-center py-8 text-gray-500">
              Select a bias finding to provide feedback
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}







