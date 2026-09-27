'use client'

import { X, TrendingUp, TrendingDown, AlertCircle, BarChart3, Target, Info } from 'lucide-react'
import { BiasMetric } from '@/lib/types/metrics'
import { getSeverityColor } from '@/lib/utils'

interface BiasDetailsModalProps {
  metric: BiasMetric
  onClose: () => void
}

export function BiasDetailsModal({ metric, onClose }: BiasDetailsModalProps) {
  // Calculate percentages for visualizations
  const group1ApprovalPct = (metric.group1_approval_rate * 100).toFixed(1)
  const group2ApprovalPct = (metric.group2_approval_rate * 100).toFixed(1)
  const approvalGap = Math.abs(metric.group1_approval_rate - metric.group2_approval_rate) * 100
  
  const parityStatus = metric.approval_parity >= 0.95 ? 'good' : metric.approval_parity >= 0.85 ? 'warning' : 'critical'
  const interestStatus = metric.interest_rate_disparity < 0.5 ? 'good' : metric.interest_rate_disparity < 1.0 ? 'warning' : 'critical'
  const collateralStatus = metric.collateral_gap < 10 ? 'good' : metric.collateral_gap < 20 ? 'warning' : 'critical'
  
  const getStatusColor = (status: string) => {
    if (status === 'good') return 'text-green-600 bg-green-50 border-green-200'
    if (status === 'warning') return 'text-yellow-600 bg-yellow-50 border-yellow-200'
    return 'text-red-600 bg-red-50 border-red-200'
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-y-auto shadow-xl">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-5 flex justify-between items-center shadow-md z-10">
          <div className="flex-1">
            <h2 className="text-2xl font-bold mb-1">
              {metric.group1_name} vs {metric.group2_name}
            </h2>
            <p className="text-blue-100 text-sm capitalize">
              {metric.dimension.replace('_', ' ')} • Severity: {metric.severity}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-blue-800 rounded-full transition-colors text-white"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Key Metrics Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className={`p-4 rounded-lg border-2 ${getStatusColor(parityStatus)}`}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">Approval Parity</span>
                {parityStatus === 'good' ? (
                  <TrendingUp className="h-4 w-4" />
                ) : (
                  <TrendingDown className="h-4 w-4" />
                )}
              </div>
              <p className="text-2xl font-bold">{metric.approval_parity.toFixed(3)}</p>
              <p className="text-xs mt-1">Target: ≥0.95</p>
            </div>

            <div className={`p-4 rounded-lg border-2 ${getStatusColor(interestStatus)}`}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">Interest Gap</span>
                {interestStatus === 'good' ? (
                  <TrendingUp className="h-4 w-4" />
                ) : (
                  <TrendingDown className="h-4 w-4" />
                )}
              </div>
              <p className="text-2xl font-bold">{metric.interest_rate_disparity.toFixed(2)}%</p>
              <p className="text-xs mt-1">Target: &lt;0.5%</p>
            </div>

            <div className={`p-4 rounded-lg border-2 ${getStatusColor(collateralStatus)}`}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">Collateral Gap</span>
                {collateralStatus === 'good' ? (
                  <TrendingUp className="h-4 w-4" />
                ) : (
                  <TrendingDown className="h-4 w-4" />
                )}
              </div>
              <p className="text-2xl font-bold">{metric.collateral_gap.toFixed(1)}%</p>
              <p className="text-xs mt-1">Target: &lt;10%</p>
            </div>

            <div className={`p-4 rounded-lg border-2 ${getSeverityColor(metric.severity)}`}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">Fairness Score</span>
                <Target className="h-4 w-4" />
              </div>
              <p className="text-2xl font-bold">{metric.overall_fairness_score.toFixed(1)}</p>
              <p className="text-xs mt-1">Target: ≥85/100</p>
            </div>
          </div>

          {/* Approval Rate Comparison - Visual Bar Chart */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-blue-600" />
              Approval Rate Comparison
            </h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">{metric.group1_name}</span>
                    <span className="text-sm font-bold text-gray-900">{group1ApprovalPct}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-8 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-blue-600 to-blue-700 flex items-center justify-end pr-3 text-white text-xs font-medium transition-all"
                      style={{ width: `${Math.min(100, parseFloat(group1ApprovalPct))}%` }}
                    >
                      {parseFloat(group1ApprovalPct) > 10 && `${group1ApprovalPct}%`}
                    </div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">{metric.group2_name}</span>
                    <span className="text-sm font-bold text-gray-900">{group2ApprovalPct}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-8 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-gray-600 to-gray-700 flex items-center justify-end pr-3 text-white text-xs font-medium transition-all"
                      style={{ width: `${Math.min(100, parseFloat(group2ApprovalPct))}%` }}
                    >
                      {parseFloat(group2ApprovalPct) > 10 && `${group2ApprovalPct}%`}
                    </div>
                  </div>
                </div>

              <div className="pt-2 border-t border-gray-300">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-semibold text-gray-700">Approval Gap</span>
                  <span className={`text-sm font-bold ${approvalGap > 10 ? 'text-red-600' : approvalGap > 5 ? 'text-yellow-600' : 'text-green-600'}`}>
                    {approvalGap.toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Interest Rate Comparison with Visual Chart */}
            <div className="bg-white border border-gray-200 rounded-lg p-5">
              <h4 className="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-blue-600" />
                Interest Rate Disparity
              </h4>
              <div className="space-y-4">
                {/* Visual Comparison Bars */}
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">{metric.group1_name}</span>
                      <span className="text-sm font-bold text-blue-700">
                        {metric.group1_interest_rate?.toFixed(2) || 'N/A'}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-8 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-600 to-blue-700 flex items-center justify-end pr-3 text-white text-xs font-semibold transition-all"
                        style={{ width: `${Math.min(100, ((metric.group1_interest_rate || 0) / 20) * 100)}%` }}
                      >
                        {metric.group1_interest_rate && metric.group1_interest_rate > 2 && `${metric.group1_interest_rate.toFixed(2)}%`}
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">{metric.group2_name}</span>
                      <span className="text-sm font-bold text-gray-700">
                        {metric.group2_interest_rate?.toFixed(2) || 'N/A'}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-8 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-gray-600 to-gray-700 flex items-center justify-end pr-3 text-white text-xs font-semibold transition-all"
                        style={{ width: `${Math.min(100, ((metric.group2_interest_rate || 0) / 20) * 100)}%` }}
                      >
                        {metric.group2_interest_rate && metric.group2_interest_rate > 2 && `${metric.group2_interest_rate.toFixed(2)}%`}
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="pt-3 border-t border-gray-200">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-semibold text-gray-700">Disparity</span>
                    <span className={`text-lg font-bold ${interestStatus === 'critical' ? 'text-red-600' : interestStatus === 'warning' ? 'text-yellow-600' : 'text-green-600'}`}>
                      {metric.interest_rate_disparity.toFixed(2)}%
                    </span>
                  </div>
                  {metric.interest_rate_disparity > 0.5 && (
                    <p className="text-xs text-red-600 mt-1 flex items-center gap-1">
                      <AlertCircle className="h-3 w-3" />
                      Significant interest rate bias detected
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* Collateral Requirement Comparison with Visual Chart */}
            <div className="bg-white border border-gray-200 rounded-lg p-5">
              <h4 className="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Target className="h-4 w-4 text-blue-600" />
                Collateral Requirements
              </h4>
              <div className="space-y-4">
                {/* Visual Comparison Bars */}
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">{metric.group1_name}</span>
                      <span className="text-sm font-bold text-blue-700">
                        {metric.group1_collateral_pct?.toFixed(1) || 'N/A'}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-8 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-600 to-blue-700 flex items-center justify-end pr-3 text-white text-xs font-semibold transition-all"
                        style={{ width: `${Math.min(100, metric.group1_collateral_pct || 0)}%` }}
                      >
                        {metric.group1_collateral_pct && metric.group1_collateral_pct > 5 && `${metric.group1_collateral_pct.toFixed(1)}%`}
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">{metric.group2_name}</span>
                      <span className="text-sm font-bold text-gray-700">
                        {metric.group2_collateral_pct?.toFixed(1) || 'N/A'}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-8 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-gray-600 to-gray-700 flex items-center justify-end pr-3 text-white text-xs font-semibold transition-all"
                        style={{ width: `${Math.min(100, metric.group2_collateral_pct || 0)}%` }}
                      >
                        {metric.group2_collateral_pct && metric.group2_collateral_pct > 5 && `${metric.group2_collateral_pct.toFixed(1)}%`}
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="pt-3 border-t border-gray-200">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-semibold text-gray-700">Gap</span>
                    <span className={`text-lg font-bold ${collateralStatus === 'critical' ? 'text-red-600' : collateralStatus === 'warning' ? 'text-yellow-600' : 'text-green-600'}`}>
                      {metric.collateral_gap.toFixed(1)}%
                    </span>
                  </div>
                  {metric.collateral_gap > 10 && (
                    <p className="text-xs text-red-600 mt-1 flex items-center gap-1">
                      <AlertCircle className="h-3 w-3" />
                      Unequal collateral requirements detected
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Comparison Summary Chart */}
          <div className="bg-gradient-to-br from-slate-50 to-gray-50 border border-gray-200 rounded-lg p-6">
            <h4 className="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-gray-700" />
              Comprehensive Comparison Summary
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Approval Rate Visual */}
              <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                <p className="text-xs font-semibold text-gray-600 mb-3 uppercase tracking-wide">Approval Rates</p>
                <div className="flex items-end justify-center gap-4 h-36 relative">
                  <div className="flex flex-col items-center flex-1">
                    <div className="relative w-full flex justify-center">
                      <div 
                        className="w-12 bg-gradient-to-t from-blue-600 to-blue-700 rounded-t transition-all mb-2 min-h-[4px]"
                        style={{ 
                          height: `${Math.max(4, (parseFloat(group1ApprovalPct) / 100) * 128)}px`,
                          maxHeight: '128px'
                        }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-900 mt-1">{group1ApprovalPct}%</span>
                    <span className="text-xs text-gray-600 mt-0.5 font-medium">{metric.group1_name.split(' ')[0]}</span>
                  </div>
                  <div className="flex flex-col items-center flex-1">
                    <div className="relative w-full flex justify-center">
                      <div 
                        className="w-12 bg-gradient-to-t from-gray-600 to-gray-700 rounded-t transition-all mb-2 min-h-[4px]"
                        style={{ 
                          height: `${Math.max(4, (parseFloat(group2ApprovalPct) / 100) * 128)}px`,
                          maxHeight: '128px'
                        }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-900 mt-1">{group2ApprovalPct}%</span>
                    <span className="text-xs text-gray-600 mt-0.5 font-medium">{metric.group2_name.split(' ')[0]}</span>
                  </div>
                </div>
              </div>
              
              {/* Interest Rate Visual */}
              <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                <p className="text-xs font-semibold text-gray-600 mb-3 uppercase tracking-wide">Interest Rates</p>
                <div className="flex items-end justify-center gap-4 h-36 relative">
                  <div className="flex flex-col items-center flex-1">
                    <div className="relative w-full flex justify-center">
                      <div 
                        className="w-12 bg-gradient-to-t from-blue-600 to-blue-700 rounded-t transition-all mb-2 min-h-[4px]"
                        style={{ 
                          height: `${Math.max(4, ((metric.group1_interest_rate || 0) / 20) * 128)}px`,
                          maxHeight: '128px'
                        }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-900 mt-1">{metric.group1_interest_rate ? metric.group1_interest_rate.toFixed(1) : 'N/A'}%</span>
                    <span className="text-xs text-gray-600 mt-0.5 font-medium">{metric.group1_name.split(' ')[0]}</span>
                  </div>
                  <div className="flex flex-col items-center flex-1">
                    <div className="relative w-full flex justify-center">
                      <div 
                        className="w-12 bg-gradient-to-t from-gray-600 to-gray-700 rounded-t transition-all mb-2 min-h-[4px]"
                        style={{ 
                          height: `${Math.max(4, ((metric.group2_interest_rate || 0) / 20) * 128)}px`,
                          maxHeight: '128px'
                        }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-900 mt-1">{metric.group2_interest_rate ? metric.group2_interest_rate.toFixed(1) : 'N/A'}%</span>
                    <span className="text-xs text-gray-600 mt-0.5 font-medium">{metric.group2_name.split(' ')[0]}</span>
                  </div>
                </div>
              </div>
              
              {/* Collateral Visual */}
              <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                <p className="text-xs font-semibold text-gray-600 mb-3 uppercase tracking-wide">Collateral Required</p>
                <div className="flex items-end justify-center gap-4 h-36 relative">
                  <div className="flex flex-col items-center flex-1">
                    <div className="relative w-full flex justify-center">
                      <div 
                        className="w-12 bg-gradient-to-t from-blue-600 to-blue-700 rounded-t transition-all mb-2 min-h-[4px]"
                        style={{ 
                          height: `${Math.max(4, ((metric.group1_collateral_pct || 0) / 100) * 128)}px`,
                          maxHeight: '128px'
                        }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-900 mt-1">{metric.group1_collateral_pct ? metric.group1_collateral_pct.toFixed(1) : 'N/A'}%</span>
                    <span className="text-xs text-gray-600 mt-0.5 font-medium">{metric.group1_name.split(' ')[0]}</span>
                  </div>
                  <div className="flex flex-col items-center flex-1">
                    <div className="relative w-full flex justify-center">
                      <div 
                        className="w-12 bg-gradient-to-t from-gray-600 to-gray-700 rounded-t transition-all mb-2 min-h-[4px]"
                        style={{ 
                          height: `${Math.max(4, ((metric.group2_collateral_pct || 0) / 100) * 128)}px`,
                          maxHeight: '128px'
                        }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-900 mt-1">{metric.group2_collateral_pct ? metric.group2_collateral_pct.toFixed(1) : 'N/A'}%</span>
                    <span className="text-xs text-gray-600 mt-0.5 font-medium">{metric.group2_name.split(' ')[0]}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Statistical Information */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-5">
            <h4 className="text-base font-semibold text-blue-900 mb-3 flex items-center gap-2">
              <Info className="h-4 w-4" />
              Statistical Analysis
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-blue-700 font-medium block mb-1">Approval Parity</span>
                <span className="text-blue-900 font-bold">
                  {metric.approval_parity.toFixed(3)}
                </span>
                <p className="text-xs text-blue-600 mt-1">
                  {metric.approval_parity >= 0.95 ? '✓ Within target' : '✗ Below target'}
                </p>
              </div>
              <div>
                <span className="text-blue-700 font-medium block mb-1">Edge Case Coverage</span>
                <span className="text-blue-900 font-bold">
                  {metric.edge_case_coverage?.toFixed(1) || 'N/A'}%
                </span>
                <p className="text-xs text-blue-600 mt-1">
                  {metric.edge_case_coverage && metric.edge_case_coverage >= 95 ? '✓ Good coverage' : '⚠ Needs improvement'}
                </p>
              </div>
              <div>
                <span className="text-blue-700 font-medium block mb-1">Overall Fairness</span>
                <span className="text-blue-900 font-bold">
                  {metric.overall_fairness_score.toFixed(1)}/100
                </span>
                <p className="text-xs text-blue-600 mt-1">
                  {metric.overall_fairness_score >= 85 ? '✓ Fair' : metric.overall_fairness_score >= 70 ? '⚠ Moderate bias' : '✗ Significant bias'}
                </p>
              </div>
              <div>
                <span className="text-blue-700 font-medium block mb-1">Severity Level</span>
                <span className={`inline-block px-2 py-1 rounded text-xs font-medium capitalize ${getSeverityColor(metric.severity)}`}>
                  {metric.severity}
                </span>
                <p className="text-xs text-blue-600 mt-1">
                  {metric.severity === 'critical' ? '✗ Requires immediate attention' : 
                   metric.severity === 'high' ? '⚠ High priority' : 
                   metric.severity === 'medium' ? '⚠ Monitor closely' : '✓ Low priority'}
                </p>
              </div>
            </div>
          </div>

          {/* Interpretation */}
          <div className="bg-gray-50 rounded-lg p-5">
            <h4 className="text-base font-semibold text-gray-900 mb-3">Interpretation</h4>
            <div className="space-y-2 text-sm text-gray-700">
              <p>
                This analysis compares <strong>{metric.group1_name}</strong> and <strong>{metric.group2_name}</strong> across the <strong>{metric.dimension.replace('_', ' ')}</strong> dimension.
              </p>
              {metric.approval_parity < 0.95 && (
                <p className="text-red-700">
                  <strong>⚠ Approval Bias:</strong> The approval rate disparity ({approvalGap.toFixed(1)}%) indicates that {metric.group1_name} applicants are 
                  {metric.approval_parity > 1 ? ' more likely' : ' less likely'} to be approved compared to {metric.group2_name} applicants.
                </p>
              )}
              {metric.interest_rate_disparity > 0.5 && (
                <p className="text-orange-700">
                  <strong>⚠ Interest Rate Bias:</strong> There is a significant difference ({metric.interest_rate_disparity.toFixed(2)}%) in average interest rates between the two groups, suggesting potential pricing discrimination.
                </p>
              )}
              {metric.collateral_gap > 10 && (
                <p className="text-yellow-700">
                  <strong>⚠ Collateral Bias:</strong> The collateral requirement gap ({metric.collateral_gap.toFixed(1)}%) shows unequal treatment in loan terms between groups.
                </p>
              )}
            </div>
          </div>

          {/* Action Button */}
          <div className="flex justify-end gap-3 pt-4 border-t">
            <button
              onClick={onClose}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
