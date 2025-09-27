import { useEffect, useState } from "react"

const steps = [
  "Scraping Data...",
  "Generating Images...",
  "Generating Analysis..."
]

const ShimmerLoading = () => {
  const [currentStep, setCurrentStep] = useState(0)
  const [progress, setProgress] = useState(0)
  
  useEffect(() => {
    const duration = 20000 // 20 seconds
    const stepDuration = duration / steps.length
    let startTime = Date.now()

    const timer = setInterval(() => {
      const elapsed = Date.now() - startTime
      const totalProgress = (elapsed / duration) * 100
      
      if (totalProgress >= 100) {
        clearInterval(timer)
        setProgress(100)
        return
      }
      
      setProgress(totalProgress)
      setCurrentStep(Math.floor((elapsed / stepDuration)))
    }, 100)

    return () => clearInterval(timer)
  }, [])

  return (
    <div className="w-full max-w-md mx-auto p-4">
      <div className="relative">
        {/* Progress bar background */}
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          {/* Shimmer effect */}
          <div
            className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 animate-shimmer"
            style={{
              width: `${progress}%`,
              transition: "width 0.1s ease-out",
            }}
          />
        </div>
        
        {/* Current step text */}
        <div className="mt-4 text-center">
          <p className="text-lg font-medium text-gray-700">
            {steps[Math.min(currentStep, steps.length - 1)]}
          </p>
          <p className="text-sm text-gray-500 mt-1">
            {Math.min(Math.round(progress), 100)}%
          </p>
        </div>
      </div>
    </div>
  )
}

export default ShimmerLoading