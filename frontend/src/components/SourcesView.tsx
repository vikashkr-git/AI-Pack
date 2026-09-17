import React, { useState } from 'react';
import { BookOpen, ExternalLink, Search, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { ScientificSource } from '../types';

interface SourcesProps {
  sources: ScientificSource[];
}

export const SourcesView: React.FC<SourcesProps> = ({ sources }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredSources = sources.filter(
    (s) =>
      s.source_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (s.scope && s.scope.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-8 max-w-5xl mx-auto animate-fade-in-up py-4">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 pb-6 border-b border-white/10">
        <div>
          <div className="flex items-center space-x-2 mb-2">
            <span className="tag-pill tag-pill-yellow text-[10px]">
              ✦ Scientific Provenance & Bibliography
            </span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
            Empirical Datasets & Academic DOIs
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 font-sans max-w-xl mt-1">
            Full bibliographic traceability and peer-reviewed citations underpinning Kader postharvest constants, USDA nutrient profiles, and ASTM barrier permeabilities.
          </p>
        </div>

        {/* Search Input */}
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-[#ffd905] absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search authors, DOIs, ASTM..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-11 pr-4 py-3 text-xs bg-white/[0.04] border border-white/15 rounded-2xl text-white placeholder-slate-400 focus:outline-none focus:border-[#ffd905] font-sans"
          />
        </div>
      </div>

      {/* Sources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredSources.map((src) => (
          <div key={src.id} className="glass-luxury rounded-[32px] p-6 sm:p-7 border border-white/12 hover:border-white/25 transition-all space-y-4">
            <div className="flex items-start justify-between">
              <span className="tag-pill tag-pill-cyan text-[10px] py-0.5 px-2.5 font-mono">
                {src.id}
              </span>
              <div className="flex items-center space-x-1 text-[#34d399] text-xs font-semibold font-mono">
                <CheckCircle2 className="w-4 h-4" />
                <span>Confidence: {(src.confidence_score * 100).toFixed(0)}%</span>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-bold text-white leading-snug">{src.title}</h3>
              <p className="text-xs text-[#ffd905] mt-1 font-mono">{src.authors} ({src.year})</p>
              {src.publisher_or_journal && (
                <p className="text-xs text-slate-400 italic mt-1 font-sans">{src.publisher_or_journal}</p>
              )}
            </div>

            {src.scope && (
              <div className="p-3.5 rounded-2xl bg-white/[0.03] border border-white/10 text-xs text-slate-300 font-sans">
                <span className="font-bold text-[#ff64d5] uppercase tracking-wider text-[10px] block mb-1">Data Scope:</span>
                {src.scope}
              </div>
            )}

            <div className="pt-2 flex items-center justify-between text-xs">
              {src.doi ? (
                <a
                  href={`https://doi.org/${src.doi}`}
                  target="_blank"
                  rel="noreferrer"
                  className="btn-luxury-yellow px-4 py-1.5 text-xs font-mono flex items-center space-x-1.5"
                >
                  <span>DOI: {src.doi}</span>
                  <ExternalLink className="w-3 h-3 ml-1" />
                </a>
              ) : src.url ? (
                <a
                  href={src.url}
                  target="_blank"
                  rel="noreferrer"
                  className="btn-luxury-glass px-4 py-1.5 text-xs font-mono flex items-center space-x-1.5"
                >
                  <span>Link to Resource</span>
                  <ExternalLink className="w-3 h-3 ml-1" />
                </a>
              ) : (
                <span className="text-slate-500 font-mono text-xs">Reference Standard</span>
              )}
              <span className="text-xs text-slate-400 uppercase font-mono">Peer-Reviewed</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
