'use client'

interface LogoProps {
  className?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

export function Logo({ className = '', size = 'md' }: LogoProps) {
  const sizeClasses = {
    sm: 'text-2xl',
    md: 'text-3xl',
    lg: 'text-4xl',
    xl: 'text-5xl'
  }

  return (
    <h1 className={`font-bold text-[#00C853] tracking-tight ${sizeClasses[size]} ${className}`}>
      fair lend.
    </h1>
  )
}
