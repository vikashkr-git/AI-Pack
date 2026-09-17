import React from 'react';
import { Leaf, Recycle, AlertTriangle, CheckCircle2, ArrowRight, ShieldCheck, Sparkles } from 'lucide-react';
import { RecommendationResponse } from '../types';

interface SustainabilityProps {
  results: RecommendationResponse;
}

export const SustainabilityView: React.FC<SustainabilityProps> = ({ results }) => {
  const ecoAlt = results.sustainable_alternative;

  return (
    <div className="space-y-10 max-w-5xl mx-auto animate-fade-in-up py-4">
      
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto">
        <div className="flex justify-center mb-3">
          <span className="tag-pill tag-pill-emerald text-xs">
            ✦ Circular Life Cycle Assessment
          </span>
        </div>
        <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
          Sustainable Packaging <span className="text-[#34d399]">Intelligence</span>
        </h2>
        <p className="text-sm text-slate-300 mt-2 font-sans">
          Evaluating bio-based polymers, post-consumer recycled (PCR) content, and mono-material recyclability against barrier protection requirements.
        </p>
      </div>

      {/* Sustainable Alternative Highlight Card */}
      {ecoAlt ? (
        <div className="glass-luxury rounded-[36px] p-8 sm:p-12 border border-emerald-500/30 relative overflow-hidden">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-8 border-b border-white/10 gap-6">
            <div>
              <span className="tag-pill tag-pill-emerald text-[10px] mb-3">
                ★ Top Sustainable Benchmark
              </span>
              <h3 className="text-2xl sm:text-4xl font-extrabold text-white mt-2 leading-tight">
                {ecoAlt.name}
              </h3>
              <p className="text-sm text-[#34d399] font-mono mt-1">{ecoAlt.structure}</p>
            </div>
            
            {/* Score Pill */}
            <div className="flex items-center space-x-4 bg-white/[0.04] p-4 rounded-3xl border border-white/12 shadow-lg">
              <div className="text-right">
                <span className="text-xs text-slate-400 uppercase font-semibold block">Suitability Score</span>
                <span className="text-xs text-[#34d399] font-mono font-bold">Eco Certified</span>
              </div>
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-[#34d399] to-[#10b981] p-0.5">
                <div className="w-full h-full bg-[#080d19] rounded-[14px] flex flex-col items-center justify-center">
                  <span className="text-2xl font-extrabold text-[#34d399]">{ecoAlt.suitability_score}</span>
                  <span className="text-[9px] font-mono text-slate-400 -mt-0.5">/ 100</span>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-5 py-8 border-b border-white/10 text-xs font-mono">
            <div className="p-5 rounded-3xl bg-white/[0.03] border border-white/10">
              <span className="text-slate-400 block mb-1 text-[11px] uppercase">Recyclability Stream</span>
              <span className="text-lg font-bold text-white">{ecoAlt.eco_highlights.recyclability_stream || 'Compostable'}</span>
            </div>

            <div className="p-5 rounded-3xl bg-white/[0.03] border border-white/10">
              <span className="text-slate-400 block mb-1 text-[11px] uppercase">Bio-Based Content</span>
              <span className="text-lg font-bold text-[#34d399]">{ecoAlt.eco_highlights.bio_based_pct || 0}%</span>
            </div>

            <div className="p-5 rounded-3xl bg-white/[0.03] border border-white/10">
              <span className="text-slate-400 block mb-1 text-[11px] uppercase">PCR Recycled Content</span>
              <span className="text-lg font-bold text-[#22d3ee]">{ecoAlt.eco_highlights.recycled_content_pct || 0}%</span>
            </div>

            <div className="p-5 rounded-3xl bg-white/[0.03] border border-white/10">
              <span className="text-slate-400 block mb-1 text-[11px] uppercase">Biodegradability</span>
              <span className="text-base font-bold text-white">
                {ecoAlt.eco_highlights.compostable ? 'ASTM D6400 Certified' : 'Mono-PE Recyclable'}
              </span>
            </div>
          </div>

          {/* Trade-off Analysis */}
          <div className="pt-8">
            <div className="flex items-center space-x-2 mb-3">
              <span className="tag-pill tag-pill-yellow text-[10px]">
                ★ Physical Barrier vs Circularity Trade-Off
              </span>
            </div>
            <div className="p-6 rounded-3xl bg-white/[0.03] border border-amber-500/30 text-xs sm:text-sm text-slate-200 leading-relaxed font-sans shadow-lg">
              {ecoAlt.trade_off_analysis}
            </div>
          </div>
        </div>
      ) : (
        <div className="p-12 rounded-[36px] glass-luxury text-center text-slate-300 border border-white/15">
          Current top recommendation structure already complies with optimal sustainability guidelines.
        </div>
      )}

      {/* Recyclability Stream Guidelines */}
      <div className="glass-luxury rounded-[36px] p-8 sm:p-12 border border-white/15">
        <div className="flex items-center space-x-3 mb-6">
          <span className="tag-pill tag-pill-cyan text-[10px]">
            ✦ Circular Packaging Standards
          </span>
          <h3 className="text-2xl font-bold text-white tracking-tight">
            Polymer Circularity & Municipal Streams
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs font-sans">
          <div className="p-6 rounded-3xl bg-white/[0.03] border border-[#34d399]/30 hover:border-[#34d399]/60 transition-all">
            <span className="tag-pill tag-pill-emerald text-[9px] mb-3">
              Code 4 & 5 (Mono-Polyolefins)
            </span>
            <h4 className="text-lg font-bold text-white mt-1 mb-2">PE & PP Single Stream</h4>
            <p className="text-slate-300 leading-relaxed text-xs">
              High recyclability in municipal recovery markets. CEFLEX design guidelines prioritize mono-PE/PP over complex mixed polymer multilayers.
            </p>
          </div>

          <div className="p-6 rounded-3xl bg-white/[0.03] border border-[#22d3ee]/30 hover:border-[#22d3ee]/60 transition-all">
            <span className="tag-pill tag-pill-cyan text-[9px] mb-3">
              Certified Biopolymers
            </span>
            <h4 className="text-lg font-bold text-white mt-1 mb-2">PLA / PBAT / PHA Blends</h4>
            <p className="text-slate-300 leading-relaxed text-xs">
              Compostable within 90-180 days under industrial composting (ASTM D6400 / EN 13432). Natural breathability ideal for organic fresh produce.
            </p>
          </div>

          <div className="p-6 rounded-3xl bg-white/[0.03] border border-white/10 hover:border-white/25 transition-all">
            <span className="tag-pill tag-pill-pink text-[9px] mb-3">
              Code 7 (Multilayer Laminates)
            </span>
            <h4 className="text-lg font-bold text-white mt-1 mb-2">Met-PET & Foil Composites</h4>
            <p className="text-slate-300 leading-relaxed text-xs">
              Unsurpassed barrier performance (OTR &lt; 0.1), but non-separable layers require pyrolysis or specialized delamination facilities.
            </p>
          </div>
        </div>
      </div>

    </div>
  );
};
