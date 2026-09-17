import React from 'react';
import { X, Printer, ShieldCheck, Download, CheckCircle2 } from 'lucide-react';
import { RecommendationResponse } from '../types';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  results: RecommendationResponse | null;
}

export const ExportDossierModal: React.FC<ExportModalProps> = ({ isOpen, onClose, results }) => {
  if (!isOpen || !results) return null;

  const top = results.top_recommendations[0];
  const req = results.scientific_requirements;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-8 bg-black/80 backdrop-blur-xl overflow-y-auto">
      <div className="bg-[#090e1a] border border-white/15 rounded-[36px] max-w-3xl w-full p-6 sm:p-10 text-white shadow-2xl relative max-h-[90vh] overflow-y-auto font-sans">
        
        {/* Header Actions */}
        <div className="flex items-center justify-between pb-6 border-b border-white/10">
          <div className="flex items-center space-x-2.5">
            <span className="tag-pill tag-pill-yellow text-[10px]">
              ✦ Technical Dossier
            </span>
            <span className="text-lg font-bold text-white">PackAI Specification Report</span>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={handlePrint}
              className="btn-luxury-yellow px-5 py-2 text-xs font-bold flex items-center space-x-2"
            >
              <Printer className="w-4 h-4 stroke-[2.2]" />
              <span>Print / Save PDF</span>
            </button>
            <button
              onClick={onClose}
              className="w-10 h-10 rounded-full bg-white/[0.06] hover:bg-white/[0.12] border border-white/15 flex items-center justify-center text-slate-300 hover:text-white transition-all cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Printable Content Body */}
        <div className="py-8 space-y-8 text-xs text-slate-300">
          
          {/* Document Header */}
          <div className="text-center pb-6 border-b border-white/10">
            <span className="tag-pill tag-pill-pink text-[9px] mb-3 inline-block">
              Mass-Transfer & Random Forest AI Recommendation
            </span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              Food Packaging Technical Specification Dossier
            </h1>
            <p className="text-xs text-[#ffd905] font-mono mt-2">
              Target Commodity: <strong className="text-white">{results.query_summary.commodity}</strong> ({results.query_summary.category}) • Generated: {new Date().toLocaleDateString()}
            </p>
          </div>

          {/* Input Conditions Summary */}
          <div>
            <h3 className="text-xs font-bold text-slate-200 tracking-wider mb-3 uppercase text-[#ffd905]">
              1. Input Parameters & Storage Climate
            </h3>
            <div className="grid grid-cols-3 gap-3 bg-white/[0.03] p-5 rounded-3xl border border-white/10 font-mono text-xs">
              <div><span className="text-slate-400">Preservation Mode:</span> <strong className="text-white block mt-0.5">{results.query_summary.storage_type}</strong></div>
              <div><span className="text-slate-400">Temperature:</span> <strong className="text-white block mt-0.5">{req.thermal_mechanical_demands.min_operating_temp_c + 5}°C</strong></div>
              <div><span className="text-slate-400">Target Shelf Life:</span> <strong className="text-white block mt-0.5">{results.query_summary.target_shelf_life_days} Days</strong></div>
              <div><span className="text-slate-400">Water Activity (aw):</span> <strong className="text-[#22d3ee] block mt-0.5">{req.water_activity_aw_estimated}</strong></div>
              <div><span className="text-slate-400">Logistics Stress:</span> <strong className="text-white block mt-0.5">{results.query_summary.transportation}</strong></div>
              <div><span className="text-slate-400">Decision Goal:</span> <strong className="text-[#34d399] block mt-0.5">{results.query_summary.optimization_goal}</strong></div>
            </div>
          </div>

          {/* Primary Recommended Material */}
          <div>
            <h3 className="text-xs font-bold text-slate-200 tracking-wider mb-3 uppercase text-[#ffd905]">
              2. Recommended Multilayer Packaging Structure (Rank #1)
            </h3>
            <div className="bg-white/[0.03] p-6 rounded-3xl border border-[#ffd905]/40 space-y-4 shadow-xl">
              <div className="flex justify-between items-start">
                <div>
                  <div className="text-xl font-bold text-white">{top.name}</div>
                  <div className="text-xs text-[#ffd905] font-mono mt-0.5">{top.structure}</div>
                </div>
                <div className="text-right">
                  <span className="text-2xl font-extrabold text-[#ffd905] block font-mono">{top.suitability_score} / 100</span>
                  <span className="text-[10px] text-slate-400 font-mono">Match Score</span>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3 border-t border-white/10 text-xs font-mono">
                <div><span className="text-slate-400 block text-[10px] uppercase">OTR:</span> {top.technical_specifications.otr_value} cm³/m²·d·atm</div>
                <div><span className="text-slate-400 block text-[10px] uppercase">WVTR:</span> {top.technical_specifications.wvtr_value} g/m²·day</div>
                <div><span className="text-slate-400 block text-[10px] uppercase">Thickness:</span> {top.technical_specifications.thickness_um} µm</div>
                <div><span className="text-slate-400 block text-[10px] uppercase">Sealing Temp:</span> {top.technical_specifications.sealing_temp_range_c}</div>
              </div>

              <div className="pt-3 border-t border-white/10 space-y-2">
                <span className="text-[10px] font-bold text-slate-300 uppercase tracking-wider block">Scientific Selection Rationale:</span>
                {top.explanation.reasons_why.map((r, i) => (
                  <p key={i} className="text-slate-300 text-xs flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 text-[#34d399] flex-shrink-0" />
                    <span>{r}</span>
                  </p>
                ))}
              </div>
            </div>
          </div>

          {/* Standards & Compliance */}
          <div className="pt-4 border-t border-white/10 text-[11px] text-slate-400 font-mono flex flex-col sm:flex-row justify-between items-center gap-2">
            <span>ASTM Barrier Standards: ASTM D3985 (Coulometric O₂), ASTM F1249 (Modulated IR H₂O)</span>
            <span>Model: Random Forest v1.0 • R² = 0.997</span>
          </div>

        </div>

      </div>
    </div>
  );
};
