import { useEffect, useState } from "react"
import ShimmerLoading from "~components/ui/loading/ShimmerLoading"
import "~styles/shimmer.css"

const ALLOWED_URLS = [
  "https://www.nike.com/gb/t/club-open-hem-fleece-trousers-k62luLev/FN3730-063",
  "https://www.shein.co.uk/goods-p-158264809.html"
]

function IndexPopup() {
  const [isLoading, setIsLoading] = useState(false)
  const [data, setData] = useState("")
  const [currentUrl, setCurrentUrl] = useState<string>("")
  const [isValidPage, setIsValidPage] = useState(false)
  const [showAnalysis, setShowAnalysis] = useState(false)
  const [analysisData, setAnalysisData] = useState<{
    analysis: string
    site: 'nike' | 'shein'
    tags: string[]
  } | null>(null)

  useEffect(() => {
    // Get current tab URL
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const url = tabs[0]?.url || ""
      setCurrentUrl(url)
      
      // Check if we're on a valid product page
      const isValid = ALLOWED_URLS.some(validUrl => url.startsWith(validUrl))
      setIsValidPage(isValid)
      
      if (isValid) {
        setIsLoading(true)
        
        // Listen for analysis data from content script
        const handleAnalysis = (event: CustomEvent) => {
          setAnalysisData(event.detail)
          setIsLoading(false)
          setShowAnalysis(true)
        }

        window.addEventListener("shoppingAiAnalysis", handleAnalysis as EventListener)
        
        return () => {
          window.removeEventListener("shoppingAiAnalysis", handleAnalysis as EventListener)
        }
      }
    })
  }, [])

  return (
    <div
      style={{
        padding: 16,
        width: 400,
        minHeight: 200
      }}>
      <h2 className="text-xl font-bold mb-4 text-center">
        Shopping AI Assistant
      </h2>
      
      {!isValidPage ? (
        <div className="text-center text-gray-600 p-4">
          This extension only works on specific product pages:
          <ul className="text-xs mt-2 text-gray-500 list-disc list-inside">
            <li className="truncate">Nike Club Open-Hem Fleece Trousers</li>
            <li className="truncate">Shein Product #158264809</li>
          </ul>
        </div>
      ) : isLoading ? (
        <ShimmerLoading />
      ) : (
        <div className="space-y-4">
          <div className="text-center text-green-600 font-medium mb-4">
            Analysis Complete!
          </div>
          
          {showAnalysis && currentUrl.includes('nike.com') && (
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-4 mb-4 border border-purple-100">
              <div className="flex items-center mb-4">
                <span className="text-xl mr-2">💅</span>
                <h3 className="font-bold text-purple-800 text-lg">Slayy's Shopping Advice</h3>
              </div>
              
              <div className="text-sm text-gray-700 space-y-2 mb-4">
                {nikeAnalysis.split('. ').map((sentence, index) => (
                  <p key={index} className="leading-relaxed flex items-start">
                    <span className="mr-2 text-purple-400">•</span>
                    {sentence}.
                  </p>
                ))}
              </div>
              
              <div className="mt-4 space-y-2">
                <div className="text-sm font-medium text-purple-800 mb-2">Quick Tags:</div>
                <div className="flex flex-wrap gap-2">
                  <span className="bg-purple-100 text-purple-800 text-xs px-3 py-1 rounded-full border border-purple-200">✨ Comfortable</span>
                  <span className="bg-purple-100 text-purple-800 text-xs px-3 py-1 rounded-full border border-purple-200">📏 True to Size</span>
                  <span className="bg-purple-100 text-purple-800 text-xs px-3 py-1 rounded-full border border-purple-200">🛍️ Well-Organized</span>
                  <span className="bg-yellow-100 text-yellow-700 text-xs px-3 py-1 rounded-full border border-yellow-200">⚠️ Size Consistency Varies</span>
                </div>
              </div>
              
              <div className="mt-4 text-xs text-purple-600 flex items-center">
                <span className="mr-1">💫</span>
                <span>Powered by AI Shopping Assistant</span>
              </div>
            </div>
          )}

          <div className="border-t pt-4">
            <input 
              className="w-full px-3 py-2 border rounded-md"
              onChange={(e) => setData(e.target.value)} 
              value={data}
              placeholder="Ask a question about this product..." 
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default IndexPopup
