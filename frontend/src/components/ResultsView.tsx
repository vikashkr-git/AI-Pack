import React, { useState } from 'react';
import { 
  Award, 
  CheckCircle2, 
  Leaf, 
  Info, 
  Wind, 
  Sparkles,
  Layers,
  ShoppingBag,
  Clock,
  ShieldCheck,
  ClipboardCheck,
  ExternalLink,
  Maximize2,
  X,
  AlertTriangle,
  ChevronRight,
  MapPin,
  Flame,
  CheckSquare,
  Square,
  BadgePercent
} from 'lucide-react';
import { 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  Radar, 
  ResponsiveContainer,
  Legend,
  Tooltip
} from 'recharts';
import { RecommendationResponse, QualityInspectionPoint } from '../types';

interface ResultsViewProps {
  results: RecommendationResponse;
  onNavigateToCompare: () => void;
  onNavigateToSustainability: () => void;
}

type ActiveTab = 'overview' | 'anatomy' | 'sourcing' | 'durability' | 'inspection';

export const ResultsView: React.FC<ResultsViewProps> = ({
  results,
  onNavigateToCompare,
  onNavigateToSustainability
}) => {
  const top1 = results.top_recommendations[0];
  const top2 = results.top_recommendations[1];
  const top3 = results.top_recommendations[2];
  const req = results.scientific_requirements;

  // Active Tab for Top Choice
  const [activeTab, setActiveTab] = useState<ActiveTab>('overview');

  // Lightbox Modal for Sample Photo
  const [lightboxImage, setLightboxImage] = useState<{ url: string; title: string; subtitle: string } | null>(null);

  // Interactive Quality Inspection Checklist State
  const initialChecked: Record<string, boolean> = {};
  top1?.quality_inspection_checklist?.forEach((item, idx) => {
    initialChecked[`top1-${idx}`] = false;
  });
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean>>(initialChecked);

  const toggleCheckItem = (key: string) => {
    setCheckedItems(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const checklist = top1?.quality_inspection_checklist || [];
  const checkedCount = checklist.filter((_, idx) => checkedItems[`top1-${idx}`]).length;

  // Format Radar Data
  const radarData = [
    {
      subject: 'Oxygen Barrier',
      Top1: top1?.explanation.radar_metrics.oxygen_barrier || 50,
      Top2: top2?.explanation.radar_metrics.oxygen_barrier || 40,
    },
    {
      subject: 'Moisture Barrier',
      Top1: top1?.explanation.radar_metrics.moisture_barrier || 50,
      Top2: top2?.explanation.radar_metrics.moisture_barrier || 40,
    },
    {
      subject: 'Mechanical Strength',
      Top1: top1?.explanation.radar_metrics.mechanical_strength || 50,
      Top2: top2?.explanation.radar_metrics.mechanical_strength || 40,
    },
    {
      subject: 'Thermal Stability',
      Top1: top1?.explanation.radar_metrics.thermal_stability || 50,
      Top2: top2?.explanation.radar_metrics.thermal_stability || 40,
    },
    {
      subject: 'Sustainability',
      Top1: top1?.explanation.radar_metrics.sustainability || 50,
      Top2: top2?.explanation.radar_metrics.sustainability || 40,
    },
    {
      subject: 'Cost Efficiency',
      Top1: top1?.explanation.radar_metrics.cost_efficiency || 50,
      Top2: top2?.explanation.radar_metrics.cost_efficiency || 40,
    },
  ];

  return (
    <div className="space-y-10 max-w-6xl mx-auto animate-fade-in-up py-4 font-sans">
      
      {/* FRESH PRODUCE RESPIRATION BANNER */}
      {req.is_fresh_produce && (
        <div className="p-6 sm:p-8 rounded-[32px] bg-gradient-to-r from-emerald-950/40 via-teal-950/30 to-slate-900/60 border border-emerald-500/30 shadow-xl relative overflow-hidden">
          <div className="flex items-start space-x-5">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 flex-shrink-0 animate-pulse">
              <Wind className="w-6 h-6 stroke-[2.2]" />
            </div>
            <div className="space-y-2">
              <div className="flex flex-wrap items-center gap-3">
                <span className="text-xl font-bold text-white tracking-tight">
                  Fresh Produce Respiration Regime Active
                </span>
                <span className="tag-pill tag-pill-emerald text-[10px]">
                  {req.map_recommendations.respiration_severity} ({req.map_recommendations.respiration_rate_mg_co2_kg_hr} mg CO₂/kg·hr)
                </span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed font-sans">
                {req.map_recommendations.scientific_rationale}
              </p>
              {req.map_recommendations.recommended_headspace_gas && (
                <div className="pt-2 flex flex-wrap items-center gap-2 text-xs">
                  <span className="font-semibold text-slate-400">Recommended Equilibrium MAP Gas:</span>
                  <span className="font-mono bg-black/50 px-3 py-1 rounded-full border border-emerald-500/30 text-emerald-300 font-bold">
                    {req.map_recommendations.recommended_headspace_gas}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* TOP 1 BEST RECOMMENDATION CHAMPION CARD */}
      <div className="glass-luxury rounded-[36px] p-6 sm:p-10 relative overflow-hidden border border-white/15 shadow-2xl">
        
        {/* Soft Radial Ambient Glow */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-[#ffd905]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-[#ff64d5]/10 rounded-full blur-3xl pointer-events-none" />

        {/* Top Header Row with Photo Preview and Score */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8 pb-8 border-b border-white/10 relative z-10">
          
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
            {/* Sample Photo Thumbnail with Zoom Trigger */}
            <div 
              onClick={() => setLightboxImage({
                url: top1.sample_photo_url || '/packaging/met_pet_pe.jpg',
                title: top1.name,
                subtitle: top1.structure
              })}
              className="relative group cursor-pointer w-28 h-28 sm:w-36 sm:h-36 rounded-3xl overflow-hidden border-2 border-[#ffd905]/40 hover:border-[#ffd905] shadow-[0_0_20px_rgba(255,217,5,0.2)] flex-shrink-0 transition-all duration-300 bg-slate-900"
            >
              <img 
                src={top1.sample_photo_url || '/packaging/met_pet_pe.jpg'} 
                alt={top1.name} 
                className="w-full h-full object-cover object-center group-hover:scale-108 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex flex-col justify-end p-2.5 opacity-90 group-hover:opacity-100 transition-opacity">
                <span className="text-[9px] font-bold text-[#ffd905] flex items-center gap-1 uppercase tracking-wider">
                  <Maximize2 className="w-3 h-3" /> Sample Photo
                </span>
              </div>
            </div>

            <div>
              <div className="flex flex-wrap items-center gap-2.5 mb-2.5">
                <span className="tag-pill tag-pill-yellow text-xs py-1 px-3.5 flex items-center gap-1.5 font-bold">
                  <Sparkles className="w-3.5 h-3.5" /> Top #1 AI Match
                </span>
                <span className="tag-pill tag-pill-pink text-[10px]">
                  {top1.category}
                </span>
                {top1.procurement_market?.estimated_cost_per_kg_inr && (
                  <span className="tag-pill tag-pill-cyan text-[10px] font-mono">
                    {top1.procurement_market.estimated_cost_per_kg_inr}
                  </span>
                )}
              </div>
              
              <h2 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
                {top1.name}
              </h2>
              
              <p className="text-xs sm:text-sm text-[#ffd905] font-mono mt-2.5 flex flex-wrap items-center gap-2">
                <span className="font-semibold uppercase tracking-wider text-[11px] bg-white/10 px-2.5 py-0.5 rounded-full border border-white/15">
                  Structure
                </span>
                <span className="text-slate-200">{top1.structure}</span>
              </p>
            </div>
          </div>

          {/* Large Suitability Score Pill */}
          <div className="flex items-center space-x-5 bg-white/[0.04] p-5 rounded-3xl border border-white/12 shadow-xl flex-shrink-0">
            <div className="text-right">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 block">
                AI Match Score
              </span>
              <span className="text-xs text-[#34d399] font-bold flex items-center justify-end font-mono mt-0.5">
                <span className="w-2 h-2 rounded-full bg-[#34d399] mr-1.5 animate-ping" />
                {results.confidence_assessment.overall_confidence}
              </span>
            </div>

            <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-[#ffd905] to-[#f5b700] p-0.5 shadow-[0_0_25px_rgba(255,217,5,0.4)]">
              <div className="w-full h-full bg-[#080d19] rounded-[14px] flex flex-col items-center justify-center">
                <span className="text-3xl font-extrabold text-[#ffd905] leading-none">{top1.suitability_score}</span>
                <span className="text-[10px] font-mono text-slate-400 mt-0.5">/ 100</span>
              </div>
            </div>
          </div>
        </div>

        {/* INTERACTIVE NAVIGATION TABS */}
        <div className="flex items-center space-x-2 sm:space-x-3 overflow-x-auto py-5 border-b border-white/10 relative z-10 no-scrollbar">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-4 py-2 rounded-2xl text-xs font-bold transition-all flex items-center space-x-2 cursor-pointer whitespace-nowrap ${
              activeTab === 'overview'
                ? 'bg-[#ffd905] text-slate-950 shadow-md shadow-[#ffd905]/20'
                : 'bg-white/[0.05] text-slate-300 hover:bg-white/[0.1] hover:text-white'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Specifications & XAI</span>
          </button>

          <button
            onClick={() => setActiveTab('anatomy')}
            className={`px-4 py-2 rounded-2xl text-xs font-bold transition-all flex items-center space-x-2 cursor-pointer whitespace-nowrap ${
              activeTab === 'anatomy'
                ? 'bg-[#ffd905] text-slate-950 shadow-md shadow-[#ffd905]/20'
                : 'bg-white/[0.05] text-slate-300 hover:bg-white/[0.1] hover:text-white'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Material Anatomy & "Why Only This"</span>
          </button>

          <button
            onClick={() => setActiveTab('sourcing')}
            className={`px-4 py-2 rounded-2xl text-xs font-bold transition-all flex items-center space-x-2 cursor-pointer whitespace-nowrap ${
              activeTab === 'sourcing'
                ? 'bg-[#ffd905] text-slate-950 shadow-md shadow-[#ffd905]/20'
                : 'bg-white/[0.05] text-slate-300 hover:bg-white/[0.1] hover:text-white'
            }`}
          >
            <ShoppingBag className="w-3.5 h-3.5" />
            <span>Nearby Markets & Cost</span>
          </button>

          <button
            onClick={() => setActiveTab('durability')}
            className={`px-4 py-2 rounded-2xl text-xs font-bold transition-all flex items-center space-x-2 cursor-pointer whitespace-nowrap ${
              activeTab === 'durability'
                ? 'bg-[#ffd905] text-slate-950 shadow-md shadow-[#ffd905]/20'
                : 'bg-white/[0.05] text-slate-300 hover:bg-white/[0.1] hover:text-white'
            }`}
          >
            <Clock className="w-3.5 h-3.5" />
            <span>Lifespan & Protection Duration</span>
          </button>

          <button
            onClick={() => setActiveTab('inspection')}
            className={`px-4 py-2 rounded-2xl text-xs font-bold transition-all flex items-center space-x-2 cursor-pointer whitespace-nowrap ${
              activeTab === 'inspection'
                ? 'bg-[#ffd905] text-slate-950 shadow-md shadow-[#ffd905]/20'
                : 'bg-white/[0.05] text-slate-300 hover:bg-white/[0.1] hover:text-white'
            }`}
          >
            <ClipboardCheck className="w-3.5 h-3.5" />
            <span>Pre-Receiving Quality Checklist</span>
            {checklist.length > 0 && (
              <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-mono font-bold ${
                checkedCount === checklist.length ? 'bg-emerald-400 text-slate-950' : 'bg-white/20 text-white'
              }`}>
                {checkedCount}/{checklist.length}
              </span>
            )}
          </button>
        </div>

        {/* TAB 1: OVERVIEW & BARRIER SPECIFICATIONS */}
        {activeTab === 'overview' && (
          <div className="space-y-8 pt-8 relative z-10 animate-fade-in-up">
            
            {/* 4 Technical Specification Tiles */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-5 rounded-3xl bg-white/[0.03] border border-white/10 hover:border-[#ffd905]/40 transition-all">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">Oxygen Barrier (OTR)</span>
                <div className="text-2xl font-extrabold text-white tracking-tight">{top1.technical_specifications.otr_value}</div>
                <span className="text-xs text-[#ffd905] font-mono mt-1 block">{top1.technical_specifications.otr_unit}</span>
              </div>

              <div className="p-5 rounded-3xl bg-white/[0.03] border border-white/10 hover:border-[#ff64d5]/40 transition-all">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">Moisture Barrier (WVTR)</span>
                <div className="text-2xl font-extrabold text-white tracking-tight">{top1.technical_specifications.wvtr_value}</div>
                <span className="text-xs text-[#ff64d5] font-mono mt-1 block">{top1.technical_specifications.wvtr_unit}</span>
              </div>

              <div className="p-5 rounded-3xl bg-white/[0.03] border border-white/10 hover:border-[#22d3ee]/40 transition-all">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">Film Gauge</span>
                <div className="text-2xl font-extrabold text-white tracking-tight">{top1.technical_specifications.thickness_um} µm</div>
                <span className="text-xs text-slate-400 font-mono mt-1 block">Dart: {top1.technical_specifications.puncture_resistance_n} N</span>
              </div>

              <div className="p-5 rounded-3xl bg-white/[0.03] border border-white/10 hover:border-[#34d399]/40 transition-all">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">Recyclability Stream</span>
                <div className="text-2xl font-extrabold text-[#34d399] tracking-tight">{top1.sustainability_profile.recyclability_stream || 'Code 7'}</div>
                <span className="text-xs text-slate-400 font-mono mt-1 block">{top1.sustainability_profile.recyclability_class || 'Standard Multilayer'}</span>
              </div>
            </div>

            {/* Explainable AI Selection Rationale */}
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <span className="tag-pill tag-pill-pink text-[10px]">
                  ★ Scientific Selection Rationale
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {top1.explanation.reasons_why.map((reason, idx) => (
                  <div key={idx} className="flex items-start space-x-3.5 text-xs sm:text-sm text-slate-200 bg-white/[0.03] p-4 rounded-2xl border border-white/10">
                    <CheckCircle2 className="w-5 h-5 text-[#34d399] flex-shrink-0 mt-0.5 stroke-[2.2]" />
                    <span className="leading-relaxed">{reason}</span>
                  </div>
                ))}
              </div>

              {top1.explanation.cautions_limitations.length > 0 && (
                <div className="mt-6 p-5 rounded-3xl bg-amber-500/10 border border-amber-500/25">
                  <span className="text-xs font-bold text-amber-300 block mb-2 uppercase tracking-wider">
                    Engineering Considerations & Trade-Offs:
                  </span>
                  <ul className="space-y-2 text-xs text-slate-300 font-sans">
                    {top1.explanation.cautions_limitations.map((c, idx) => (
                      <li key={idx} className="flex items-center space-x-2.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-400 flex-shrink-0" />
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: MATERIAL ANATOMY & WHY ONLY THIS MATERIAL */}
        {activeTab === 'anatomy' && (
          <div className="space-y-8 pt-8 relative z-10 animate-fade-in-up">
            
            {/* "Why Only This Material" Scientific Callout */}
            <div className="p-6 rounded-3xl bg-gradient-to-r from-amber-500/15 via-[#ffd905]/10 to-transparent border border-[#ffd905]/30">
              <div className="flex items-start space-x-4">
                <div className="w-10 h-10 rounded-2xl bg-[#ffd905]/20 border border-[#ffd905]/40 flex items-center justify-center text-[#ffd905] flex-shrink-0 font-bold">
                  ★
                </div>
                <div className="space-y-1.5">
                  <h4 className="text-base font-bold text-white tracking-tight">
                    Why Only This Specific Material Structure?
                  </h4>
                  <p className="text-sm text-amber-100/90 leading-relaxed">
                    {top1.material_composition?.why_this_material_short || 
                     "This multi-layer co-extrusion is engineered to combine tensile print stability, an impermeable gas/moisture shield, and low-temperature fusion sealing without excessive package weight."}
                  </p>
                </div>
              </div>
            </div>

            {/* Layer-by-Layer Visual Stack Diagram */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                  <Layers className="w-4 h-4 text-[#22d3ee]" />
                  Microscopic Layer-by-Layer Production Architecture
                </span>
                <span className="text-xs font-mono text-slate-400">
                  Total Gauge: {top1.technical_specifications.thickness_um} µm
                </span>
              </div>

              <div className="space-y-3">
                {top1.material_composition?.layers?.map((layer, idx) => (
                  <div 
                    key={idx}
                    className="p-4 sm:p-5 rounded-2xl bg-white/[0.04] border border-white/10 hover:border-[#22d3ee]/40 transition-all flex flex-col md:flex-row md:items-center justify-between gap-4"
                  >
                    <div className="flex items-start space-x-4">
                      <div className="w-8 h-8 rounded-xl bg-[#22d3ee]/20 text-[#22d3ee] font-mono font-bold flex items-center justify-center text-xs flex-shrink-0 mt-0.5">
                        L{layer.layer_no}
                      </div>
                      <div className="space-y-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="text-sm font-bold text-white">{layer.name}</span>
                          {layer.position && (
                            <span className="text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-slate-300 font-mono">
                              {layer.position}
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-slate-300 leading-relaxed">
                          <strong className="text-[#ffd905]">Functional Work:</strong> {layer.work || layer.function}
                        </p>
                      </div>
                    </div>

                    <div className="text-right flex-shrink-0 md:pl-4 border-t md:border-t-0 md:border-l border-white/10 pt-2 md:pt-0">
                      <span className="text-xs text-slate-400 block font-mono">Thickness</span>
                      <span className="text-base font-extrabold text-[#22d3ee] font-mono">
                        {layer.thickness_um} µm
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        )}

        {/* TAB 3: NEARBY MARKETPLACE AVAILABILITY & COST ESTIMATOR */}
        {activeTab === 'sourcing' && (
          <div className="space-y-8 pt-8 relative z-10 animate-fade-in-up">
            
            {/* Cost Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              <div className="p-6 rounded-3xl bg-gradient-to-br from-emerald-950/30 to-slate-900/60 border border-emerald-500/30">
                <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider block mb-1">
                  Estimated Bulk Rollstock Cost
                </span>
                <div className="text-2xl sm:text-3xl font-extrabold text-white font-mono tracking-tight">
                  {top1.procurement_market?.estimated_cost_per_kg_inr || "₹270 – ₹350 / kg"}
                </div>
                <span className="text-xs text-slate-400 font-mono mt-1 block">
                  Approx. {top1.procurement_market?.approx_cost_usd || "$3.25 – $4.20 / kg"}
                </span>
              </div>

              <div className="p-6 rounded-3xl bg-gradient-to-br from-cyan-950/30 to-slate-900/60 border border-cyan-500/30">
                <span className="text-xs font-semibold text-cyan-400 uppercase tracking-wider block mb-1">
                  Finished Pouch Unit Cost
                </span>
                <div className="text-2xl sm:text-3xl font-extrabold text-white font-mono tracking-tight">
                  {top1.procurement_market?.estimated_cost_per_pouch_inr || "₹1.60 – ₹2.80 / pouch"}
                </div>
                <span className="text-xs text-slate-400 font-mono mt-1 block">
                  Based on 200g–500g standardized format
                </span>
              </div>

              <div className="p-6 rounded-3xl bg-gradient-to-br from-amber-950/30 to-slate-900/60 border border-amber-500/30">
                <span className="text-xs font-semibold text-amber-400 uppercase tracking-wider block mb-1">
                  Order Quantity & Lead Time
                </span>
                <div className="text-sm font-bold text-white font-mono">
                  MOQ: {top1.procurement_market?.moq || "1,500 pouches"}
                </div>
                <span className="text-xs text-amber-200/80 font-mono mt-1 block">
                  Lead Time: {top1.procurement_market?.lead_time || "3–5 days (Stock)"}
                </span>
              </div>
            </div>

            {/* Sourcing Channels & Industrial Marketplace Hubs */}
            <div className="p-6 rounded-3xl bg-white/[0.03] border border-white/10 space-y-4">
              <div className="flex items-center space-x-2">
                <MapPin className="w-5 h-5 text-[#ffd905]" />
                <h4 className="text-base font-bold text-white tracking-tight">
                  Where to Source in Near-By Marketplaces (India & Regional Hubs)
                </h4>
              </div>
              <p className="text-xs text-slate-300 font-sans">
                Packaging materials can be procured directly from primary film extruders, pouch converters, or online B2B industrial hubs:
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                {top1.procurement_market?.sourcing_channels?.map((channel, idx) => (
                  <div 
                    key={idx}
                    className="p-3.5 rounded-2xl bg-white/[0.04] border border-white/10 hover:border-[#ffd905]/40 transition-all flex items-center justify-between text-xs text-slate-200"
                  >
                    <div className="flex items-center space-x-2.5">
                      <span className="w-2 h-2 rounded-full bg-[#ffd905]" />
                      <span className="font-medium">{channel}</span>
                    </div>
                    <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
                  </div>
                ))}
              </div>
            </div>

          </div>
        )}

        {/* TAB 4: MATERIAL LIFESPAN & FOOD PROTECTION DURATION */}
        {activeTab === 'durability' && (
          <div className="space-y-8 pt-8 relative z-10 animate-fade-in-up">
            
            {/* Two Duration Meters Side-by-Side */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Meter 1: Virgin Unfilled Shelf Life */}
              <div className="p-6 rounded-3xl bg-gradient-to-br from-blue-950/40 via-slate-900/60 to-slate-900/60 border border-blue-500/30 space-y-3">
                <div className="flex items-center space-x-2.5 text-blue-400 text-xs font-bold uppercase tracking-wider">
                  <Clock className="w-4 h-4" />
                  <span>Unfilled Material Warehouse Lifespan</span>
                </div>
                <div className="text-2xl font-extrabold text-white tracking-tight">
                  {top1.material_durability?.virgin_material_shelf_life || "18 – 24 Months"}
                </div>
                <p className="text-xs text-slate-300 leading-relaxed font-sans">
                  The packaging rollstock or pre-formed pouches can be safely stored in the warehouse before filling without structural degradation.
                </p>
                {top1.material_durability?.unfilled_storage_conditions && (
                  <div className="pt-2 border-t border-white/10 text-xs text-slate-400">
                    <strong className="text-blue-300">Optimal Warehouse Climate:</strong> {top1.material_durability.unfilled_storage_conditions}
                  </div>
                )}
              </div>

              {/* Meter 2: Packaged Product Protection Shelf Life */}
              <div className="p-6 rounded-3xl bg-gradient-to-br from-emerald-950/40 via-slate-900/60 to-slate-900/60 border border-emerald-500/30 space-y-3">
                <div className="flex items-center space-x-2.5 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                  <ShieldCheck className="w-4 h-4" />
                  <span>Packaged Commodity Preservation Duration</span>
                </div>
                <div className="text-2xl font-extrabold text-white tracking-tight">
                  {top1.material_durability?.packaged_product_protection_duration || 
                   `Guarantees ${results.query_summary.target_shelf_life_days} Days preservation under ${results.query_summary.storage_type} storage`}
                </div>
                <p className="text-xs text-slate-300 leading-relaxed font-sans">
                  Protects {results.query_summary.commodity} against moisture gain, lipid rancidity, and flavor degradation under {results.query_summary.storage_type} climate.
                </p>
                {top1.material_durability?.aging_failure_modes && (
                  <div className="pt-2 border-t border-white/10 text-xs text-slate-400">
                    <strong className="text-emerald-300">Aging Risk Factors:</strong> {top1.material_durability.aging_failure_modes}
                  </div>
                )}
              </div>

            </div>

          </div>
        )}

        {/* TAB 5: PRE-RECEIVING QUALITY INSPECTION CHECKLIST */}
        {activeTab === 'inspection' && (
          <div className="space-y-6 pt-8 relative z-10 animate-fade-in-up">
            
            {/* Header & Verification Progress Banner */}
            <div className="p-5 rounded-3xl bg-white/[0.04] border border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h4 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                  <ClipboardCheck className="w-5 h-5 text-[#ffd905]" />
                  Receiving Dock Inspection Protocol (Pre-Acceptance Verification)
                </h4>
                <p className="text-xs text-slate-300 mt-1 font-sans">
                  Perform these 5 physical quality tests before signing supplier delivery receipts to prevent packaging line jams and food spoilage:
                </p>
              </div>

              <div className="flex items-center space-x-3 flex-shrink-0">
                <div className="text-right">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">QA Status</span>
                  <span className={`text-xs font-bold font-mono ${
                    checkedCount === checklist.length ? 'text-emerald-400' : 'text-amber-400'
                  }`}>
                    {checkedCount} of {checklist.length} Inspected
                  </span>
                </div>
                <div className={`w-10 h-10 rounded-2xl flex items-center justify-center font-bold text-xs ${
                  checkedCount === checklist.length 
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                    : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                }`}>
                  {Math.round((checkedCount / Math.max(checklist.length, 1)) * 100)}%
                </div>
              </div>
            </div>

            {/* Checklist Items */}
            <div className="space-y-3.5">
              {checklist.map((item, idx) => {
                const key = `top1-${idx}`;
                const isChecked = !!checkedItems[key];

                return (
                  <div 
                    key={idx}
                    onClick={() => toggleCheckItem(key)}
                    className={`p-4 sm:p-5 rounded-2xl border transition-all cursor-pointer select-none ${
                      isChecked 
                        ? 'bg-emerald-950/20 border-emerald-500/40 shadow-sm'
                        : 'bg-white/[0.02] border-white/10 hover:border-white/20'
                    }`}
                  >
                    <div className="flex items-start space-x-3.5">
                      <button 
                        type="button"
                        className="mt-0.5 text-xl flex-shrink-0 transition-transform active:scale-90"
                      >
                        {isChecked ? (
                          <CheckSquare className="w-5 h-5 text-emerald-400" />
                        ) : (
                          <Square className="w-5 h-5 text-slate-400 hover:text-white" />
                        )}
                      </button>

                      <div className="space-y-1.5 flex-1">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <span className={`text-sm font-bold ${isChecked ? 'text-emerald-300 line-through' : 'text-white'}`}>
                            {item.check_item}
                          </span>
                          <div className="flex items-center space-x-2">
                            {item.standard && (
                              <span className="text-[10px] font-mono bg-white/10 px-2 py-0.5 rounded-full text-slate-300">
                                {item.standard}
                              </span>
                            )}
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${
                              item.criticality === 'Critical' ? 'bg-red-500/20 text-red-300 border border-red-500/30' : 'bg-amber-500/20 text-amber-300'
                            }`}>
                              {item.criticality}
                            </span>
                          </div>
                        </div>

                        <p className="text-xs text-slate-300 font-sans">
                          <strong className="text-slate-200">Acceptance Standard:</strong> {item.acceptance_criteria}
                        </p>

                        <p className="text-xs text-[#ffd905]/90 font-mono">
                          <strong>Test Protocol:</strong> {item.how_to_test}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

          </div>
        )}

      </div>

      {/* RADAR CHART & ALTERNATIVES GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Radar Chart (5 cols) */}
        <div className="lg:col-span-5 glass-luxury rounded-[36px] p-8 border border-white/15 flex flex-col justify-between">
          <div>
            <span className="tag-pill tag-pill-yellow text-[10px] mb-3">
              ✦ Multi-Dimensional Indices
            </span>
            <h3 className="text-2xl font-bold text-white tracking-tight mb-1">Barrier Balance Radar</h3>
            <p className="text-xs text-slate-300 mb-6 font-sans">
              Compares Top Pick (Gold) vs Runner-Up (Pink) across 6 physical criteria.
            </p>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255, 255, 255, 0.15)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#cbd5e1', fontSize: 10, fontWeight: 500 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} stroke="rgba(255, 255, 255, 0.15)" />
                <Radar name={top1.short_name} dataKey="Top1" stroke="#ffd905" fill="#ffd905" fillOpacity={0.35} />
                {top2 && (
                  <Radar name={top2.short_name} dataKey="Top2" stroke="#ff64d5" fill="#ff64d5" fillOpacity={0.25} />
                )}
                <Tooltip contentStyle={{ backgroundColor: '#090e1a', borderColor: '#ffd905', borderRadius: '16px', fontSize: '11px', color: '#fff' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="pt-5 border-t border-white/10 text-xs font-mono text-slate-400 flex justify-between">
            <span>Model: {results.confidence_assessment.model_version}</span>
            <span>Analyzed: {results.confidence_assessment.empirical_measurements_analyzed} materials</span>
          </div>
        </div>

        {/* Runner-Up Alternatives (7 cols) */}
        <div className="lg:col-span-7 space-y-5">
          <div className="flex items-center justify-between px-1">
            <span className="text-sm font-bold text-white tracking-wide">Candidate Alternatives</span>
            <button
              onClick={onNavigateToCompare}
              className="text-xs font-bold text-[#ffd905] hover:underline cursor-pointer flex items-center space-x-1"
            >
              <span>3-Way Side-by-Side Comparison →</span>
            </button>
          </div>

          {[top2, top3].filter(Boolean).map((alt) => (
            <div key={alt.id} className="p-6 rounded-[28px] bg-white/[0.03] border border-white/12 hover:border-white/25 transition-all">
              <div className="flex items-start justify-between gap-4 mb-3">
                <div className="flex items-start space-x-4">
                  {alt.sample_photo_url && (
                    <img 
                      src={alt.sample_photo_url} 
                      alt={alt.name}
                      onClick={() => setLightboxImage({
                        url: alt.sample_photo_url || '',
                        title: alt.name,
                        subtitle: alt.structure
                      })}
                      className="w-16 h-16 rounded-2xl object-cover border border-white/20 cursor-pointer hover:scale-105 transition-transform flex-shrink-0" 
                    />
                  )}
                  <div>
                    <div className="flex items-center space-x-2.5">
                      <span className="tag-pill tag-pill-yellow text-[9px] py-0 px-2 font-mono">
                        Rank #{alt.rank}
                      </span>
                      <span className="text-base sm:text-lg font-bold text-white">{alt.name}</span>
                    </div>
                    <span className="text-xs text-slate-400 font-mono mt-1 block">{alt.structure}</span>
                    {alt.procurement_market?.estimated_cost_per_kg_inr && (
                      <span className="text-[11px] font-mono text-emerald-400 mt-1 block">
                        Cost: {alt.procurement_market.estimated_cost_per_kg_inr}
                      </span>
                    )}
                  </div>
                </div>

                <div className="px-3.5 py-1.5 rounded-full bg-white/[0.08] text-sm font-bold text-[#ffd905] font-mono flex-shrink-0">
                  {alt.suitability_score} / 100
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3 py-3 border-y border-white/10 my-3 text-xs font-mono">
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase">OTR</span>
                  <span className="font-bold text-white">{alt.technical_specifications.otr_value}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase">WVTR</span>
                  <span className="font-bold text-white">{alt.technical_specifications.wvtr_value}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase">Gauge</span>
                  <span className="font-bold text-white">{alt.technical_specifications.thickness_um} µm</span>
                </div>
              </div>

              <div className="space-y-1.5">
                {alt.explanation.reasons_why.slice(0, 2).map((r, i) => (
                  <p key={i} className="text-xs text-slate-300 flex items-center space-x-2 font-sans">
                    <CheckCircle2 className="w-3.5 h-3.5 text-[#34d399] flex-shrink-0" />
                    <span>{r}</span>
                  </p>
                ))}
              </div>
            </div>
          ))}

          {/* Sustainable Alternative Callout */}
          {results.sustainable_alternative && (
            <div
              onClick={onNavigateToSustainability}
              className="p-5 rounded-[28px] bg-gradient-to-r from-emerald-950/30 to-slate-900/60 border border-emerald-500/30 flex items-center justify-between cursor-pointer hover:border-emerald-500/60 transition-all shadow-md"
            >
              <div className="flex items-center space-x-4">
                {results.sustainable_alternative.sample_photo_url && (
                  <img 
                    src={results.sustainable_alternative.sample_photo_url} 
                    alt="Eco Alternative" 
                    className="w-12 h-12 rounded-xl object-cover border border-emerald-500/40 flex-shrink-0"
                  />
                )}
                <div>
                  <span className="text-xs font-bold text-emerald-300 block uppercase tracking-wider">
                    Eco-Friendly Alternative Available
                  </span>
                  <span className="text-sm text-white font-medium">
                    {results.sustainable_alternative.name} ({results.sustainable_alternative.suitability_score}/100)
                  </span>
                  {results.sustainable_alternative.procurement_market?.estimated_cost_per_kg_inr && (
                    <span className="text-[11px] font-mono text-emerald-300 block mt-0.5">
                      Approx. {results.sustainable_alternative.procurement_market.estimated_cost_per_kg_inr}
                    </span>
                  )}
                </div>
              </div>
              <button className="btn-luxury-glass px-4 py-2 text-xs font-bold text-emerald-300">
                Eco Profile →
              </button>
            </div>
          )}

        </div>

      </div>

      {/* Decision-Support Scientific Disclaimer */}
      <div className="p-5 rounded-3xl bg-white/[0.03] border border-white/10 text-xs text-slate-400 flex items-start space-x-3.5">
        <Info className="w-5 h-5 text-[#ffd905] flex-shrink-0 mt-0.5" />
        <p className="leading-relaxed font-sans text-xs">
          <span className="font-bold text-slate-300 uppercase tracking-wider">Decision-Support Notice: </span>
          {results.disclaimer}
        </p>
      </div>

      {/* LIGHTBOX PHOTO MODAL */}
      {lightboxImage && (
        <div 
          onClick={() => setLightboxImage(null)}
          className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-8 bg-black/85 backdrop-blur-xl animate-fade-in-up"
        >
          <div 
            onClick={e => e.stopPropagation()}
            className="bg-[#090e1a] border border-white/20 rounded-[36px] overflow-hidden max-w-2xl w-full text-white shadow-2xl relative"
          >
            <div className="relative aspect-square w-full bg-black/60 flex items-center justify-center overflow-hidden">
              <img 
                src={lightboxImage.url} 
                alt={lightboxImage.title} 
                className="w-full h-full object-contain"
              />
              <button
                onClick={() => setLightboxImage(null)}
                className="absolute top-4 right-4 w-10 h-10 rounded-full bg-black/60 hover:bg-black/80 border border-white/20 flex items-center justify-center text-white cursor-pointer transition-all"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-6 border-t border-white/10 space-y-1.5">
              <h3 className="text-xl font-bold text-white tracking-tight">{lightboxImage.title}</h3>
              <p className="text-xs text-[#ffd905] font-mono">{lightboxImage.subtitle}</p>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
