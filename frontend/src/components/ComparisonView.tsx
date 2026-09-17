import React from 'react';
import { Scale, Check, X, ShieldCheck, Leaf, DollarSign, Award } from 'lucide-react';
import { RecommendationResponse } from '../types';

interface ComparisonProps {
  results: RecommendationResponse;
}

export const ComparisonView: React.FC<ComparisonProps> = ({ results }) => {
  const candidates = results.top_recommendations;

  if (candidates.length < 2) {
    return (
      <div className="glass-luxury p-16 text-center rounded-[36px] border border-white/15 text-slate-300">
        <span className="text-2xl font-bold text-[#ffd905] block mb-2">No Candidates to Compare</span>
        <p className="text-sm text-slate-400">Run the packaging advisor wizard to generate side-by-side candidate comparison.</p>
      </div>
    );
  }

  const comparisonRows = [
    {
      category: "Predictive Score & Barrier Class",
      items: [
        {
          label: "AI Suitability Score",
          getValue: (c: any) => (
            <span className="text-lg font-extrabold text-[#ffd905] font-mono">
              {c.suitability_score} / 100
            </span>
          )
        },
        {
          label: "Barrier Classification",
          getValue: (c: any) => (
            <span className="tag-pill tag-pill-cyan text-[10px]">
              {c.technical_specifications.otr_class} / {c.technical_specifications.wvtr_class}
            </span>
          )
        }
      ]
    },
    {
      category: "Mass-Transfer Permeability (ASTM D3985 / F1249)",
      items: [
        {
          label: "Oxygen Transmission Rate (OTR)",
          getValue: (c: any) => (
            <span className="font-mono text-sm font-bold text-white">
              {c.technical_specifications.otr_value} <span className="text-xs text-[#ffd905] font-normal">cm³/m²·d·atm</span>
            </span>
          )
        },
        {
          label: "Water Vapor Transmission (WVTR)",
          getValue: (c: any) => (
            <span className="font-mono text-sm font-bold text-white">
              {c.technical_specifications.wvtr_value} <span className="text-xs text-[#ff64d5] font-normal">g/m²·day</span>
            </span>
          )
        },
        {
          label: "Total Film Gauge",
          getValue: (c: any) => (
            <span className="font-mono text-sm text-white font-medium">{c.technical_specifications.thickness_um} µm</span>
          )
        },
        {
          label: "Controlled Gas Breathability",
          getValue: (c: any) => c.technical_specifications.breathable || c.technical_specifications.micro_perforated ? (
            <span className="tag-pill tag-pill-emerald text-[9px]"><Check className="w-3 h-3 mr-1" /> Breathable</span>
          ) : (
            <span className="tag-pill tag-pill-pink text-[9px]"><X className="w-3 h-3 mr-1" /> Hermetic</span>
          )
        }
      ]
    },
    {
      category: "Mechanical Strength & Limits",
      items: [
        {
          label: "Dart Drop Puncture Resistance",
          getValue: (c: any) => (
            <span className="font-mono text-sm text-white font-medium">{c.technical_specifications.puncture_resistance_n || 'N/A'} N</span>
          )
        },
        {
          label: "Heat Seal Temperature Range",
          getValue: (c: any) => (
            <span className="font-mono text-xs text-slate-300">{c.technical_specifications.sealing_temp_range_c || 'N/A'}</span>
          )
        },
        {
          label: "Cold Crack Temp Limit",
          getValue: (c: any) => (
            <span className="font-mono text-xs text-[#22d3ee] font-bold">{c.technical_specifications.min_temperature_c ?? -10}°C</span>
          )
        },
        {
          label: "MAP Gas Flushing Suitability",
          getValue: (c: any) => c.technical_specifications.map_suitable ? (
            <span className="tag-pill tag-pill-emerald text-[9px]"><Check className="w-3 h-3 mr-1" /> Suitable</span>
          ) : (
            <span className="text-slate-400 text-xs font-mono">Standard</span>
          )
        }
      ]
    },
    {
      category: "Circularity & Economy",
      items: [
        {
          label: "Recyclability Stream",
          getValue: (c: any) => (
            <span className="tag-pill tag-pill-emerald text-[10px]">
              {c.sustainability_profile.recyclability_stream || 'Code 7'}
            </span>
          )
        },
        {
          label: "Bio-Based Polymer Content",
          getValue: (c: any) => c.sustainability_profile.compostable || (c.sustainability_profile.bio_based_pct || 0) > 0 ? (
            <span className="font-bold text-xs text-[#34d399] font-mono">
              {c.sustainability_profile.bio_based_pct}% Bio-Based
            </span>
          ) : (
            <span className="text-slate-400 text-xs font-mono">Petroleum Polymer</span>
          )
        },
        {
          label: "Relative Cost Multiplier",
          getValue: (c: any) => (
            <span className="font-mono text-sm font-bold text-[#ffd905]">
              {c.sustainability_profile.relative_cost_index}x <span className="text-xs text-slate-400 font-normal">(vs LDPE)</span>
            </span>
          )
        }
      ]
    },
    {
      category: "Marketplace Procurement & Cost Estimator (INR)",
      items: [
        {
          label: "Bulk Rollstock Cost (₹/kg)",
          getValue: (c: any) => (
            <span className="font-mono text-sm font-bold text-emerald-400">
              {c.procurement_market?.estimated_cost_per_kg_inr || '₹240 – ₹340 / kg'}
            </span>
          )
        },
        {
          label: "Unit Pouch Cost (₹/pouch)",
          getValue: (c: any) => (
            <span className="font-mono text-xs font-semibold text-white">
              {c.procurement_market?.estimated_cost_per_pouch_inr || '₹1.50 – ₹3.00'}
            </span>
          )
        },
        {
          label: "Minimum Order Quantity (MOQ)",
          getValue: (c: any) => (
            <span className="font-mono text-xs text-slate-300">
              {c.procurement_market?.moq || '1,500 units'}
            </span>
          )
        },
        {
          label: "Procurement Lead Time",
          getValue: (c: any) => (
            <span className="font-mono text-xs text-[#ffd905]">
              {c.procurement_market?.lead_time || '3–5 days'}
            </span>
          )
        }
      ]
    },
    {
      category: "Material Anatomy & Durability Lifespan",
      items: [
        {
          label: "Coextrusion / Laminate Layers",
          getValue: (c: any) => (
            <span className="font-mono text-xs text-[#22d3ee] font-bold">
              {c.material_composition?.layers?.length || 2} Production Layers
            </span>
          )
        },
        {
          label: "Unfilled Material Warehouse Lifespan",
          getValue: (c: any) => (
            <span className="font-mono text-xs text-white">
              {c.material_durability?.virgin_material_shelf_life || '18–24 Months'}
            </span>
          )
        },
        {
          label: "Packaged Product Protection Guarantee",
          getValue: (c: any) => (
            <span className="text-xs text-emerald-300 font-sans">
              {c.material_durability?.packaged_product_protection_duration || 'Standard'}
            </span>
          )
        },
        {
          label: "Pre-Receiving Quality Tests",
          getValue: (c: any) => (
            <span className="tag-pill tag-pill-yellow text-[9px]">
              {c.quality_inspection_checklist?.length || 4} QC Protocol Checks
            </span>
          )
        }
      ]
    }
  ];

  return (
    <div className="glass-luxury rounded-[36px] p-8 sm:p-12 max-w-6xl mx-auto shadow-2xl border border-white/15 my-4">
      
      {/* Header */}
      <div className="flex items-center space-x-4 mb-8 pb-6 border-b border-white/10">
        <div className="w-12 h-12 rounded-2xl bg-[#ffd905]/15 border border-[#ffd905]/40 flex items-center justify-center text-[#ffd905]">
          <Scale className="w-6 h-6 stroke-[2.2]" />
        </div>
        <div>
          <span className="tag-pill tag-pill-yellow text-[10px] mb-1.5">
            ✦ Side-by-Side Audit
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            3-Way Candidate Comparison Matrix
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 font-sans mt-0.5">
            Direct parameter evaluation across Top 3 candidate material structures including photos, market costs, and durability.
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-white/15">
              <th className="py-4 px-5 text-xs font-semibold text-slate-400 uppercase tracking-wider w-1/4">
                Specification Attribute
              </th>
              {candidates.map((cand, idx) => (
                <th key={cand.id} className="py-4 px-5 w-1/4">
                  <div className="space-y-2">
                    {cand.sample_photo_url && (
                      <img 
                        src={cand.sample_photo_url} 
                        alt={cand.name} 
                        className="w-14 h-14 rounded-2xl object-cover border border-white/20 mb-2 bg-slate-900"
                      />
                    )}
                    <span className={`tag-pill ${idx === 0 ? 'tag-pill-yellow' : idx === 1 ? 'tag-pill-pink' : 'tag-pill-cyan'} text-[9px]`}>
                      Rank #{cand.rank} {idx === 0 && '• Best Choice'}
                    </span>
                    <div className="text-base font-bold text-white leading-tight mt-1">{cand.name}</div>
                    <div className="text-xs text-slate-400 font-mono truncate">{cand.structure}</div>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {comparisonRows.map((section, sIdx) => (
              <React.Fragment key={sIdx}>
                <tr className="bg-white/[0.02]">
                  <td colSpan={candidates.length + 1} className="py-3 px-5 text-xs font-bold text-[#ffd905] uppercase tracking-wider border-y border-white/10">
                    {section.category}
                  </td>
                </tr>
                {section.items.map((row, rIdx) => (
                  <tr key={rIdx} className="border-b border-white/[0.06] hover:bg-white/[0.02] transition-colors">
                    <td className="py-3.5 px-5 text-xs font-medium text-slate-300">
                      {row.label}
                    </td>
                    {candidates.map((cand) => (
                      <td key={cand.id} className="py-3.5 px-5 text-xs">
                        {row.getValue(cand)}
                      </td>
                    ))}
                  </tr>
                ))}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
