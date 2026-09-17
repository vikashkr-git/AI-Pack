import React from 'react';
import { 
  Sparkles, 
  ArrowRight, 
  Apple, 
  Flame, 
  Coffee, 
  ThermometerSnowflake, 
  Layers, 
  ShieldCheck, 
  Cpu, 
  Activity,
  Zap
} from 'lucide-react';
import { FoodInputFormState } from '../types';

interface HeroSectionProps {
  onSelectPreset: (preset: FoodInputFormState) => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({ onSelectPreset }) => {
  const telemetryStats = [
    { label: "Calibrated Samples", value: "18,000+", sub: "Out-of-Distribution Tested", icon: Cpu, color: "text-[#22d3ee]" },
    { label: "Barrier Structures", value: "15+ Multilayer", sub: "ASTM D3985 / F1249", icon: Layers, color: "text-[#ffd905]" },
    { label: "Generalization R²", value: "0.997 Score", sub: "Zero Target Leakage", icon: Activity, color: "text-[#ff64d5]" },
    { label: "Mass Transfer Engine", value: "Arrhenius Equations", sub: "Coulometric Permeabilities", icon: ShieldCheck, color: "text-[#34d399]" },
  ];

  const demoPresets: Array<{
    title: string;
    category: string;
    icon: React.ReactNode;
    cardClass: string;
    badgeClass: string;
    badgeText: string;
    accentColor: string;
    metrics: string[];
    description: string;
    params: FoodInputFormState;
  }> = [
    {
      title: "Fresh Tomato",
      category: "Fresh Produce / Respiration",
      icon: <Apple className="w-6 h-6 text-rose-400" />,
      cardClass: "glass-card-pink",
      badgeClass: "tag-pill-pink",
      badgeText: "Respiring Produce",
      accentColor: "#ff64d5",
      metrics: ["18.5 mg CO₂/kg·hr", "Chilled 12°C", "MAP 3-5% O₂"],
      description: "Active respiration mandates equilibrium gas transmission. Hermetic aluminum foil is strictly disbarred by physics rules to avoid anaerobic fermentation.",
      params: {
        commodity: "Tomato",
        category: "Fresh Produce",
        moisture_pct: 94.5,
        fat_pct: 0.2,
        protein_pct: 0.9,
        ph: 4.3,
        respiration_rate: 18.5,
        shelf_life_days: 14,
        storage_temp_c: 12.0,
        relative_humidity_pct: 90.0,
        storage_type: "Chilled",
        transportation: "Refrigerated",
        optimization_goal: "Balanced"
      }
    },
    {
      title: "Potato Chips",
      category: "Lipid Oxidation / Crisp Snack",
      icon: <Flame className="w-6 h-6 text-amber-400" />,
      cardClass: "glass-card-yellow",
      badgeClass: "tag-pill-yellow",
      badgeText: "High Oxidation Risk",
      accentColor: "#ffd905",
      metrics: ["34.5% Fat Content", "2.0% Moisture", "WVTR < 1.0 g/m²·d"],
      description: "Hygroscopic fried snack vulnerable to rancidity and sogginess. AI recommends metallized BOPP/Met-PET barrier structures for dry crispness.",
      params: {
        commodity: "Potato Chips",
        category: "Snacks",
        moisture_pct: 2.0,
        fat_pct: 34.5,
        protein_pct: 6.5,
        ph: 6.2,
        respiration_rate: 0.0,
        shelf_life_days: 180,
        storage_temp_c: 22.0,
        relative_humidity_pct: 50.0,
        storage_type: "Ambient",
        transportation: "Long_Distance",
        optimization_goal: "Balanced"
      }
    },
    {
      title: "Milk Powder",
      category: "Critical Powder Caking",
      icon: <Coffee className="w-6 h-6 text-cyan-400" />,
      cardClass: "glass-card-cyan",
      badgeClass: "tag-pill-cyan",
      badgeText: "Hermetic Moisture Seal",
      accentColor: "#22d3ee",
      metrics: ["aw = 0.22", "365 Days Shelf Life", "OTR < 0.1 cm³/m²·d"],
      description: "Severe irreversible powder caking above aw 0.40. System selects hermetic aluminum foil laminate structure to preserve dry nutritional stability.",
      params: {
        commodity: "Milk Powder",
        category: "Dairy",
        moisture_pct: 3.5,
        fat_pct: 26.5,
        protein_pct: 26.0,
        ph: 6.6,
        respiration_rate: 0.0,
        shelf_life_days: 365,
        storage_temp_c: 22.0,
        relative_humidity_pct: 60.0,
        storage_type: "Ambient",
        transportation: "Long_Distance",
        optimization_goal: "Performance"
      }
    },
    {
      title: "Frozen Peas",
      category: "Cryogenic Sub-Zero",
      icon: <ThermometerSnowflake className="w-6 h-6 text-emerald-400" />,
      cardClass: "glass-card-emerald",
      badgeClass: "tag-pill-emerald",
      badgeText: "Cold-Crack Resistant",
      accentColor: "#34d399",
      metrics: ["Storage -18°C", "Anti-Freezer Burn", "LLDPE Ductility"],
      description: "Sub-zero conditions cause brittle polymer shattering. Recommends ductile, cold-crack resilient metallocene LLDPE/PA copolymer co-extrusion.",
      params: {
        commodity: "Frozen Peas",
        category: "Frozen Vegetable",
        moisture_pct: 79.0,
        fat_pct: 0.5,
        protein_pct: 5.4,
        ph: 6.5,
        respiration_rate: 0.0,
        shelf_life_days: 365,
        storage_temp_c: -18.0,
        relative_humidity_pct: 90.0,
        storage_type: "Frozen",
        transportation: "Refrigerated",
        optimization_goal: "Balanced"
      }
    }
  ];

  return (
    <div className="pt-8 sm:pt-14 pb-12 text-center relative max-w-6xl mx-auto animate-fade-in-up">
      
      {/* Soft Floating Pill Badges */}
      <div className="flex flex-wrap items-center justify-center gap-3 mb-8">
        <span className="tag-pill tag-pill-yellow animate-float-gentle">
          ✦ ASTM Barrier Standards
        </span>
        <span className="tag-pill tag-pill-pink animate-float-slow">
          ★ Grouped Random Forest AI
        </span>
        <span className="tag-pill tag-pill-cyan animate-float-gentle">
          ● Zero Data Leakage
        </span>
      </div>

      {/* Spacious, Grand & Radiant Headline */}
      <div className="max-w-4xl mx-auto mb-6">
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white leading-[1.12] mb-4">
          Intelligent Food Packaging <br />
          <span className="bg-gradient-to-r from-[#ffd905] via-[#ff64d5] to-[#22d3ee] bg-clip-text text-transparent">
            Recommendation System
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed font-normal mt-4">
          An enterprise scientific decision-support system matching food commodities with calibrated barrier films using{' '}
          <span className="text-[#ffd905] font-semibold">mass-transfer equations</span>,{' '}
          <span className="text-[#ff64d5] font-semibold">ASTM empirical permeabilities</span>, and{' '}
          <span className="text-[#22d3ee] font-semibold">GroupKFold machine learning</span>.
        </p>
      </div>

      {/* Spacious Telemetry Stats Matrix */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 max-w-5xl mx-auto mb-16 mt-10 text-left">
        {telemetryStats.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <div 
              key={idx} 
              className="p-5 rounded-3xl bg-slate-900/40 backdrop-blur-xl border border-white/10 hover:border-white/20 transition-all group"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  {stat.label}
                </span>
                <Icon className={`w-4 h-4 ${stat.color} group-hover:scale-110 transition-transform`} />
              </div>
              <div className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
                {stat.value}
              </div>
              <div className="text-xs text-slate-400 font-mono mt-1">
                {stat.sub}
              </div>
            </div>
          );
        })}
      </div>

      {/* Interactive Jury Simulation Scenarios */}
      <div className="max-w-6xl mx-auto text-left">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 px-1 gap-2">
          <div className="flex items-center space-x-2.5">
            <span className="tag-pill tag-pill-yellow text-xs py-1 px-3">
              ⚡ 1-Click Benchmark Demonstrations
            </span>
            <span className="text-xs text-slate-400 hidden md:inline">
              Click any commodity card to run instant AI evaluation
            </span>
          </div>
          <span className="text-xs font-mono text-[#ffd905]">
            Real-time candidate ranking
          </span>
        </div>

        {/* 4 Spacious, Beautiful Benchmark Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {demoPresets.map((preset) => (
            <div
              key={preset.title}
              className={`${preset.cardClass} p-6 sm:p-7 flex flex-col justify-between group cursor-pointer`}
              onClick={() => onSelectPreset(preset.params)}
            >
              <div>
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <span className={`tag-pill ${preset.badgeClass} text-[10px] py-0.5 px-2.5`}>
                    {preset.badgeText}
                  </span>
                  <div className="p-2.5 rounded-2xl bg-white/[0.08] border border-white/10 group-hover:scale-110 transition-transform">
                    {preset.icon}
                  </div>
                </div>

                {/* Title & Category */}
                <h3 className="text-2xl font-bold text-white tracking-tight group-hover:text-[#ffd905] transition-colors mb-1">
                  {preset.title}
                </h3>
                <p className="text-xs text-slate-400 font-medium mb-4">
                  {preset.category}
                </p>

                {/* Spec Pills */}
                <div className="flex flex-wrap gap-1.5 mb-4">
                  {preset.metrics.map((m, i) => (
                    <span key={i} className="text-[10px] font-mono px-2.5 py-1 rounded-full bg-black/40 text-slate-300 border border-white/10">
                      {m}
                    </span>
                  ))}
                </div>

                <p className="text-xs text-slate-300 leading-relaxed mb-6 font-normal">
                  {preset.description}
                </p>
              </div>

              {/* Action Button */}
              <button
                type="button"
                className="w-full py-2.5 px-4 rounded-full text-xs font-bold bg-white/10 hover:bg-white/20 text-white border border-white/15 flex items-center justify-center space-x-2 transition-all group-hover:border-[#ffd905]"
                onClick={(e) => {
                  e.stopPropagation();
                  onSelectPreset(preset.params);
                }}
              >
                <Zap className="w-3.5 h-3.5 text-[#ffd905] fill-current" />
                <span>Run Simulation</span>
                <ArrowRight className="w-3.5 h-3.5 ml-1 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
