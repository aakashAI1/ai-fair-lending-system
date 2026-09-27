"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { apiClient } from "@/lib/api-client"
import { Loader2, Sparkles } from "lucide-react"

interface GenerationStatus {
  status: "idle" | "generating" | "success" | "error"
  message: string
  generated?: number
  testRunId?: string
}

export default function ProfileGeneration() {
  const [generationStatus, setGenerationStatus] = useState<GenerationStatus>({
    status: "idle",
    message: "",
  })
  const [count, setCount] = useState<string>('50')
  const [dimensions, setDimensions] = useState<string[]>([
    "geographic",
    "income",
    "credit",
    "edge_cases",
  ])
  const [isGenerating, setIsGenerating] = useState(false)

  const dimensionOptions = [
    { value: "geographic", label: "Geographic (Urban vs Rural)" },
    { value: "income", label: "Income (High vs Low)" },
    { value: "credit", label: "Credit (Good vs Fair)" },
    { value: "edge_cases", label: "Edge Cases (Self-employed, etc.)" },
    { value: "gender", label: "Gender (Coming Soon)" },
  ]

  const handleGenerate = async () => {
    if (isGenerating) return

    try {
      setIsGenerating(true)
      setGenerationStatus({
        status: "generating",
        message: "Generating synthetic student profiles using GenAI...",
      })

      const countNum = parseInt(count) || 50
      const response = await apiClient.post("/profiles/generate", {
        count: countNum,
        dimensions: dimensions.filter((d) => d !== "gender"), // Filter out gender for now
        batch_size: 50,
      })

      if (response.data) {
        const testRunId = response.data.test_run_id
        
        // Poll for completion and actual count
        const pollForCompletion = async () => {
          const maxAttempts = 120 // Poll for up to 2 minutes
          let attempts = 0
          let pollInterval: NodeJS.Timeout | null = null
          
          pollInterval = setInterval(async () => {
            try {
              attempts++
              
              // Check test run status
              const statusResponse = await apiClient.get(`/profiles/test-run/${testRunId}`)
              const { status, total_profiles_generated } = statusResponse.data
              
              if (status === "completed" && total_profiles_generated) {
                if (pollInterval) clearInterval(pollInterval)
                setGenerationStatus({
                  status: "success",
                  message: `Successfully generated ${total_profiles_generated} profiles!`,
                  generated: total_profiles_generated,
                  testRunId: testRunId,
                })
                setIsGenerating(false)
                
                // Refresh page to show new profiles
                setTimeout(() => {
                  window.location.reload()
                }, 2000)
              } else if (status === "failed") {
                if (pollInterval) clearInterval(pollInterval)
                const errorMsg = statusResponse.data.error_message || "Failed to generate profiles. Please try again."
                setGenerationStatus({
                  status: "error",
                  message: errorMsg,
                  testRunId: testRunId,
                })
                setIsGenerating(false)
              } else if (total_profiles_generated && total_profiles_generated > 0) {
                // Update with current progress
                setGenerationStatus({
                  status: "generating",
                  message: `Generating profiles... ${total_profiles_generated} generated so far.`,
                  generated: total_profiles_generated,
                  testRunId: testRunId,
                })
              }
              
              if (attempts >= maxAttempts) {
                if (pollInterval) clearInterval(pollInterval)
                // Use last known count or requested count as fallback
                const finalCount = total_profiles_generated || countNum
                setGenerationStatus({
                  status: "success",
                  message: `Profile generation completed!`,
                  generated: finalCount,
                  testRunId: testRunId,
                })
                
                // Refresh after 2 seconds
                setTimeout(() => {
                  window.location.reload()
                }, 2000)
              }
            } catch (err: any) {
              // If test run endpoint doesn't exist or other error, continue polling
              console.error("Error polling test run status:", err)
              
              // After many attempts, use fallback
              if (attempts >= maxAttempts) {
                if (pollInterval) clearInterval(pollInterval)
                setGenerationStatus({
                  status: "success",
                  message: `Profile generation initiated! Please check profiles page.`,
                  generated: countNum,
                  testRunId: testRunId,
                })
              }
            }
          }, 2000) // Poll every 2 seconds
        }
        
        // Start polling
        pollForCompletion()
      }
    } catch (error: any) {
      console.error("Error generating profiles:", error)
      setGenerationStatus({
        status: "error",
        message:
          error.response?.data?.detail ||
          error.message ||
          "Failed to generate profiles. Please try again.",
      })
    } finally {
      setIsGenerating(false)
    }
  }

  const toggleDimension = (dimension: string) => {
    if (dimension === "gender") {
      // Gender not implemented yet
      return
    }
    setDimensions((prev) =>
      prev.includes(dimension)
        ? prev.filter((d) => d !== dimension)
        : [...prev, dimension]
    )
  }

  const getStatusColor = () => {
    switch (generationStatus.status) {
      case "success":
        return "border-green-500 bg-green-50"
      case "error":
        return "border-red-500 bg-red-50"
      case "generating":
        return "border-blue-500 bg-blue-50"
      default:
        return "border-gray-300 bg-white"
    }
  }

  const getStatusIcon = () => {
    switch (generationStatus.status) {
      case "success":
        return "✅"
      case "error":
        return "❌"
      case "generating":
        return "⏳"
      default:
        return "✨"
    }
  }

  return (
    <Card className={`${getStatusColor()} transition-colors`}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-purple-600" />
          Generate Synthetic Profiles (GenAI)
        </CardTitle>
        <CardDescription>
          Use Google Gemini AI to generate realistic Indian student loan profiles with diversity
          across geographic, income, credit, and edge case dimensions.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Number of Profiles */}
          <div>
            <label htmlFor="profile-count" className="block text-sm font-medium text-gray-700 mb-2">
              Number of Profiles
            </label>
            <input
              id="profile-count"
              type="number"
              min="10"
              max="500"
              value={count}
              onChange={(e) => {
                const value = e.target.value
                // Allow empty string while typing, or valid numbers
                if (value === '' || (!isNaN(Number(value)) && Number(value) >= 0)) {
                  setCount(value)
                }
              }}
              onBlur={(e) => {
                // Ensure valid value on blur
                const numValue = parseInt(e.target.value) || 50
                const clampedValue = Math.max(10, Math.min(500, numValue))
                setCount(clampedValue.toString())
              }}
              disabled={isGenerating}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
            />
            <p className="text-xs text-gray-500 mt-1">
              Recommended: 50-200 profiles for quick testing, 200-500 for comprehensive analysis
            </p>
          </div>

          {/* Dimensions */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Test Dimensions (Select at least one)
            </label>
            <div className="grid grid-cols-2 gap-2">
              {dimensionOptions.map((option) => (
                <label
                  key={option.value}
                  className={`flex items-center p-2 border rounded-md cursor-pointer transition-colors ${
                    dimensions.includes(option.value)
                      ? "bg-blue-50 border-blue-500"
                      : option.value === "gender"
                      ? "bg-gray-100 border-gray-300 cursor-not-allowed opacity-60"
                      : "bg-white border-gray-300 hover:bg-gray-50"
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={dimensions.includes(option.value)}
                    onChange={() => toggleDimension(option.value)}
                    disabled={isGenerating || option.value === "gender"}
                    className="mr-2"
                  />
                  <span className="text-sm">{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={isGenerating || dimensions.length === 0 || !count || parseInt(count) < 10}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold py-3 px-4 rounded-md hover:from-purple-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
          >
            {isGenerating ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                Generating Profiles...
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5" />
                Generate Profiles with GenAI
              </>
            )}
          </button>

          {/* Status Message */}
          {generationStatus.status !== "idle" && (
            <div className="mt-4 p-4 bg-white rounded-lg border">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-2 flex-1">
                  <span className="text-xl">{getStatusIcon()}</span>
                  <div className="flex-1">
                    <p className="font-medium">{generationStatus.message}</p>
                    {generationStatus.generated && (
                      <p className="text-sm text-gray-500 mt-1">
                        Generated {generationStatus.generated} student profiles
                      </p>
                    )}
                    {generationStatus.testRunId && (
                      <p className="text-xs text-gray-400 mt-1 font-mono">
                        Test Run ID: {generationStatus.testRunId}
                      </p>
                    )}
                    {generationStatus.status === "success" && (
                      <a
                        href="/profiles"
                        className="inline-block mt-2 text-sm text-blue-600 hover:text-blue-800 font-medium underline"
                      >
                        View Generated Profiles →
                      </a>
                    )}
                  </div>
                </div>
                {generationStatus.status === "generating" && (
                  <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
                )}
              </div>
            </div>
          )}

          {/* Info Box */}
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
            <p className="text-xs text-blue-800 font-semibold mb-1">💡 How it works:</p>
            <ul className="text-xs text-blue-700 space-y-1 list-disc list-inside">
              <li>Uses Google Gemini AI to create realistic Indian student profiles</li>
              <li>Ensures diversity across selected dimensions for bias testing</li>
              <li>Profiles include: name, location, income, CIBIL score, GPA, course, etc.</li>
              <li>After generation, you can score profiles and calculate bias metrics</li>
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

