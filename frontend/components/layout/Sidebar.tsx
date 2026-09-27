'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  LayoutDashboard, 
  BarChart3, 
  MessageSquare, 
  TrendingUp,
  Users,
  User
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Profiles', href: '/profiles', icon: Users },
  { name: 'Bias Analysis', href: '/bias-analysis', icon: BarChart3 },
  { name: 'Feedback', href: '/feedback', icon: MessageSquare },
  { name: 'Mitigation', href: '/mitigation', icon: TrendingUp },
]

interface UserInfo {
  employee_id: string
  full_name: string
  role: string
}

export function Sidebar() {
  const pathname = usePathname()
  const [user, setUser] = useState<UserInfo | null>(null)

  useEffect(() => {
    // Get user from localStorage
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        const userData = JSON.parse(userStr)
        setUser({
          employee_id: userData.employee_id,
          full_name: userData.full_name,
          role: userData.role
        })
      } catch (e) {
        console.error('Error parsing user data:', e)
      }
    }
  }, [])

  // Don't show sidebar on login page
  if (pathname === '/login') {
    return null
  }

  return (
    <aside className="w-64 bg-white shadow-sm border-r border-gray-200 flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Navigation</h2>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                'flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
                isActive
                  ? 'bg-blue-50 text-blue-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-50'
              )}
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </Link>
          )
        })}
      </nav>
      
      {/* Profile Section at Bottom */}
      {user && (
        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center space-x-3 px-4 py-3 bg-gray-50 rounded-lg">
            <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
              <User className="h-5 w-5 text-blue-600" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {user.full_name}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {user.employee_id}
              </p>
              <p className="text-xs text-gray-400 capitalize mt-0.5">
                {user.role}
              </p>
            </div>
          </div>
        </div>
      )}
    </aside>
  )
}







