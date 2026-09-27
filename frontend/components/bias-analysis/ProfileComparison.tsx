'use client'

import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Loader2, TrendingUp, TrendingDown, CheckCircle, XCircle, DollarSign, BarChart3, Users, Percent } from 'lucide-react'
import { BiasMetric } from '@/lib/types/metrics'

interface StudentProfile {
  id: number
  profile_id: string
  name: string
  postcode: string
  region: string
  state: string
  family_income: number
  cibil_score: number
  requested_loan_amount: number
  gpa: number
  course: string
  educational_background: string
  college_tier?: string | null
  university_name?: string | null
  co_applicant: string | null
  employment_type: string
  family_structure: string
  test_dimension: string
  created_at: string
  updated_at?: string | null
}

interface ScoringResult {
  id: number
  profile_id: number
  scoring_type: string
  score: number
  approval_decision: string
  interest_rate: number
  collateral_required: boolean
  reasoning: string | null
  created_at: string
}

interface ProfileWithScores {
  profile: StudentProfile
  fair_score: ScoringResult | null
  biased_score: ScoringResult | null
}

interface ProfileComparisonResponse {
  metric: BiasMetric
  group1_profiles: ProfileWithScores[]
  group2_profiles: ProfileWithScores[]
}

interface ProfileComparisonProps {
  metricId: number
}

function ProfileCard({ profileWithScores, groupName }: { profileWithScores: ProfileWithScores; groupName: string }) {
  const { profile, fair_score, biased_score } = profileWithScores
  const scoreDiff = biased_score && fair_score ? biased_score.score - fair_score.score : 0

  return (
    <div className="border rounded-lg p-4 bg-gray-50">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h4 className="font-semibold text-gray-900">{profile.name}</h4>
          <p className="text-sm text-gray-600">{profile.profile_id}</p>
        </div>
        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
          {groupName}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-xs text-gray-500">State</p>
          <p className="text-sm font-medium">{profile.state}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">CIBIL</p>
          <p className="text-sm font-medium">{profile.cibil_score}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Income</p>
          <p className="text-sm font-medium">₹{(profile.family_income / 100000).toFixed(1)}L</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">GPA</p>
          <p className="text-sm font-medium">{profile.gpa.toFixed(1)}</p>
        </div>
      </div>

      {fair_score && biased_score && (
        <div className="space-y-2 pt-3 border-t">
          <div className="grid grid-cols-2 gap-2">
            <div className="bg-green-50 p-2 rounded">
              <p className="text-xs text-gray-600">Fair Score</p>
              <div className="flex items-center gap-1">
                <p className="text-lg font-bold text-green-700">{fair_score.score.toFixed(1)}</p>
                {fair_score.approval_decision === 'approve' ? (
                  <CheckCircle className="h-4 w-4 text-green-600" />
                ) : (
                  <XCircle className="h-4 w-4 text-red-600" />
                )}
              </div>
              <p className="text-xs text-gray-500">
                {fair_score.interest_rate}% | {fair_score.collateral_required ? 'Collateral' : 'No Collateral'}
              </p>
            </div>
            <div className="bg-orange-50 p-2 rounded">
              <p className="text-xs text-gray-600">Biased Score</p>
              <div className="flex items-center gap-1">
                <p className="text-lg font-bold text-orange-700">{biased_score.score.toFixed(1)}</p>
                {biased_score.approval_decision === 'approve' ? (
                  <CheckCircle className="h-4 w-4 text-green-600" />
                ) : (
                  <XCircle className="h-4 w-4 text-red-600" />
                )}
              </div>
              <p className="text-xs text-gray-500">
                {biased_score.interest_rate}% | {biased_score.collateral_required ? 'Collateral' : 'No Collateral'}
              </p>
            </div>
          </div>
          {scoreDiff !== 0 && (
            <div className={`flex items-center gap-1 text-xs ${scoreDiff < 0 ? 'text-red-600' : 'text-green-600'}`}>
              {scoreDiff < 0 ? (
                <TrendingDown className="h-3 w-3" />
              ) : (
                <TrendingUp className="h-3 w-3" />
              )}
              <span>Difference: {scoreDiff > 0 ? '+' : ''}{scoreDiff.toFixed(1)} points</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export function ProfileComparison({ metricId }: ProfileComparisonProps) {
  const { data, isLoading, error } = useQuery<ProfileComparisonResponse>({
    queryKey: ['metric-profile-comparison', metricId],
    queryFn: async () => {
      const response = await apiClient.get(`/metrics/${metricId}/profile-comparison?limit=5`)
      return response.data
    },
    enabled: !!metricId,
  })

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Profile Comparison</CardTitle>
          <p className="text-sm text-gray-600">
            Fair vs. Biased scoring comparison for selected metric
          </p>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
            <span className="ml-2 text-gray-600">Loading profile comparisons...</span>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Profile Comparison</CardTitle>
          <p className="text-sm text-gray-600">
            Fair vs. Biased scoring comparison for selected metric
          </p>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-red-600">
            Error loading profile comparisons. Please try again.
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!data || (data.group1_profiles.length === 0 && data.group2_profiles.length === 0)) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Profile Comparison</CardTitle>
          <p className="text-sm text-gray-600">
            Fair vs. Biased scoring comparison for selected metric
          </p>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-gray-500">
            No profile data available for this comparison.
          </div>
        </CardContent>
      </Card>
    )
  }

  // Calculate aggregate statistics for visualizations
  const group1FairScores = data.group1_profiles
    .map(p => p.fair_score?.score)
    .filter((s): s is number => s !== undefined && s !== null)
  const group1BiasedScores = data.group1_profiles
    .map(p => p.biased_score?.score)
    .filter((s): s is number => s !== undefined && s !== null)
  const group2FairScores = data.group2_profiles
    .map(p => p.fair_score?.score)
    .filter((s): s is number => s !== undefined && s !== null)
  const group2BiasedScores = data.group2_profiles
    .map(p => p.biased_score?.score)
    .filter((s): s is number => s !== undefined && s !== null)

  const group1FairAvg = group1FairScores.length > 0
    ? group1FairScores.reduce((a, b) => a + b, 0) / group1FairScores.length
    : 0
  const group1BiasedAvg = group1BiasedScores.length > 0
    ? group1BiasedScores.reduce((a, b) => a + b, 0) / group1BiasedScores.length
    : 0
  const group2FairAvg = group2FairScores.length > 0
    ? group2FairScores.reduce((a, b) => a + b, 0) / group2FairScores.length
    : 0
  const group2BiasedAvg = group2BiasedScores.length > 0
    ? group2BiasedScores.reduce((a, b) => a + b, 0) / group2BiasedScores.length
    : 0

  const group1FairApprovals = data.group1_profiles.filter(p => p.fair_score?.approval_decision === 'approve').length
  const group1BiasedApprovals = data.group1_profiles.filter(p => p.biased_score?.approval_decision === 'approve').length
  const group2FairApprovals = data.group2_profiles.filter(p => p.fair_score?.approval_decision === 'approve').length
  const group2BiasedApprovals = data.group2_profiles.filter(p => p.biased_score?.approval_decision === 'approve').length

  const group1FairApprovalRate = data.group1_profiles.length > 0 ? (group1FairApprovals / data.group1_profiles.length) * 100 : 0
  const group1BiasedApprovalRate = data.group1_profiles.length > 0 ? (group1BiasedApprovals / data.group1_profiles.length) * 100 : 0
  const group2FairApprovalRate = data.group2_profiles.length > 0 ? (group2FairApprovals / data.group2_profiles.length) * 100 : 0
  const group2BiasedApprovalRate = data.group2_profiles.length > 0 ? (group2BiasedApprovals / data.group2_profiles.length) * 100 : 0

  const group1FairInterest = data.group1_profiles
    .map(p => p.fair_score?.interest_rate)
    .filter((s): s is number => s !== undefined && s !== null)
  const group1BiasedInterest = data.group1_profiles
    .map(p => p.biased_score?.interest_rate)
    .filter((s): s is number => s !== undefined && s !== null)
  const group2FairInterest = data.group2_profiles
    .map(p => p.fair_score?.interest_rate)
    .filter((s): s is number => s !== undefined && s !== null)
  const group2BiasedInterest = data.group2_profiles
    .map(p => p.biased_score?.interest_rate)
    .filter((s): s is number => s !== undefined && s !== null)

  const group1FairInterestAvg = group1FairInterest.length > 0
    ? group1FairInterest.reduce((a, b) => a + b, 0) / group1FairInterest.length
    : 0
  const group1BiasedInterestAvg = group1BiasedInterest.length > 0
    ? group1BiasedInterest.reduce((a, b) => a + b, 0) / group1BiasedInterest.length
    : 0
  const group2FairInterestAvg = group2FairInterest.length > 0
    ? group2FairInterest.reduce((a, b) => a + b, 0) / group2FairInterest.length
    : 0
  const group2BiasedInterestAvg = group2BiasedInterest.length > 0
    ? group2BiasedInterest.reduce((a, b) => a + b, 0) / group2BiasedInterest.length
    : 0

  // Helper function to create bar chart visualization
  const BarChart = ({ value, maxValue, label, color, showValue = true }: { 
    value: number
    maxValue: number
    label: string
    color: string
    showValue?: boolean
  }) => {
    const percentage = maxValue > 0 ? (value / maxValue) * 100 : 0
    return (
      <div className="space-y-1">
        <div className="flex justify-between items-center text-sm">
          <span className="text-gray-700 font-medium">{label}</span>
          {showValue && <span className="text-gray-900 font-bold">{value.toFixed(1)}</span>}
        </div>
        <div className="w-full bg-gray-200 rounded-full h-6 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${color}`}
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
        </div>
      </div>
    )
  }

  return (
    <Card className="mt-6">
      <CardHeader>
        <div className="flex items-center gap-2">
          <BarChart3 className="h-5 w-5 text-blue-600" />
          <CardTitle>Profile Comparison</CardTitle>
        </div>
        <p className="text-sm text-gray-600 mt-2">
          Fair vs. Biased scoring comparison for <span className="font-semibold">{data.metric.group1_name}</span> vs <span className="font-semibold">{data.metric.group2_name}</span>
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Summary Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
            <div className="flex items-center gap-2 mb-2">
              <Users className="h-4 w-4 text-green-700" />
              <p className="text-sm font-medium text-green-800">Group 1 Fair Score</p>
            </div>
            <p className="text-2xl font-bold text-green-900">{group1FairAvg.toFixed(2)}</p>
            <p className="text-xs text-green-700 mt-1">Avg from {group1FairScores.length} profiles</p>
          </div>
          <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-lg border border-orange-200">
            <div className="flex items-center gap-2 mb-2">
              <Users className="h-4 w-4 text-orange-700" />
              <p className="text-sm font-medium text-orange-800">Group 1 Biased Score</p>
            </div>
            <p className="text-2xl font-bold text-orange-900">{group1BiasedAvg.toFixed(2)}</p>
            <p className="text-xs text-orange-700 mt-1">Avg from {group1BiasedScores.length} profiles</p>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
            <div className="flex items-center gap-2 mb-2">
              <Users className="h-4 w-4 text-green-700" />
              <p className="text-sm font-medium text-green-800">Group 2 Fair Score</p>
            </div>
            <p className="text-2xl font-bold text-green-900">{group2FairAvg.toFixed(2)}</p>
            <p className="text-xs text-green-700 mt-1">Avg from {group2FairScores.length} profiles</p>
          </div>
          <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-lg border border-orange-200">
            <div className="flex items-center gap-2 mb-2">
              <Users className="h-4 w-4 text-orange-700" />
              <p className="text-sm font-medium text-orange-800">Group 2 Biased Score</p>
            </div>
            <p className="text-2xl font-bold text-orange-900">{group2BiasedAvg.toFixed(2)}</p>
            <p className="text-xs text-orange-700 mt-1">Avg from {group2BiasedScores.length} profiles</p>
          </div>
        </div>

        {/* Interest Rate Comparison */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Average Interest Rate Comparison</CardTitle>
            <p className="text-sm text-gray-600">Interest rates offered to each group</p>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm font-medium text-gray-700 mb-4">{data.metric.group1_name}</p>
                <BarChart
                  value={group1FairInterestAvg}
                  maxValue={20}
                  label="Fair Model Interest Rate"
                  color="bg-green-500"
                />
                <div className="mt-3">
                  <BarChart
                    value={group1BiasedInterestAvg}
                    maxValue={20}
                    label="Biased Model Interest Rate"
                    color="bg-orange-500"
                  />
                </div>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700 mb-4">{data.metric.group2_name}</p>
                <BarChart
                  value={group2FairInterestAvg}
                  maxValue={20}
                  label="Fair Model Interest Rate"
                  color="bg-green-500"
                />
                <div className="mt-3">
                  <BarChart
                    value={group2BiasedInterestAvg}
                    maxValue={20}
                    label="Biased Model Interest Rate"
                    color="bg-orange-500"
                  />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Individual Profile Details */}
        <div>
          <h3 className="text-lg font-semibold mb-4 text-gray-900 flex items-center gap-2">
            <Users className="h-5 w-5" />
            Individual Profile Details
          </h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Group 1 */}
            <div>
              <h4 className="text-md font-semibold mb-3 text-gray-800">
                {data.metric.group1_name}
                <span className="ml-2 text-sm font-normal text-gray-500">
                  ({data.group1_profiles.length} profiles)
                </span>
              </h4>
              <div className="space-y-4">
                {data.group1_profiles.map((profileWithScores) => (
                  <ProfileCard
                    key={profileWithScores.profile.id}
                    profileWithScores={profileWithScores}
                    groupName={data.metric.group1_name}
                  />
                ))}
                {data.group1_profiles.length === 0 && (
                  <div className="text-center py-4 text-gray-500 text-sm">
                    No profiles found for this group
                  </div>
                )}
              </div>
            </div>

            {/* Group 2 */}
            <div>
              <h4 className="text-md font-semibold mb-3 text-gray-800">
                {data.metric.group2_name}
                <span className="ml-2 text-sm font-normal text-gray-500">
                  ({data.group2_profiles.length} profiles)
                </span>
              </h4>
              <div className="space-y-4">
                {data.group2_profiles.map((profileWithScores) => (
                  <ProfileCard
                    key={profileWithScores.profile.id}
                    profileWithScores={profileWithScores}
                    groupName={data.metric.group2_name}
                  />
                ))}
                {data.group2_profiles.length === 0 && (
                  <div className="text-center py-4 text-gray-500 text-sm">
                    No profiles found for this group
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}







