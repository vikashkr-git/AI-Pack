import React, { useState, useEffect } from 'react';
import { X, Search, Layers, ShieldCheck, Leaf, Filter, ExternalLink, Sparkles } from 'lucide-react';
import { PackagingItem } from '../types';
import { fetchPackaging } from '../services/api';

interface MaterialsLibraryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectMaterial?: (material: PackagingItem) => void;
}

export const MaterialsLibraryModal: React.FC<MaterialsLibraryModalProps> = ({
  isOpen,
  onClose,
  onSelectMaterial
}) => {
  const [materials, setMaterials] = useState<PackagingItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');

  useEffect(() => {
    if (isOpen && materials.length === 0) {
      setLoading(true);
      fetchPackaging()
        .then((data) => {
          setMaterials(data);
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }
  }, [isOpen, materials.length]);

  if (!isOpen) return null;

  const categories = ['ALL', 'Multilayer High Barrier', 'Biodegradable & Bio-Based', 'Metallized & Foil', 'Breathable & Fresh Produce', 'Commodity Monolayer'];

  const filtered = materials.filter((m) => {
    const matchesSearch =
      m.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.structure.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (m.category && m.category.toLowerCase().includes(searchQuery.toLowerCase()));

    if (!matchesSearch) return false;

    if (selectedCategory === 'ALL') return true;
    if (selectedCategory === 'Multilayer High Barrier') return m.structure.includes('/') && !m.structure.includes('Foil') && !m.structure.includes('Met');
    if (selectedCategory === 'Biodegradable & Bio-Based') return (m as any).bio_based_pct > 0 || (m as any).compostable || m.structure.includes('PLA') || m.structure.includes('PBAT');
    if (selectedCategory === 'Metallized & Foil') return m.structure.includes('Foil') || m.structure.includes('Met');
    if (selectedCategory === 'Breathable & Fresh Produce') return (m as any).breathable || (m as any).micro_perforated || m.otr_value > 500;
    if (selectedCategory === 'Commodity Monolayer') return !m.structure.includes('/');
    return true;
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-8 bg-black/80 backdrop-blur-xl overflow-y-auto animate-fade-in-up">
      <div className="bg-[#090e1a] border border-white/15 rounded-[36px] max-w-5xl w-full p-6 sm:p-10 text-white shadow-2xl relative max-h-[90vh] flex flex-col font-sans">
        
        {/* Header Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-white/10 gap-4 flex-shrink-0">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <span className="tag-pill tag-pill-cyan text-[10px]">
                ✦ Calibrated Barrier Database
              </span>
              <span className="text-xs text-slate-400 font-mono">ASTM D3985 / ASTM F1249</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              Packaging Materials <span className="text-[#22d3ee]">Library</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 font-sans mt-1">
              Browse calibrated barrier specifications, multilayer co-extrusions, and recyclability streams for 15+ packaging films.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={onClose}
              className="w-10 h-10 rounded-full bg-white/[0.06] hover:bg-white/[0.12] border border-white/15 flex items-center justify-center text-slate-300 hover:text-white transition-all cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Filter Controls & Search */}
        <div className="py-5 space-y-4 flex-shrink-0">
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
            {/* Search Input */}
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 text-[#22d3ee] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search EVOH, Aluminum Foil, PLA, BOPP..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 text-xs bg-white/[0.04] border border-white/15 rounded-2xl text-white placeholder-slate-400 focus:outline-none focus:border-[#22d3ee] font-sans"
              />
            </div>

            <span className="text-xs font-mono text-slate-400">
              Showing <strong className="text-[#22d3ee]">{filtered.length}</strong> of {materials.length} validated structures
            </span>
          </div>

          {/* Filter Pills */}
          <div className="flex flex-wrap gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-medium transition-all cursor-pointer ${
                  selectedCategory === cat
                    ? 'bg-[#ffd905] text-slate-950 font-bold shadow-[0_0_15px_rgba(255,217,5,0.3)]'
                    : 'bg-white/[0.04] hover:bg-white/[0.08] border border-white/10 text-slate-300'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Materials Grid (Scrollable) */}
        <div className="overflow-y-auto pr-2 flex-1 space-y-4 py-2">
          {loading ? (
            <div className="text-center py-20 text-slate-400">
              <div className="w-8 h-8 border-2 border-[#22d3ee] border-t-transparent rounded-full animate-spin mx-auto mb-3" />
              <span className="text-sm font-semibold text-white">Loading Barrier Catalog...</span>
            </div>
          ) : filtered.length === 0 ? (
            <div className="text-center py-16 text-slate-400 font-mono text-xs">
              No packaging materials found matching "{searchQuery}".
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filtered.map((mat) => {
                const isFoil = mat.structure.includes('Foil') || mat.structure.includes('Met');
                const isBio = (mat as any).bio_based_pct > 0 || mat.structure.includes('PLA') || mat.structure.includes('PBAT');
                const isProduce = (mat as any).breathable || mat.otr_value > 500;

                return (
                  <div
                    key={mat.id}
                    className="p-5 rounded-3xl bg-white/[0.03] border border-white/10 hover:border-white/25 transition-all flex flex-col justify-between group shadow-sm hover:shadow-xl"
                  >
                    <div className="flex items-start gap-4">
                      {mat.sample_photo_url && (
                        <img 
                          src={mat.sample_photo_url} 
                          alt={mat.name} 
                          className="w-16 h-16 rounded-2xl object-cover border border-white/20 flex-shrink-0 bg-slate-900"
                        />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between mb-1">
                          <span className="tag-pill tag-pill-cyan text-[9px] py-0 px-2 font-mono">
                            {mat.id}
                          </span>
                          {isBio ? (
                            <span className="tag-pill tag-pill-emerald text-[9px] py-0 px-2 font-mono">
                              🌱 Bio-Based
                            </span>
                          ) : isFoil ? (
                            <span className="tag-pill tag-pill-yellow text-[9px] py-0 px-2 font-mono">
                              ⚡ Ultra Barrier
                            </span>
                          ) : isProduce ? (
                            <span className="tag-pill tag-pill-pink text-[9px] py-0 px-2 font-mono">
                              💨 Breathable
                            </span>
                          ) : (
                            <span className="text-[10px] font-mono text-slate-400">
                              {mat.category}
                            </span>
                          )}
                        </div>

                        <h3 className="text-base font-bold text-white tracking-tight group-hover:text-[#ffd905] transition-colors line-clamp-1">
                          {mat.name}
                        </h3>
                        <p className="text-xs text-[#ffd905] font-mono mt-0.5 line-clamp-1">
                          {mat.structure}
                        </p>
                      </div>
                    </div>

                    {/* Barrier Specs Matrix */}
                    <div className="grid grid-cols-3 gap-2 py-2.5 border-y border-white/10 my-2.5 text-xs font-mono">
                      <div>
                        <span className="text-slate-400 block text-[9px] uppercase">OTR</span>
                        <span className="text-white font-bold">{mat.otr_value}</span>
                        <span className="text-slate-400 block text-[8px]">cm³/m²·d</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[9px] uppercase">WVTR</span>
                        <span className="text-white font-bold">{mat.wvtr_value}</span>
                        <span className="text-slate-400 block text-[8px]">g/m²·d</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[9px] uppercase">Gauge</span>
                        <span className="text-white font-bold">{mat.total_thickness_um} µm</span>
                        <span className="text-slate-400 block text-[8px]">Dart: {(mat as any).puncture_resistance_n || '15'} N</span>
                      </div>
                    </div>

                    {/* Footer Info with Market Cost and Durability */}
                    <div className="space-y-1.5 pt-1 text-xs font-mono">
                      <div className="flex items-center justify-between">
                        <span className="text-emerald-400 font-bold">
                          {mat.procurement_market?.estimated_cost_per_kg_inr || `${(mat as any).cost_index_relative || 1.2}x Base`}
                        </span>
                        <span className="text-slate-400 text-[11px]">
                          Pouch: <strong className="text-slate-200">{mat.procurement_market?.estimated_cost_per_pouch_inr || '₹1.50 – ₹3.00'}</strong>
                        </span>
                      </div>
                      {mat.material_composition?.why_this_material_short && (
                        <p className="text-[11px] text-slate-300 line-clamp-2 font-sans">
                          {mat.material_composition.why_this_material_short}
                        </p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

      </div>
    </div>
  );
};
