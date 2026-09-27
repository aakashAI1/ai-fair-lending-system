'use client'

import { KPIMetrics, SeverityLevel } from '@/lib/types/metrics'
import { formatPercentage, getSeverityColor } from '@/lib/utils'
import { AlertCircle, TrendingDown, Shield, BarChart3, CheckCircle2, XCircle } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'

interface KPICardsProps {
  metrics: KPIMetrics
}

export function KPICards({ metrics }: KPICardsProps) {
  const cards = [
    {
      title: 'Approval Parity',
      description: 'Ratio of approval rates between groups',
      value: metrics.approval_parity.toFixed(2),
      target: '≥0.95',
      icon: BarChart3,
      isPass: metrics.approval_parity >= 0.95,
      color: metrics.approval_parity >= 0.95 ? 'text-green-600' : 'text-red-600',
      bgColor: metrics.approval_parity >= 0.95 ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200',
      iconBg: metrics.approval_parity >= 0.95 ? 'bg-green-100' : 'bg-red-100',
    },
    {
      title: 'Interest Gap',
      description: 'Difference in interest rates (%)',
      value: `${metrics.interest_gap.toFixed(2)}%`,
      target: '<0.5%',
      icon: TrendingDown,
      isPass: metrics.interest_gap < 0.5,
      color: metrics.interest_gap < 0.5 ? 'text-green-600' : 'text-red-600',
      bgColor: metrics.interest_gap < 0.5 ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200',
      iconBg: metrics.interest_gap < 0.5 ? 'bg-green-100' : 'bg-red-100',
    },
    {
      title: 'Collateral Gap',
      description: 'Difference in collateral requirements (%)',
      value: `${metrics.collateral_gap.toFixed(1)}%`,
      target: '<10%',
      icon: Shield,
      isPass: metrics.collateral_gap < 10,
      color: metrics.collateral_gap < 10 ? 'text-green-600' : 'text-red-600',
      bgColor: metrics.collateral_gap < 10 ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200',
      iconBg: metrics.collateral_gap < 10 ? 'bg-green-100' : 'bg-red-100',
    },
    {
      title: 'Fairness Score',
      description: 'Overall fairness metric (0-100)',
      value: metrics.fairness_score.toFixed(1),
      target: '≥85/100',
      icon: AlertCircle,
      isPass: metrics.fairness_score >= 85,
      color: metrics.fairness_score >= 85 ? 'text-green-600' : 'text-red-600',
      bgColor: metrics.fairness_score >= 85 ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200',
      iconBg: metrics.fairness_score >= 85 ? 'bg-green-100' : 'bg-red-100',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {cards.map((card) => {
        const Icon = card.icon
        return (
          <Card key={card.title} className={`${card.bgColor} border-2 shadow-sm hover:shadow-md transition-shadow`}>
            <CardContent className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-sm font-semibold text-gray-700 mb-1">{card.title}</h3>
                  <p className="text-xs text-gray-500">{card.description}</p>
                </div>
                <div className={`${card.iconBg} p-2 rounded-lg`}>
                  <Icon className={`h-5 w-5 ${card.color}`} />
                </div>
              </div>
              <div className="flex items-baseline justify-between">
                <div>
                  <p className={`text-3xl font-bold ${card.color} mb-1`}>
                    {card.value}
                  </p>
                  <div className="flex items-center gap-2">
                    {card.isPass ? (
                      <CheckCircle2 className="h-4 w-4 text-green-600" />
                    ) : (
                      <XCircle className="h-4 w-4 text-red-600" />
                    )}
                    <p className="text-xs text-gray-600">Target: {card.target}</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}







