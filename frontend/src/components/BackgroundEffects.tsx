import React from 'react';

export const BackgroundEffects: React.FC = () => {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      
      {/* Soft Luminous Aurora Ambient Halos (Cinematic & Atmospheric) */}
      <div className="absolute -top-32 left-1/4 w-[650px] h-[650px] bg-[#ffd905]/[0.05] rounded-full blur-[160px] animate-float-gentle" />
      
      <div className="absolute top-1/3 -right-32 w-[600px] h-[600px] bg-[#ff64d5]/[0.05] rounded-full blur-[170px] animate-float-slow" />
      
      <div className="absolute -bottom-36 left-1/3 w-[700px] h-[700px] bg-[#06b6d4]/[0.05] rounded-full blur-[180px] animate-float-gentle" />

      {/* Subtle Floating Sparkles */}
      <div className="absolute top-[20%] left-[8%] w-1.5 h-1.5 bg-[#ffd905]/40 rounded-full blur-[0.5px] animate-pulse" />
      <div className="absolute top-[35%] right-[10%] w-2 h-2 bg-[#ff64d5]/40 rounded-full blur-[0.5px] animate-pulse delay-700" />
      <div className="absolute bottom-[25%] left-[12%] w-1.5 h-1.5 bg-[#06b6d4]/40 rounded-full blur-[0.5px] animate-pulse delay-1000" />

      {/* Subtle Background Radial Vignette */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_0%,rgba(6,10,19,0.7)_100%)] pointer-events-none" />
    </div>
  );
};
