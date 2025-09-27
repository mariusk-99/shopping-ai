import React, { useState, useEffect } from "react";

// Import Nike assets to ensure they're included in the build
import nikeImage1 from "./assets/nike/Gemini_Generated_Image_alooralooraloora.png";
import nikeImage2 from "./assets/nike/Gemini_Generated_Image_oafcb5oafcb5oafc.png";
import nikeImage3 from "./assets/nike/Gemini_Generated_Image_zes4mczes4mczes4.png";

// Import Shein assets to ensure they're included in the build
import sheinImage1 from "./assets/shein/Gemini_Generated_Image_iqwxnliqwxnliqwx.png";
import sheinImage2 from "./assets/shein/Gemini_Generated_Image_iqwxnliqwxnliqwx (1).png";

// Simple SVG icons as React components (typed)
const CheckCircle: React.FC<{ className?: string; style?: React.CSSProperties }> = ({ className, style }) => (
  <svg className={className} style={style} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414          {/* Slayy's Shopping Advice Section */}
        <div style={sectionStyle}>
          <div style={titleStyle}>💅 Slayy's Shopping Advice</div>
          {isLoading ? (
            <div style={{
              padding: '16px',
              backgroundColor: '#f3f4f6',
              borderRadius: '8px',
              animation: 'shimmer 1.5s infinite linear'
            }}>
              Analyzing product details...
            </div>
          ) : analysisData ? (
            <div style={{
              backgroundColor: '#fdf4ff',
              borderRadius: '8px',
              padding: '16px',
              border: '1px solid #f5d0fe'
            }}>
              <p style={{ fontSize: '14px', lineHeight: '1.6', color: '#581c87' }}>
                {analysisData.analysis}
              </p>
              <div style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '8px',
                marginTop: '12px'
              }}>
                {analysisData.tags.map((tag, index) => (
                  <span key={index} style={{
                    backgroundColor: '#f3e8ff',
                    color: '#6b21a8',
                    padding: '4px 8px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    border: '1px solid #e9d5ff'
                  }}>
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ) : null}
        </div>

          {/* Safety Section */}
        <div style={sectionStyle}>
          <div style={titleStyle}>Shopping Safety</div>414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
  </svg>
);

const AlertTriangle: React.FC<{ className?: string; style?: React.CSSProperties }> = ({ className, style }) => (
  <svg className={className} style={style} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
  </svg>
);

const XCircle: React.FC<{ className?: string; style?: React.CSSProperties }> = ({ className, style }) => (
  <svg className={className} style={style} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
  </svg>
);

const ImageIcon: React.FC<{ className?: string; style?: React.CSSProperties }> = ({ className, style }) => (
  <svg className={className} style={style} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
    <circle cx="8.5" cy="8.5" r="1.5" />
    <polyline points="21,15 16,10 5,21" />
  </svg>
);

const X: React.FC<{ className?: string; style?: React.CSSProperties }> = ({ className, style }) => (
  <svg className={className} style={style} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
);

// Configuration for the content script - only run on specific shopping sites
export const config = {
  matches: [
    "https://www.nike.com/gb/t/club-open-hem-fleece-trousers-k62luLev/FN3730-063",
    "https://www.shein.co.uk/goods-p-158264809.html*"
  ],
  all_frames: false,
  run_at: "document_end"
};

interface ProductAnalysis {
  url: string;
  analysis: string;
  tags: string[];
  timestamp: number;
  brand: 'nike' | 'shein';
}

type SafetyStatus = "safe" | "caution" | "unsafe";

interface SafetyData {
  status: SafetyStatus;
  confidence: number;
  threats: string[];
  details: string;
}

// Analyze website safety for shopping sites
const getWebsiteSafety = async (url: string): Promise<SafetyData> => {
  // Simulate loading delay
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  const domain = new URL(url).hostname;
  
  // Nike - Premium brand, generally safe
  if (domain.includes("nike.com")) {
    return {
      status: "safe",
      confidence: 95,
      threats: [],
      details: "Nike is a trusted global brand with secure shopping experience."
    };
  } 
  // Shein - Fast fashion retailer, generally safe but with some considerations
  else if (domain.includes("shein.co.uk")) {
    return {
      status: "caution",
      confidence: 75,
      threats: ["Fast fashion concerns", "Environmental impact"],
      details: "Shein is a legitimate retailer, but consider sustainability and quality factors."
    };
  } 
  // Fallback for other domains
  else {
    return {
      status: "unsafe",
      confidence: 85,
      threats: ["Unknown retailer", "Potential security risks"],
      details: "This website may pose security risks. Avoid sharing sensitive data."
    };
  }
};


// Helper function to get asset URL
const getAssetURL = (path: string): string => {
  try {
    // Type assertion for chrome extension API
    return (window as any).chrome.runtime.getURL(path);
  } catch (error) {
    // Fallback for development
    return path;
  }
};

// Media assets for each brand - using imported assets
const brandAssets = {
  nike: {
    images: [
      nikeImage1,
      nikeImage2,
      nikeImage3
    ],
    videos: [
      getAssetURL("assets/nike/Generated File September 27, 2025 - 2_09PM.mp4")
    ]
  },
  shein: {
    images: [
      sheinImage1,
      sheinImage2
    ],
    videos: []
  }
};

// Check if current URL matches the specific product pages
const isTargetProductPage = (url: string): boolean => {
  // Check for specific product identifiers in the URL
  const nikeProductId = "club-open-hem-fleece-trousers-k62luLev/FN3730-063";
  const sheinProductId = "goods-p-158264809.html";
  
  return url.includes(nikeProductId) || url.includes(sheinProductId);
};

// Get current brand based on URL
const getCurrentBrand = (url: string): 'nike' | 'shein' | null => {
  if (url.includes("nike.com")) return 'nike';
  if (url.includes("shein.co.uk")) return 'shein';
  return null;
};


const WebsiteSafetyExtension: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false); // Start hidden
  const [isLoading, setIsLoading] = useState(true);
  const [safetyData, setSafetyData] = useState<SafetyData | null>(null);
  const [mediaLoading, setMediaLoading] = useState(true);
  const [currentMediaIndex, setCurrentMediaIndex] = useState(0);
  const [analysisData, setAnalysisData] = useState<ProductAnalysis | null>(null);

  // Predefined product analyses
  const productAnalyses: Record<string, ProductAnalysis> = {
    "https://www.nike.com/gb/t/club-open-hem-fleece-trousers-k62luLev/FN3730-063": {
      url: "https://www.nike.com/gb/t/club-open-hem-fleece-trousers-k62luLev/FN3730-063",
      analysis: "The reviews are mostly positive, with shoppers praising the comfort, fit, and style of the products. Many highlight that items are true to size, soft, and well-organized in stores, which makes shopping easier. Several customers bought the products for teenagers or grandkids, who also liked them. A few people mentioned they would repurchase in other colors. However, there is one very negative review that criticizes the material, sizing, and comfort, noting that even sizing up did not help. Overall, the feedback shows strong satisfaction with quality and comfort, though sizing consistency may be an issue for some customers.",
      tags: ["Comfortable", "True to Size", "Well-Organized", "Size Consistency Varies"],
      timestamp: Date.now(),
      brand: "nike"
    },
    "https://www.shein.co.uk/goods-p-158264809.html": {
      url: "https://www.shein.co.uk/goods-p-158264809.html",
      analysis: "Product analysis coming soon",
      tags: [],
      timestamp: Date.now(),
      brand: "shein"
    }
  };

  // Add CSS animations for shimmer loading - MUST be at top level
  React.useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
      }
    `;
    document.head.appendChild(style);
    return () => {
      if (document.head.contains(style)) {
        document.head.removeChild(style);
      }
    };
  }, []);

  useEffect(() => {
    console.log("🔥 Slayy Extension - Script loaded!");
    
    const currentUrl = window.location.href;
    
    // Debug: Log current URL and check result
    console.log("🌐 Slayy Extension - Current URL:", currentUrl);
    console.log("🔍 Slayy Extension - URL includes nike.com:", currentUrl.includes("nike.com"));
    console.log("🔍 Slayy Extension - URL includes shein.co.uk:", currentUrl.includes("shein.co.uk"));
    console.log("🎯 Slayy Extension - Is target page:", isTargetProductPage(currentUrl));
    
    // TEMPORARY: Show on any Nike or Shein page for testing
    const isNikeOrShein = currentUrl.includes("nike.com") || currentUrl.includes("shein.co.uk");
    
    if (!isNikeOrShein) {
      console.log("❌ Slayy Extension - Not Nike or Shein, hiding extension");
      setIsVisible(false);
      return;
    }

    console.log("✅ Slayy Extension - Nike or Shein detected, showing extension");
    setIsVisible(true);

    const loadSafetyData = async () => {
      setIsLoading(true);
      try {
        const data = await getWebsiteSafety(currentUrl);
        setSafetyData(data);
      } catch (error) {
        console.error("Failed to load safety data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    const loadMedia = async () => {
      setMediaLoading(true);
      // Show loading for 3 seconds to simulate analysis
      await new Promise(resolve => setTimeout(resolve, 3000));
      setMediaLoading(false);
    };

    loadSafetyData();
    loadMedia();
  }, []); // no need to include window.location.href here

  const getStatusIcon = (status: SafetyStatus): JSX.Element | null => {
    const iconStyle = { width: "20px", height: "20px", color: "white" } as React.CSSProperties;
    switch (status) {
      case "safe":
        return <CheckCircle style={iconStyle} />;
      case "caution":
        return <AlertTriangle style={iconStyle} />;
      case "unsafe":
        return <XCircle style={iconStyle} />;
      default:
        return null;
    }
  };

  const getCurrentBrandAssets = () => {
    const currentUrl = window.location.href;
    const brand = getCurrentBrand(currentUrl);
    return brand ? brandAssets[brand] : null;
  };

  const getAllMedia = () => {
    const assets = getCurrentBrandAssets();
    if (!assets) return [];
    return [...assets.images, ...assets.videos];
  };

  const nextMedia = () => {
    const allMedia = getAllMedia();
    setCurrentMediaIndex((prev) => (prev + 1) % allMedia.length);
  };

  const prevMedia = () => {
    const allMedia = getAllMedia();
    setCurrentMediaIndex((prev) => (prev - 1 + allMedia.length) % allMedia.length);
  };

  const isVideo = (path: string) => path.endsWith('.mp4');


  console.log("🎨 Slayy Extension - Render check, isVisible:", isVisible);
  
  if (!isVisible) {
    console.log("👻 Slayy Extension - Not visible, returning null");
    return null;
  }
  
  console.log("🚀 Slayy Extension - Rendering extension!");

  const containerStyle: React.CSSProperties = {
    position: 'fixed',
    top: '20px',
    right: '20px',
    width: '320px',
    maxHeight: '600px',
    backgroundColor: 'white',
    border: '1px solid #e5e7eb',
    borderRadius: '12px',
    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)',
    zIndex: 999999,
    fontFamily: 'system-ui, -apple-system, sans-serif',
    color: '#1f2937',
    overflow: 'hidden',
    animation: 'slideUp 0.3s ease-out, float 3s ease-in-out infinite'
  };

  const headerStyle: React.CSSProperties = {
    backgroundColor: '#f9fafb',
    padding: '16px',
    borderBottom: '1px solid #e5e7eb',
    position: 'relative'
  };

  const closeButtonStyle: React.CSSProperties = {
    position: 'absolute',
    top: '8px',
    right: '8px',
    width: '32px',
    height: '32px',
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer',
    borderRadius: '6px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#6b7280'
  };

  const contentStyle: React.CSSProperties = {
    padding: '16px',
    overflow: 'auto',
    maxHeight: '500px'
  };

  const sectionStyle: React.CSSProperties = {
    marginBottom: '24px',
    paddingBottom: '16px',
    borderBottom: '1px solid #e5e7eb'
  };

  const titleStyle: React.CSSProperties = {
    fontSize: '18px',
    fontWeight: '600',
    marginBottom: '16px',
    color: '#1f2937'
  };

  const statusContainerStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '16px'
  };

  const statusIconStyle: React.CSSProperties = {
    width: '48px',
    height: '48px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0
  };

  const statusTextStyle: React.CSSProperties = {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '8px'
  };

  const statusDescStyle: React.CSSProperties = {
    fontSize: '14px',
    color: '#6b7280',
    lineHeight: '1.5'
  };

  const uploadAreaStyle: React.CSSProperties = {
    width: '128px',
    height: '128px',
    backgroundColor: '#f3f4f6',
    border: '2px dashed #d1d5db',
    borderRadius: '8px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '0 auto',
    color: '#6b7280',
    cursor: 'pointer'
  };

  const insightsListStyle: React.CSSProperties = {
    fontSize: '14px',
    color: '#6b7280',
    lineHeight: '1.6'
  };

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={headerStyle}>
        <button
          onClick={() => setIsVisible(false)}
          style={closeButtonStyle}
        >
          <X style={{ width: '16px', height: '16px' }} />
        </button>
        <h2 style={{ fontSize: '14px', fontWeight: '600', margin: 0, paddingTop: '8px' }}>
          💅 Slayyyy
        </h2>
      </div>

      {/* Content */}
      <div style={contentStyle}>
        {/* Safety Section */}
        <div style={sectionStyle}>
          <div style={titleStyle}>Shopping Safety</div>
          {isLoading ? (
            <div style={{ color: '#6b7280' }}>Loading safety data...</div>
          ) : safetyData ? (
            <div style={statusContainerStyle}>
              <div style={{
                ...statusIconStyle,
                backgroundColor: safetyData.status === "safe" ? "#10b981" : 
                                safetyData.status === "caution" ? "#f59e0b" : "#ef4444"
              }}>
                {getStatusIcon(safetyData.status)}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{
                  ...statusTextStyle,
                  color: safetyData.status === "safe" ? "#10b981" : 
                         safetyData.status === "caution" ? "#f59e0b" : "#ef4444"
                }}>
                  {safetyData.status === "safe" ? "Safe" : 
                   safetyData.status === "caution" ? "Caution" : "Unsafe"}
                </div>
                <p style={statusDescStyle}>
                  {safetyData.status === "safe" ? "This website has a good reputation." :
                   safetyData.status === "caution" ? "Exercise caution when browsing this website." :
                   "This website may pose security risks."}
                </p>
              </div>
            </div>
          ) : (
            <div style={{ color: '#6b7280' }}>Failed to load safety data</div>
          )}
        </div>

        {/* Media Section */}
        <div style={sectionStyle}>
          <div style={titleStyle}>Style Check - Will you slay in this?</div>
          <div style={{ 
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            width: '100%'
          }}>
            {(() => {
              const allMedia = getAllMedia();
              const currentMedia = allMedia[currentMediaIndex];
              
              return (
                <div style={{ 
                  position: 'relative',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '100%',
                  minHeight: '400px',
                  padding: '20px 0'
                }}>
                  {/* Carousel Container */}
                  <div style={{
                    position: 'relative',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '100%',
                    maxWidth: '360px',
                    margin: '0 auto'
                  }}>
                    {/* Media container with enhanced styling */}
                    <div style={{
                      width: '280px',
                      height: '320px',
                      borderRadius: '20px',
                      border: 'none',
                      position: 'relative',
                      overflow: 'hidden',
                      boxShadow: '0 20px 40px rgba(0, 0, 0, 0.15), 0 10px 20px rgba(0, 0, 0, 0.1)',
                      background: 'linear-gradient(145deg, #ffffff, #f8f9fa)',
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                      transform: 'perspective(1000px) rotateX(2deg)',
                    }}>
                    {/* Shimmer loading overlay */}
                    {mediaLoading && (
                      <div style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f8fafc 100%)',
                        backgroundSize: '200% 200%',
                        animation: 'shimmer 2s ease-in-out infinite',
                        borderRadius: '20px'
                      }}></div>
                    )}
                    
                    {/* Actual media */}
                    {!mediaLoading && currentMedia && (
                      <>
                        {isVideo(currentMedia) ? (
                          <video
                            src={currentMedia}
                            style={{
                              width: '100%',
                              height: '100%',
                              objectFit: 'cover',
                              borderRadius: '20px',
                              transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
                            }}
                            controls
                            autoPlay
                            muted
                            loop
                          />
                        ) : (
                          <img
                            src={currentMedia}
                            alt="Style preview"
                            style={{
                              width: '100%',
                              height: '100%',
                              objectFit: 'cover',
                              borderRadius: '20px',
                              transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
                            }}
                            onLoad={() => {
                              // Add subtle scale animation on load
                              const img = document.querySelector('img[src="' + currentMedia + '"]') as HTMLElement;
                              if (img) {
                                img.style.transform = 'scale(1.02)';
                                setTimeout(() => {
                                  img.style.transform = 'scale(1)';
                                }, 200);
                              }
                            }}
                          />
                        )}
                      </>
                    )}
                  </div>
                  
                    {/* Enhanced Navigation buttons */}
                    {!mediaLoading && allMedia.length > 1 && (
                      <>
                        <button
                          onClick={prevMedia}
                          style={{
                            position: 'absolute',
                            left: '-50px',
                            top: '50%',
                            transform: 'translateY(-50%)',
                          width: '44px',
                          height: '44px',
                          borderRadius: '22px',
                          border: 'none',
                          backgroundColor: 'rgba(255, 255, 255, 0.95)',
                          color: '#374151',
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '20px',
                          fontWeight: 'bold',
                          boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15), 0 3px 10px rgba(0, 0, 0, 0.1)',
                          transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                          backdropFilter: 'blur(10px)',
                          zIndex: 10
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.transform = 'translateY(-50%) scale(1.1)';
                          e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 1)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.transform = 'translateY(-50%) scale(1)';
                          e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
                        }}
                      >
                        ←
                      </button>
                        <button
                          onClick={nextMedia}
                          style={{
                            position: 'absolute',
                            right: '-50px',
                            top: '50%',
                            transform: 'translateY(-50%)',
                          width: '44px',
                          height: '44px',
                          borderRadius: '22px',
                          border: 'none',
                          backgroundColor: 'rgba(255, 255, 255, 0.95)',
                          color: '#374151',
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '20px',
                          fontWeight: 'bold',
                          boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15), 0 3px 10px rgba(0, 0, 0, 0.1)',
                          transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                          backdropFilter: 'blur(10px)',
                          zIndex: 10
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.transform = 'translateY(-50%) scale(1.1)';
                          e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 1)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.transform = 'translateY(-50%) scale(1)';
                          e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
                        }}
                      >
                            →
                          </button>
                        </>
                      )}
                  </div>
                  
                  {/* Enhanced dot indicators */}
                  {!mediaLoading && allMedia.length > 1 && (
                    <div style={{
                      display: 'flex',
                      gap: '8px',
                      alignItems: 'center',
                      justifyContent: 'center',
                      marginTop: '20px',
                      width: '100%'
                    }}>
                      {allMedia.map((_, index) => (
                        <button
                          key={index}
                          onClick={() => setCurrentMediaIndex(index)}
                          style={{
                            width: index === currentMediaIndex ? '24px' : '8px',
                            height: '8px',
                            borderRadius: '4px',
                            border: 'none',
                            backgroundColor: index === currentMediaIndex ? '#8b5cf6' : '#d1d5db',
                            cursor: 'pointer',
                            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                            opacity: index === currentMediaIndex ? 1 : 0.6
                          }}
                        />
                      ))}
                    </div>
                  )}
                  
                  {/* Enhanced Media counter */}
                  {!mediaLoading && (
                    <div style={{ 
                      marginTop: '12px', 
                      fontSize: '13px', 
                      color: '#8b5cf6',
                      fontWeight: '500',
                      letterSpacing: '0.5px',
                      textAlign: 'center',
                      width: '100%'
                    }}>
                      {(() => {
                        const allMedia = getAllMedia();
                        return `${currentMediaIndex + 1} of ${allMedia.length}`;
                      })()}
                    </div>
                  )}
                </div>
              );
            })()}
          </div>
        </div>

        {/* Insights Section */}
        <div style={sectionStyle}>
          <div style={titleStyle}>Slayy's Shopping Advice</div>
          <div style={insightsListStyle}>
            {(() => {
              const currentUrl = window.location.href;
              const brand = getCurrentBrand(currentUrl);
              
              if (brand === 'nike') {
                return (
                  <div style={{ fontSize: '14px', lineHeight: '1.6', color: '#374151' }}>
                    <p style={{ marginBottom: '8px' }}>
                      <strong>Customer Reviews Summary:</strong>
                    </p>
                    <p>
                      The reviews are mostly positive, with shoppers praising the comfort, fit, and style of the products. 
                      Many highlight that items are true to size, soft, and well-organized in stores, which makes shopping easier. 
                      Several customers bought the products for teenagers or grandkids, who also liked them. A few people 
                      mentioned they would repurchase in other colors. However, there is one very negative review that 
                      criticizes the material, sizing, and comfort, noting that even sizing up did not help. Overall, 
                      the feedback shows strong satisfaction with quality and comfort, though sizing consistency may be 
                      an issue for some customers.
                    </p>
                  </div>
                );
              } else if (brand === 'shein') {
                return (
                  <div style={{ fontSize: '14px', lineHeight: '1.6', color: '#374151' }}>
                    <p style={{ marginBottom: '8px' }}>
                      <strong>Customer Reviews Summary:</strong>
                    </p>
                    <p>
                      The feedback is mostly very positive, with customers praising the set for being elegant, stylish, 
                      and true to size. Many noted that the outfit looks just like the photos, fits well, and includes 
                      the belt as shown. Shoppers from different body types and sizes generally found it flattering, 
                      with some saying they would buy it again. Words like "superb," "beautiful," and "magnificent" 
                      are used often.
                    </p>
                  </div>
                );
              } else {
                return (
                  <div>
                    <div>• Price comparison analysis</div>
                    <div>• Quality vs value assessment</div>
                    <div>• Style compatibility check</div>
                    <div>• Brand reputation insights</div>
                  </div>
                );
              }
            })()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WebsiteSafetyExtension;