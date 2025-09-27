import React, { useState, useEffect } from "react";

// Simple SVG icons as React components (typed)
const CheckCircle: React.FC<{ className?: string; style?: React.CSSProperties }> = ({ className, style }) => (
  <svg className={className} style={style} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
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

// Configuration for the content script (move to a separate file if needed)
export const config = {
  matches: ["<all_urls>"],
  all_frames: false,
  run_at: "document_end"
};

type SafetyStatus = "safe" | "caution" | "unsafe";

interface SafetyData {
  status: SafetyStatus;
  confidence: number;
  threats: string[];
  details: string;
}

// Mock function to simulate loading and determine website safety
const getWebsiteSafety = async (url: string): Promise<SafetyData> => {
  // Simulate loading delay
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  const domain = new URL(url).hostname;
  
  if (domain.includes("bank") || domain.includes("gov") || domain.includes("edu")) {
    return {
      status: "safe",
      confidence: 95,
      threats: [],
      details: "This website appears to be legitimate and secure."
    };
  } else if (domain.includes("unknown") || domain.includes("suspicious") || domain.includes("ads")) {
    return {
      status: "caution",
      confidence: 60,
      threats: ["Suspicious redirects", "Unknown reputation"],
      details: "Exercise caution when sharing personal information."
    };
  } else {
    return {
      status: "unsafe",
      confidence: 85,
      threats: ["Phishing attempt", "Malicious content", "Data harvesting"],
      details: "This website may pose security risks. Avoid sharing sensitive data."
    };
  }
};


const WebsiteSafetyExtension: React.FC = () => {
  const [isVisible, setIsVisible] = useState(true);
  const [isLoading, setIsLoading] = useState(true);
  const [safetyData, setSafetyData] = useState<SafetyData | null>(null);

  useEffect(() => {
    const loadSafetyData = async () => {
      setIsLoading(true);
      try {
        const currentUrl = window.location.href; // read inside effect
        const data = await getWebsiteSafety(currentUrl);
        setSafetyData(data);
      } catch (error) {
        console.error("Failed to load safety data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    loadSafetyData();
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


  if (!isVisible) return null;

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
          <div style={titleStyle}>Website Safety</div>
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

        {/* Image Section */}
        <div style={sectionStyle}>
          <div style={titleStyle}>Check if you are going to slay in it:</div>
          <div style={uploadAreaStyle}>
            <ImageIcon style={{ width: '32px', height: '32px', marginBottom: '8px' }} />
            <span style={{ fontSize: '12px' }}>Upload image</span>
          </div>
        </div>

        {/* Insights Section */}
        <div style={sectionStyle}>
          <div style={titleStyle}>Slayy's personal advice</div>
          <div style={insightsListStyle}>
            <div>• Personalized safety recommendations</div>
            <div>• Style and reputation insights</div>
            <div>• Smart shopping guidance</div>
            <div>• Trust score analysis</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WebsiteSafetyExtension;