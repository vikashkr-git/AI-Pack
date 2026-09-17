import React from 'react';

export const MarqueeTicker: React.FC = () => {
  const tickerItems = [
    { text: "ASTM D3985 Coulometric OTR", style: "tag-pill-yellow" },
    { text: "18,000+ Calibrated Pairs", style: "tag-pill-cyan" },
    { text: "Zero Data Leakage ML", style: "tag-pill-pink" },
    { text: "Arrhenius Mass-Transfer", style: "tag-pill-emerald" },
    { text: "ASTM F1249 Modulated IR WVTR", style: "tag-pill-yellow" },
    { text: "Grouped Random Forest R² = 0.997", style: "tag-pill-pink" },
    { text: "Circular Bio-Based Polymers", style: "tag-pill-emerald" },
    { text: "Kader Fresh Produce Respiration", style: "tag-pill-cyan" },
  ];

  const displayItems = [...tickerItems, ...tickerItems];

  return (
    <div className="w-full overflow-hidden py-4 my-10 relative z-10 select-none">
      <div className="animate-marquee-smooth flex items-center space-x-6">
        {displayItems.map((item, idx) => (
          <div key={idx} className="flex items-center space-x-4 flex-shrink-0">
            <span className={`tag-pill ${item.style} text-[11px] py-1.5 px-4 font-mono shadow-sm`}>
              {item.text}
            </span>
            <span className="text-white/25 text-sm font-light">✦</span>
          </div>
        ))}
      </div>
    </div>
  );
};
