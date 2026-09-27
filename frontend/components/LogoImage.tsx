'use client'

interface LogoImageProps {
  className?: string
  width?: number
  height?: number
}

export function LogoImage({ className = '', width = 200, height = 60 }: LogoImageProps) {
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 200 60"
      className={className}
      xmlns="http://www.w3.org/2000/svg"
    >
      <text
        x="10"
        y="45"
        fontSize="42"
        fontWeight="bold"
        fill="#00C853"
        fontFamily="Arial, sans-serif"
        letterSpacing="-1"
      >
        fair lend.
      </text>
    </svg>
  )
}
