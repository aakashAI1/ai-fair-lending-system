'use client'

import { useEffect, useState } from 'react'
import { usePathname, useRouter } from 'next/navigation'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

export function AppLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()
  const [isChecking, setIsChecking] = useState(true)

  useEffect(() => {
    // Only check auth for protected routes (not login page)
    if (pathname !== '/login') {
      const token = localStorage.getItem('access_token')
      const user = localStorage.getItem('user')
      if (!token || !user) {
        router.push('/login')
        return
      }
    }
    setIsChecking(false)
  }, [pathname, router])

  // Show loading while checking (only for protected routes)
  if (isChecking && pathname !== '/login') {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // Login page - no layout
  if (pathname === '/login') {
    return <>{children}</>
  }

  // Protected pages - with layout
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
