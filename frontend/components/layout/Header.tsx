'use client'

import { useState, useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { User, LogOut, ChevronDown } from 'lucide-react'
import { Logo } from '@/components/Logo'

interface UserInfo {
  id: number
  employee_id: string
  full_name: string
  email?: string
  role: string
  is_active: boolean
}

export function Header() {
  const router = useRouter()
  const pathname = usePathname()
  const [user, setUser] = useState<UserInfo | null>(null)
  const [showProfileMenu, setShowProfileMenu] = useState(false)
  const [logoImageLoaded, setLogoImageLoaded] = useState(false)

  useEffect(() => {
    // Get user from localStorage
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        setUser(JSON.parse(userStr))
      } catch (e) {
        console.error('Error parsing user data:', e)
      }
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  // Don't show profile on login page
  if (pathname === '/login') {
    return null
  }

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {/* Always show text logo - image replaces it if available */}
          {!logoImageLoaded && <Logo size="md" />}
          <img
            src="/logo.png"
            alt="fair lend."
            className={`h-12 w-auto object-contain ${logoImageLoaded ? 'block' : 'hidden'}`}
            onLoad={() => setLogoImageLoaded(true)}
            onError={() => setLogoImageLoaded(false)}
          />
          <span className="text-sm text-gray-500 hidden lg:block">|</span>
          <span className="text-sm text-gray-600 hidden lg:block">
            AI Validation System
          </span>
        </div>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600 hidden md:block">
            GenAI-Powered Bias Detection
          </span>
          
          {/* Profile Section */}
          {user && (
            <div className="relative">
              <button
                onClick={() => setShowProfileMenu(!showProfileMenu)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                  <User className="h-5 w-5 text-blue-600" />
                </div>
                <div className="hidden md:block text-left">
                  <p className="text-sm font-medium text-gray-900">{user.full_name}</p>
                  <p className="text-xs text-gray-500">{user.employee_id} • {user.role}</p>
                </div>
                <ChevronDown className="h-4 w-4 text-gray-400" />
              </button>

              {/* Profile Dropdown Menu */}
              {showProfileMenu && (
                <>
                  <div 
                    className="fixed inset-0 z-10" 
                    onClick={() => setShowProfileMenu(false)}
                  />
                  <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 z-20">
                    <div className="p-4 border-b border-gray-200">
                      <p className="text-sm font-semibold text-gray-900">{user.full_name}</p>
                      <p className="text-xs text-gray-500 mt-1">{user.employee_id}</p>
                      <p className="text-xs text-gray-500">{user.email || 'No email'}</p>
                      <span className="inline-block mt-2 px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded capitalize">
                        {user.role}
                      </span>
                    </div>
                    <div className="p-2">
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors"
                      >
                        <LogOut className="h-4 w-4" />
                        <span>Sign Out</span>
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  )
}







