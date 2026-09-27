'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import { Loader2, Search, Filter, X, Eye } from 'lucide-react'
import ProfileGeneration from '@/components/dashboard/ProfileGeneration'

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
  co_applicant: string | null
  employment_type: string
  family_structure: string
  test_dimension: string
  created_at: string
  updated_at?: string | null
}

// Helper function to parse region into urban/rural and tier
function parseRegion(region: string): { areaType: string; tier: string } {
  const regionLower = region.toLowerCase()
  const areaType = regionLower.includes('urban') ? 'Urban' : 'Rural'
  
  let tier = 'Tier 1'
  if (regionLower.includes('tier2')) {
    tier = 'Tier 2'
  } else if (regionLower.includes('tier3')) {
    tier = 'Tier 3'
  }
  
  return { areaType, tier }
}

export default function ProfilesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedDimension, setSelectedDimension] = useState<string>('all')
  const [currentPage, setCurrentPage] = useState(0)
  const [pageSize] = useState(50)
  const [selectedProfile, setSelectedProfile] = useState<StudentProfile | null>(null)

  const { data: profiles, isLoading, error, refetch } = useQuery({
    queryKey: ['profiles', currentPage, pageSize],
    queryFn: async () => {
      const response = await apiClient.get('/profiles/', {
        params: {
          skip: currentPage * pageSize,
          limit: pageSize,
        },
      })
      return response.data as StudentProfile[]
    },
  })

  // Filter profiles
  const filteredProfiles = profiles?.filter((profile) => {
    const matchesSearch =
      searchTerm === '' ||
      profile.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      profile.state.toLowerCase().includes(searchTerm.toLowerCase()) ||
      profile.region.toLowerCase().includes(searchTerm.toLowerCase()) ||
      profile.course.toLowerCase().includes(searchTerm.toLowerCase())

    const matchesDimension =
      selectedDimension === 'all' || profile.test_dimension === selectedDimension

    return matchesSearch && matchesDimension
  })

  const dimensions = ['all', 'geographic', 'income', 'credit', 'edge_cases', 'gender']
  const dimensionLabels: Record<string, string> = {
    all: 'All Dimensions',
    geographic: 'Geographic',
    income: 'Income',
    credit: 'Credit',
    edge_cases: 'Edge Cases',
    gender: 'Gender',
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading profiles...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Profiles</h2>
        <p className="text-red-600">
          {error instanceof Error ? error.message : 'Failed to load profiles'}
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Student Profiles</h1>
        <p className="text-gray-600">Generate and view student loan profiles for bias testing</p>
      </div>

      {/* Profile Generation Section */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-1">
        <div className="bg-white rounded-lg">
          <ProfileGeneration />
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              placeholder="Search by name, state, region, or course..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Dimension Filter */}
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <select
              value={selectedDimension}
              onChange={(e) => setSelectedDimension(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none bg-white"
            >
              {dimensions.map((dim) => (
                <option key={dim} value={dim}>
                  {dimensionLabels[dim]}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Results Count */}
        {filteredProfiles && (
          <div className="mt-4 text-sm text-gray-600">
            Showing <span className="font-semibold">{filteredProfiles.length}</span> of{' '}
            <span className="font-semibold">{profiles?.length || 0}</span> profiles
          </div>
        )}
      </div>

      {/* Profiles Grid */}
      {!filteredProfiles || filteredProfiles.length === 0 ? (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-blue-800 mb-2">No Profiles Found</h2>
          <p className="text-blue-600">
            {profiles && profiles.length === 0
              ? 'No profiles have been generated yet. Generate profiles using the dashboard to get started.'
              : 'No profiles match your search criteria. Try adjusting your filters.'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredProfiles.map((profile) => (
            <div
              key={profile.id}
              className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <h3 className="font-semibold text-lg text-gray-900 mb-1 font-mono">
                    {profile.profile_id}
                  </h3>
                  <p className="text-sm text-gray-500 mb-1">
                    {profile.state} • {(() => {
                      const { areaType, tier } = parseRegion(profile.region)
                      return `${areaType} • ${tier}`
                    })()}
                  </p>
                </div>
                <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded whitespace-nowrap ml-2">
                  {profile.test_dimension}
                </span>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Course:</span>
                  <span className="font-medium">{profile.course}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">GPA:</span>
                  <span className="font-medium">{profile.gpa.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">CIBIL Score:</span>
                  <span className="font-medium">{profile.cibil_score}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Family Income:</span>
                  <span className="font-medium">{formatCurrency(profile.family_income)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Loan Amount:</span>
                  <span className="font-medium">{formatCurrency(profile.requested_loan_amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Employment:</span>
                  <span className="font-medium capitalize">{profile.employment_type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Family Structure:</span>
                  <span className="font-medium capitalize">
                    {profile.family_structure.replace('_', ' ')}
                  </span>
                </div>
                {profile.co_applicant && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Co-Applicant:</span>
                    <span className="font-medium capitalize">{profile.co_applicant}</span>
                  </div>
                )}
              </div>

              <div className="mt-3 pt-3 border-t border-gray-200 flex justify-end">
                <button
                  onClick={() => setSelectedProfile(profile)}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors"
                >
                  <Eye className="h-3.5 w-3.5" />
                  See Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Profile Details Modal */}
      {selectedProfile && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto shadow-xl">
            {/* Header with Applicant Name */}
            <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-5 flex justify-between items-center shadow-md">
              <div className="flex-1">
                <div className="mb-2">
                  <p className="text-blue-200 text-xs uppercase tracking-wide mb-1">Student Name</p>
                  <h2 className="text-3xl font-bold">
                    {selectedProfile.name}
                  </h2>
                </div>
                <p className="text-blue-100 text-sm">
                  Profile ID: {selectedProfile.profile_id} • {selectedProfile.state} • {(() => {
                    const { areaType, tier } = parseRegion(selectedProfile.region)
                    return `${areaType} • ${tier}`
                  })()}
                </p>
              </div>
              <button
                onClick={() => setSelectedProfile(null)}
                className="p-2 hover:bg-blue-800 rounded-full transition-colors text-white"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <div className="p-6">
              {/* Quick Summary Card */}
              <div className="mb-6 bg-gradient-to-br from-gray-50 to-blue-50 rounded-lg p-4 border border-gray-200">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">GPA</p>
                    <p className="text-lg font-bold text-gray-900">{selectedProfile.gpa.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">CIBIL Score</p>
                    <p className="text-lg font-bold text-gray-900">{selectedProfile.cibil_score}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Loan Amount</p>
                    <p className="text-lg font-bold text-gray-900">{formatCurrency(selectedProfile.requested_loan_amount)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Test Dimension</p>
                    <span className="inline-block px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                      {selectedProfile.test_dimension.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Personal Information - Highlighted */}
                <div className="bg-white border-2 border-blue-200 rounded-lg p-4">
                  <h4 className="text-sm font-semibold text-blue-700 mb-4 uppercase tracking-wide flex items-center gap-2">
                    <span className="w-1 h-4 bg-blue-600 rounded"></span>
                    Applicant Information
                  </h4>
                  <div className="space-y-4">
                    <div className="pb-3 border-b border-gray-100">
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Full Name</span>
                      <p className="text-lg font-bold text-gray-900">
                        {selectedProfile.name}
                      </p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Location</span>
                      <p className="text-sm font-medium text-gray-900">{selectedProfile.state}</p>
                      <p className="text-xs text-gray-600">{(() => {
                        const { areaType, tier } = parseRegion(selectedProfile.region)
                        return `${areaType} • ${tier}`
                      })()}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Postcode</span>
                      <p className="text-sm font-medium text-gray-900">{selectedProfile.postcode}</p>
                    </div>
                  </div>
                </div>

                {/* Database Information */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">System Information</h4>
                  <div className="space-y-3">
                    <div>
                      <span className="text-sm text-gray-600">Database ID:</span>
                      <p className="text-sm font-mono font-medium">#{selectedProfile.id}</p>
                    </div>
                    <div>
                      <span className="text-sm text-gray-600">Profile ID:</span>
                      <p className="text-sm font-mono font-medium">{selectedProfile.profile_id}</p>
                    </div>
                    <div>
                      <span className="text-sm text-gray-600">Test Dimension:</span>
                      <p className="text-sm font-medium capitalize">
                        {selectedProfile.test_dimension.replace('_', ' ')}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Academic Information */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">Academic Information</h4>
                  <div className="space-y-3">
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Course / Degree Program</span>
                      <p className="text-base font-semibold text-gray-900">{selectedProfile.course}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Educational Background</span>
                      <p className="text-base font-semibold text-gray-900 capitalize">{selectedProfile.educational_background}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">GPA (Indian 10-point scale)</span>
                      <p className="text-base font-semibold text-gray-900">{selectedProfile.gpa.toFixed(2)} / 10.0</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {selectedProfile.gpa >= 8.5 ? 'Excellent' : 
                         selectedProfile.gpa >= 7.5 ? 'Very Good' : 
                         selectedProfile.gpa >= 7.0 ? 'Good' : 
                         selectedProfile.gpa >= 6.0 ? 'Satisfactory' : 'Needs Improvement'}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Financial Information */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">Financial Information</h4>
                  <div className="space-y-3">
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Annual Family Income</span>
                      <p className="text-base font-semibold text-gray-900">{formatCurrency(selectedProfile.family_income)}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Requested Loan Amount</span>
                      <p className="text-base font-semibold text-gray-900">{formatCurrency(selectedProfile.requested_loan_amount)}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">CIBIL Credit Score</span>
                      <p className="text-base font-semibold text-gray-900">{selectedProfile.cibil_score}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {selectedProfile.cibil_score >= 750 ? 'Excellent' : 
                         selectedProfile.cibil_score >= 650 ? 'Good' : 
                         selectedProfile.cibil_score >= 600 ? 'Fair' : 'Poor'}
                      </p>
                    </div>
                    <div className="pt-2 border-t border-gray-200">
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Loan to Income Ratio</span>
                      <p className="text-base font-semibold text-gray-900">
                        {((selectedProfile.requested_loan_amount / selectedProfile.family_income) * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                </div>

                {/* Family & Employment */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">Family & Employment Details</h4>
                  <div className="space-y-3">
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Employment Type</span>
                      <p className="text-base font-semibold text-gray-900 capitalize">{selectedProfile.employment_type.replace('-', ' ')}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Family Structure</span>
                      <p className="text-base font-semibold text-gray-900 capitalize">
                        {selectedProfile.family_structure.replace('_', ' ')}
                      </p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Co-Applicant</span>
                      <p className="text-base font-semibold text-gray-900 capitalize">
                        {selectedProfile.co_applicant || 'None'}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {selectedProfile.co_applicant === 'parent' ? 'Parent as co-applicant' :
                         selectedProfile.co_applicant === 'sibling' ? 'Sibling as co-applicant' :
                         selectedProfile.co_applicant === 'spouse' ? 'Spouse as co-applicant' :
                         'No co-applicant'}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Test & Metadata */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">Test Information & Timestamps</h4>
                  <div className="space-y-3">
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Bias Test Dimension</span>
                      <span className="inline-block px-3 py-1 text-sm font-medium bg-purple-100 text-purple-800 rounded">
                        {selectedProfile.test_dimension.replace('_', ' ').toUpperCase()}
                      </span>
                    </div>
                    <div className="pt-2 border-t border-gray-200">
                      <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Profile Created</span>
                      <p className="text-sm font-medium text-gray-900">
                        {new Date(selectedProfile.created_at).toLocaleString('en-IN', {
                          dateStyle: 'long',
                          timeStyle: 'short'
                        })}
                      </p>
                    </div>
                    {selectedProfile.updated_at && (
                      <div>
                        <span className="text-xs text-gray-500 uppercase tracking-wide block mb-1">Last Updated</span>
                        <p className="text-sm font-medium text-gray-900">
                          {new Date(selectedProfile.updated_at).toLocaleString('en-IN', {
                            dateStyle: 'long',
                            timeStyle: 'short'
                          })}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setSelectedProfile(null)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Pagination */}
      {profiles && profiles.length >= pageSize && (
        <div className="flex justify-center items-center gap-4">
          <button
            onClick={() => setCurrentPage((p) => Math.max(0, p - 1))}
            disabled={currentPage === 0}
            className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Previous
          </button>
          <span className="text-sm text-gray-600">
            Page {currentPage + 1}
          </span>
          <button
            onClick={() => setCurrentPage((p) => p + 1)}
            disabled={!profiles || profiles.length < pageSize}
            className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}

