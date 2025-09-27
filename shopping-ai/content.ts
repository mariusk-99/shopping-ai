import type { PlasmoCSConfig } from "plasmo"

// Configure the content script to run only on specific URLs
export const config: PlasmoCSConfig = {
  matches: [
    "https://www.nike.com/gb/t/club-open-hem-fleece-trousers-k62luLev/FN3730-063",
    "https://www.shein.co.uk/goods-p-158264809.html*"
  ],
  all_frames: false
}

interface ProductAnalysis {
  url: string
  timestamp: number
  analysis: string
  site: 'nike' | 'shein'
  tags: string[]
}

// Predefined analyses for specific products
const productAnalyses: Record<string, ProductAnalysis> = {
  "https://www.nike.com/gb/t/club-open-hem-fleece-trousers-k62luLev/FN3730-063": {
    url: "https://www.nike.com/gb/t/club-open-hem-fleece-trousers-k62luLev/FN3730-063",
    timestamp: Date.now(),
    site: "nike",
    analysis: "The reviews are mostly positive, with shoppers praising the comfort, fit, and style of the products. Many highlight that items are true to size, soft, and well-organized in stores, which makes shopping easier. Several customers bought the products for teenagers or grandkids, who also liked them. A few people mentioned they would repurchase in other colors. However, there is one very negative review that criticizes the material, sizing, and comfort, noting that even sizing up did not help. Overall, the feedback shows strong satisfaction with quality and comfort, though sizing consistency may be an issue for some customers.",
    tags: ["Comfortable", "True to Size", "Well-Organized", "Size Consistency Varies"]
  },
  "https://www.shein.co.uk/goods-p-158264809.html": {
    url: "https://www.shein.co.uk/goods-p-158264809.html",
    timestamp: Date.now(),
    site: "shein",
    analysis: "Product analysis will be available once loaded",
    tags: []
  }
}

// Create a custom event to communicate with the popup
const sendAnalysisData = () => {
  const currentUrl = window.location.href.split('?')[0] // Remove query parameters
  const analysisData = productAnalyses[currentUrl]

  if (analysisData) {
    const event = new CustomEvent("shoppingAiAnalysis", {
      detail: {
        ...analysisData,
        timestamp: Date.now()
      }
    })
    window.dispatchEvent(event)
    console.log("Shopping AI: Analysis data sent", analysisData)
  }
}

// Initialize when the content script loads
window.addEventListener("load", () => {
  console.log("Shopping AI: Content script initialized on product page")
  
  // Delay to simulate analysis
  setTimeout(() => {
    sendAnalysisData()
  }, 20000) // 20 seconds delay
})