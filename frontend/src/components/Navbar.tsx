import React from 'react';
import { 
  ShieldCheck, 
  Zap, 
  Dice5, 
  Layers, 
  FileText, 
  RotateCcw, 
  Sparkles,
  Sliders
} from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  hasResults: boolean;
  onOpenExport: () => void;
  onOpenMaterialsLibrary: () => void;
  onQuickDemo: () => void;
  onRandomCommodity: () => void;
  onReset: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  hasResults,
  onOpenExport,
  onOpenMaterialsLibrary,
  onQuickDemo,
  onRandomCommodity,
  onReset
}) => {
  return (
    <header className="sticky top-5 z-50 px-4 sm:px-8 max-w-7xl mx-auto w-full transition-all duration-300">
      <div className="rounded-full bg-slate-950/70 backdrop-blur-2xl border border-white/15 px-5 sm:px-8 py-3 shadow-[0_20px_60px_rgba(0,0,0,0.6)] flex items-center justify-between gap-4">
        
        {/* Brand Logo */}
        <div 
          className="flex items-center space-x-3 cursor-pointer group flex-shrink-0 select-none" 
          onClick={() => setActiveTab('wizard')}
          title="PackAI - Home"
        >
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-[#ffd905] via-[#ff9900] to-[#ff64d5] p-0.5 shadow-[0_0_20px_rgba(255,217,5,0.4)] group-hover:scale-105 transition-transform flex-shrink-0">
            <div className="w-full h-full bg-[#080d19] rounded-[14px] flex items-center justify-center p-1.5">
              <svg className="w-full h-full" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5.5 4.5C5.5 3.94772 5.94772 3.5 6.5 3.5H17.5C18.0523 3.5 18.5 3.94772 18.5 4.5L19.5 17.5C19.6 18.8 18.8 20.2 17.2 21C15.5 21.8 8.5 21.8 6.8 21C5.2 20.2 4.4 18.8 4.5 17.5L5.5 4.5Z" fill="url(#navPouchGrad)" stroke="#ffffff" strokeWidth="1.2" strokeLinejoin="round"/>
                <line x1="6" y1="5.5" x2="18" y2="5.5" stroke="#ffffff" strokeWidth="0.8" strokeDasharray="1.5 1.5"/>
                <path d="M8.5 9.5C8.5 9 9 8.5 9.5 8.5H14.5C15 8.5 15.5 9 15.5 9.5V15.5C15.5 16.8 14 18 12 18C10 18 8.5 16.8 8.5 15.5V9.5Z" fill="#090e1a" stroke="#22d3ee" strokeWidth="1"/>
                <path d="M12 11C12 11 14 12.2 14 14C14 15.2 13 16 12 16C11 16 10 15.2 10 14C10 12.2 12 11 12 11Z" fill="#34d399"/>
                <defs>
                  <linearGradient id="navPouchGrad" x1="5" y1="3" x2="19" y2="21" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#ffd905"/>
                    <stop offset="1" stopColor="#ff64d5"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xl sm:text-2xl font-black text-white tracking-tight">
              Pack<span className="text-[#ffd905]">AI</span>
            </span>
            <span className="hidden md:inline-flex tag-pill tag-pill-yellow text-[9px] py-0.5 px-2">
              Decision Engine
            </span>
          </div>
        </div>

        {/* Clean, Spacious, 100% Working Action Buttons */}
        <div className="flex items-center space-x-2.5">
          
          {/* 1. Quick Demo */}
          <button
            onClick={onQuickDemo}
            className="btn-luxury-yellow px-4 sm:px-5 py-2 text-xs tracking-wide shadow-lg group"
            title="Instant 1-Click AI recommendation demonstration"
          >
            <Zap className="w-3.5 h-3.5 mr-1.5 fill-current group-hover:scale-125 transition-transform" />
            <span>Instant Demo</span>
          </button>

          {/* 2. Random Food Surprise */}
          <button
            onClick={onRandomCommodity}
            className="btn-luxury-pink px-4 sm:px-5 py-2 text-xs tracking-wide shadow-lg group hidden sm:inline-flex"
            title="Surprise me with a random food commodity from USDA database"
          >
            <Dice5 className="w-3.5 h-3.5 mr-1.5 stroke-[2.5] group-hover:rotate-180 transition-transform duration-500" />
            <span>Random Food</span>
          </button>

          {/* 3. Materials Library */}
          <button
            onClick={onOpenMaterialsLibrary}
            className="btn-luxury-glass px-4 sm:px-5 py-2 text-xs tracking-wide"
            title="Explore all 15+ packaging materials with OTR & WVTR barrier specs"
          >
            <Layers className="w-3.5 h-3.5 mr-1.5 text-[#22d3ee]" />
            <span>Materials Library</span>
          </button>

          {/* 4. Results View Indicator (When Active) */}
          {hasResults && (
            <button
              onClick={() => setActiveTab('results')}
              className={`px-4 py-2 rounded-full text-xs font-bold transition-all cursor-pointer flex items-center space-x-1.5 ${
                activeTab === 'results'
                  ? 'bg-gradient-to-r from-[#ffd905] to-[#f5b700] text-slate-950 shadow-[0_0_20px_rgba(255,217,5,0.4)]'
                  : 'bg-white/10 text-white hover:bg-white/20 border border-white/20'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>View Picks</span>
            </button>
          )}

        </div>

        {/* Right Actions: Dossier & Reset */}
        <div className="flex items-center space-x-2.5 flex-shrink-0">
          
          {/* Printable Technical Dossier */}
          <button
            onClick={onOpenExport}
            className="btn-luxury-glass px-4 py-2 text-xs tracking-wide hidden lg:inline-flex"
            title="Open printable technical packaging dossier"
          >
            <FileText className="w-3.5 h-3.5 mr-1.5 text-[#ff64d5]" />
            <span>Dossier</span>
          </button>

          {/* Reset State Button */}
          <button
            onClick={onReset}
            className="w-10 h-10 rounded-full bg-white/[0.06] hover:bg-white/[0.12] border border-white/15 flex items-center justify-center text-slate-300 hover:text-white hover:rotate-180 transition-all duration-300 cursor-pointer shadow-sm"
            title="Reset analysis and start fresh"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

        </div>

      </div>
    </header>
  );
};
