import React, { useState, useEffect } from 'react';
import { 
  Layers, 
  Thermometer, 
  Truck, 
  Settings2, 
  CheckCircle2, 
  AlertTriangle, 
  Zap,
  Sparkles,
  ArrowRight,
  ArrowLeft
} from 'lucide-react';
import { FoodInputFormState, FoodProfile } from '../types';
import { validateInput } from '../services/api';

interface WizardProps {
  formState: FoodInputFormState;
  setFormState: React.Dispatch<React.SetStateAction<FoodInputFormState>>;
  onSubmit: () => void;
  isLoading: boolean;
  foodsList: FoodProfile[];
}

export const RecommendationWizard: React.FC<WizardProps> = ({
  formState,
  setFormState,
  onSubmit,
  isLoading,
  foodsList
}) => {
  const [activeStep, setActiveStep] = useState<number>(1);
  const [warnings, setWarnings] = useState<string[]>([]);

  // Validate inputs on change
  useEffect(() => {
    const timer = setTimeout(async () => {
      try {
        const res = await validateInput({
          commodity: formState.commodity,
          moisture_pct: formState.moisture_pct,
          fat_pct: formState.fat_pct,
          protein_pct: formState.protein_pct,
          storage_temp_c: formState.storage_temp_c,
          storage_type: formState.storage_type
        });
        setWarnings(res.warnings || []);
      } catch (err) {
        // Silently skip validation network errors
      }
    }, 250);
    return () => clearTimeout(timer);
  }, [formState.commodity, formState.moisture_pct, formState.fat_pct, formState.protein_pct, formState.storage_temp_c, formState.storage_type]);

  const handleCommoditySelect = (commodityName: string) => {
    const matched = foodsList.find((f) => f.commodity.toLowerCase() === commodityName.toLowerCase());
    if (matched) {
      setFormState((prev) => ({
        ...prev,
        commodity: matched.commodity,
        category: matched.category,
        moisture_pct: matched.moisture_pct,
        fat_pct: matched.fat_pct,
        protein_pct: matched.protein_pct,
        ph: matched.ph,
        respiration_rate: matched.respiration_rate_val,
        shelf_life_days: matched.standard_shelf_life_days,
        storage_temp_c: matched.optimal_temp_c,
        relative_humidity_pct: matched.optimal_rh_pct,
        storage_type: matched.optimal_storage_type as any
      }));
    } else {
      setFormState((prev) => ({ ...prev, commodity: commodityName }));
    }
  };

  const steps = [
    { num: 1, label: "Food Profile", icon: Layers },
    { num: 2, label: "Storage Climate", icon: Thermometer },
    { num: 3, label: "Transit Stress", icon: Truck },
    { num: 4, label: "Decision Goal", icon: Settings2 },
  ];

  const quickPicks = ['Tomato', 'Potato Chips', 'Milk Powder', 'Strawberries', 'Fresh Fish', 'Honey'];

  return (
    <div className="glass-luxury rounded-[36px] p-8 sm:p-14 max-w-4xl mx-auto shadow-2xl relative overflow-hidden my-8">
      
      {/* Step Tabs with Generous Spacing */}
      <div className="mb-12">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
          {steps.map((step) => {
            const Icon = step.icon;
            const isCurrent = activeStep === step.num;
            const isPassed = activeStep > step.num;
            return (
              <button
                key={step.num}
                onClick={() => setActiveStep(step.num)}
                className={`py-3 px-4 rounded-2xl flex items-center justify-center space-x-2.5 transition-all duration-300 cursor-pointer ${
                  isCurrent
                    ? 'bg-gradient-to-r from-[#ffd905] to-[#f5b700] text-slate-950 font-bold shadow-[0_4px_20px_rgba(255,217,5,0.35)] scale-[1.02]'
                    : isPassed
                    ? 'bg-white/[0.08] text-[#34d399] border border-[#34d399]/30'
                    : 'bg-white/[0.04] text-slate-400 hover:text-white border border-white/10'
                }`}
              >
                <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                  isCurrent ? 'bg-slate-950 text-[#ffd905]' : isPassed ? 'bg-[#34d399] text-slate-950' : 'bg-white/10 text-white'
                }`}>
                  {isPassed ? '✓' : step.num}
                </div>
                <span className="text-xs font-semibold tracking-wide">
                  {step.label}
                </span>
              </button>
            );
          })}
        </div>

        {/* Smooth Subtle Progress Line */}
        <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-[#ffd905] via-[#ff64d5] to-[#22d3ee] rounded-full transition-all duration-500"
            style={{ width: `${(activeStep / 4) * 100}%` }}
          />
        </div>
      </div>

      {/* Validation Warnings */}
      {warnings.length > 0 && (
        <div className="mb-8 p-5 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs flex items-start space-x-3.5 shadow-lg">
          <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5 text-amber-400 animate-bounce" />
          <div className="space-y-1">
            <span className="font-bold text-amber-300 block text-sm">Physical Parameter Notice</span>
            {warnings.map((w, idx) => (
              <p key={idx} className="text-slate-300 leading-relaxed font-sans">{w}</p>
            ))}
          </div>
        </div>
      )}

      {/* STEP 1: FOOD PROPERTIES */}
      {activeStep === 1 && (
        <div className="space-y-8 animate-fade-in-up">
          <div className="pb-4 border-b border-white/10">
            <h3 className="text-2xl font-bold text-white tracking-tight flex items-center space-x-2.5">
              <Sparkles className="w-5 h-5 text-[#ffd905]" />
              <span>Food Commodity Characteristics</span>
            </h3>
            <p className="text-sm text-slate-300 mt-1">
              Select standard benchmark foods from USDA reference database or adjust proximate parameters.
            </p>
          </div>

          {/* Quick Select Preset Chips */}
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider mr-1">Quick Picks:</span>
            {quickPicks.map((pick) => (
              <button
                key={pick}
                type="button"
                onClick={() => handleCommoditySelect(pick)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-medium transition-all cursor-pointer ${
                  formState.commodity.toLowerCase() === pick.toLowerCase()
                    ? 'bg-[#ffd905] text-slate-950 font-bold shadow-[0_0_15px_rgba(255,217,5,0.4)] scale-105'
                    : 'bg-white/[0.06] hover:bg-white/[0.12] text-slate-300 border border-white/10'
                }`}
              >
                {pick}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {/* Commodity Select */}
            <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/12 focus-within:border-[#ffd905] transition-all">
              <label className="block text-xs font-bold text-slate-300 mb-2 flex items-center justify-between">
                <span>Commodity Name</span>
                <span className="tag-pill tag-pill-cyan text-[8px] py-0 px-2 font-mono">USDA Autofill</span>
              </label>
              <select
                value={formState.commodity}
                onChange={(e) => handleCommoditySelect(e.target.value)}
                className="w-full px-4 py-2.5 text-sm bg-slate-950/80 border border-white/15 rounded-xl text-white font-medium focus:outline-none focus:border-[#ffd905] cursor-pointer"
              >
                {foodsList.map((f) => (
                  <option key={f.commodity} value={f.commodity} className="bg-slate-900 text-white">
                    {f.commodity} ({f.category})
                  </option>
                ))}
              </select>
            </div>

            {/* Category */}
            <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/12 focus-within:border-[#ffd905] transition-all">
              <label className="block text-xs font-bold text-slate-300 mb-2">Food Category</label>
              <input
                type="text"
                value={formState.category}
                onChange={(e) => setFormState({ ...formState, category: e.target.value })}
                className="w-full px-4 py-2.5 text-sm bg-slate-950/80 border border-white/15 rounded-xl text-white font-medium focus:outline-none focus:border-[#ffd905]"
              />
            </div>
          </div>

          {/* Proximate Composition 4-Box Grid with Generous Spacing */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
            <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/12 focus-within:border-[#ff64d5] transition-all">
              <label className="block text-xs font-semibold text-slate-400 mb-1.5">Moisture (%)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                max="100"
                value={formState.moisture_pct}
                onChange={(e) => setFormState({ ...formState, moisture_pct: parseFloat(e.target.value) || 0 })}
                className="w-full text-2xl font-bold bg-transparent border-none text-[#ff64d5] font-mono focus:outline-none"
              />
            </div>

            <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/12 focus-within:border-[#ffd905] transition-all">
              <label className="block text-xs font-semibold text-slate-400 mb-1.5">Fat / Lipid (%)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                max="100"
                value={formState.fat_pct}
                onChange={(e) => setFormState({ ...formState, fat_pct: parseFloat(e.target.value) || 0 })}
                className="w-full text-2xl font-bold bg-transparent border-none text-[#ffd905] font-mono focus:outline-none"
              />
            </div>

            <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/12 focus-within:border-[#22d3ee] transition-all">
              <label className="block text-xs font-semibold text-slate-400 mb-1.5">Protein (%)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                max="100"
                value={formState.protein_pct}
                onChange={(e) => setFormState({ ...formState, protein_pct: parseFloat(e.target.value) || 0 })}
                className="w-full text-2xl font-bold bg-transparent border-none text-[#22d3ee] font-mono focus:outline-none"
              />
            </div>

            <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/12 focus-within:border-[#34d399] transition-all">
              <label className="block text-xs font-semibold text-slate-400 mb-1.5">Acidity (pH)</label>
              <input
                type="number"
                step="0.1"
                min="1"
                max="14"
                value={formState.ph}
                onChange={(e) => setFormState({ ...formState, ph: parseFloat(e.target.value) || 7 })}
                className="w-full text-2xl font-bold bg-transparent border-none text-[#34d399] font-mono focus:outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-2">
            <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/12 focus-within:border-[#ffd905]">
              <label className="block text-xs font-bold text-slate-300 mb-2 flex items-center justify-between">
                <span>Respiration Rate (mg CO₂ / kg·hr)</span>
                <span className="text-[11px] text-slate-400 font-mono">0 for non-produce</span>
              </label>
              <input
                type="number"
                step="0.5"
                min="0"
                value={formState.respiration_rate}
                onChange={(e) => setFormState({ ...formState, respiration_rate: parseFloat(e.target.value) || 0 })}
                className="w-full px-4 py-2.5 text-sm bg-slate-950/80 border border-white/15 rounded-xl text-white font-mono font-bold focus:outline-none"
              />
            </div>

            <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/12 focus-within:border-[#ffd905]">
              <label className="block text-xs font-bold text-slate-300 mb-2">
                Target Shelf Life (Days)
              </label>
              <input
                type="number"
                min="1"
                max="1200"
                value={formState.shelf_life_days}
                onChange={(e) => setFormState({ ...formState, shelf_life_days: parseInt(e.target.value) || 30 })}
                className="w-full px-4 py-2.5 text-sm bg-slate-950/80 border border-white/15 rounded-xl text-white font-mono font-bold focus:outline-none"
              />
            </div>
          </div>
        </div>
      )}

      {/* STEP 2: STORAGE & ENVIRONMENT */}
      {activeStep === 2 && (
        <div className="space-y-8 animate-fade-in-up">
          <div className="pb-4 border-b border-white/10">
            <h3 className="text-2xl font-bold text-white tracking-tight flex items-center space-x-2.5">
              <Thermometer className="w-5 h-5 text-[#ffd905]" />
              <span>Storage Temperature & Climate Gradients</span>
            </h3>
            <p className="text-sm text-slate-300 mt-1">
              Environmental gradients govern vapor-pressure driving forces across the film barrier.
            </p>
          </div>

          {/* Storage Mode 3 Big Cards */}
          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-3.5">
              Storage Preservation Regime
            </label>
            <div className="grid grid-cols-3 gap-4 sm:gap-6">
              {[
                { type: 'Ambient', temp: 22, desc: 'Room Temperature (22°C)' },
                { type: 'Chilled', temp: 4, desc: 'Cold Chain (4°C)' },
                { type: 'Frozen', temp: -18, desc: 'Deep Freeze (-18°C)' },
              ].map((item) => {
                const isSelected = formState.storage_type === item.type;
                return (
                  <button
                    key={item.type}
                    type="button"
                    onClick={() => setFormState({ ...formState, storage_type: item.type as any, storage_temp_c: item.temp })}
                    className={`p-6 rounded-3xl text-center transition-all duration-300 cursor-pointer ${
                      isSelected
                        ? 'bg-gradient-to-b from-[#ffd905]/20 to-transparent border-2 border-[#ffd905] shadow-[0_8px_30px_rgba(255,217,5,0.25)] scale-[1.03]'
                        : 'bg-white/[0.04] border border-white/12 text-slate-400 hover:text-white hover:border-white/30'
                    }`}
                  >
                    <div className={`text-xl font-bold mb-1 ${isSelected ? 'text-[#ffd905]' : 'text-white'}`}>
                      {item.type}
                    </div>
                    <div className="text-xs text-slate-400 font-mono">
                      {item.desc}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Temperature Slider */}
          <div className="p-6 rounded-3xl bg-white/[0.03] border border-white/12">
            <div className="flex justify-between items-center mb-3">
              <label className="text-xs font-bold text-slate-200 uppercase tracking-wider">Exact Storage Temperature</label>
              <span className="tag-pill tag-pill-cyan text-xs font-mono font-bold">
                {formState.storage_temp_c}°C
              </span>
            </div>
            <input
              type="range"
              min="-25"
              max="45"
              step="0.5"
              value={formState.storage_temp_c}
              onChange={(e) => setFormState({ ...formState, storage_temp_c: parseFloat(e.target.value) })}
              className="w-full accent-[#ffd905] cursor-pointer h-2 bg-slate-900 rounded-lg"
            />
            <div className="flex justify-between text-[11px] text-slate-400 mt-3 font-mono">
              <span>-25°C (Cryo Freeze)</span>
              <span>4°C (Chilled)</span>
              <span>22°C (Ambient)</span>
              <span>45°C (Extreme Heat)</span>
            </div>
          </div>

          {/* Humidity Slider */}
          <div className="p-6 rounded-3xl bg-white/[0.03] border border-white/12">
            <div className="flex justify-between items-center mb-3">
              <label className="text-xs font-bold text-slate-200 uppercase tracking-wider">Relative Humidity</label>
              <span className="tag-pill tag-pill-pink text-xs font-mono font-bold">
                {formState.relative_humidity_pct}% RH
              </span>
            </div>
            <input
              type="range"
              min="20"
              max="98"
              step="1"
              value={formState.relative_humidity_pct}
              onChange={(e) => setFormState({ ...formState, relative_humidity_pct: parseFloat(e.target.value) })}
              className="w-full accent-[#ff64d5] cursor-pointer h-2 bg-slate-900 rounded-lg"
            />
            <div className="flex justify-between text-[11px] text-slate-400 mt-3 font-mono">
              <span>20% (Arid)</span>
              <span>55% (Moderate)</span>
              <span>75% (Monsoon)</span>
              <span>95% (Saturated)</span>
            </div>
          </div>
        </div>
      )}

      {/* STEP 3: TRANSIT STRESS */}
      {activeStep === 3 && (
        <div className="space-y-8 animate-fade-in-up">
          <div className="pb-4 border-b border-white/10">
            <h3 className="text-2xl font-bold text-white tracking-tight flex items-center space-x-2.5">
              <Truck className="w-5 h-5 text-[#ffd905]" />
              <span>Logistics & Mechanical Vibration Stress</span>
            </h3>
            <p className="text-sm text-slate-300 mt-1">
              Sets minimum tensile burst and dart-drop puncture resistance limits to prevent transit leaks.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
            {[
              { id: 'Normal', label: 'Local / Regional', desc: 'Standard road freight, moderate vibration risk (tensile ≥ 20 MPa)' },
              { id: 'Refrigerated', label: 'Reefer Cold Chain', desc: 'Active refrigerated container with continuous humidity monitoring' },
              { id: 'Long_Distance', label: 'Long Distance / Severe', desc: 'Rough highways, multiple transshipments, puncture ≥ 25 N' }
            ].map((t) => {
              const isSelected = formState.transportation === t.id;
              return (
                <button
                  key={t.id}
                  type="button"
                  onClick={() => setFormState({ ...formState, transportation: t.id as any })}
                  className={`p-6 rounded-3xl text-left transition-all duration-300 cursor-pointer ${
                    isSelected
                      ? 'bg-gradient-to-b from-[#ffd905]/15 to-transparent border-2 border-[#ffd905] shadow-[0_8px_30px_rgba(255,217,5,0.25)] scale-[1.02]'
                      : 'bg-white/[0.04] border border-white/12 text-slate-400 hover:text-white'
                  }`}
                >
                  <div className={`text-lg font-bold mb-2 ${isSelected ? 'text-[#ffd905]' : 'text-white'}`}>{t.label}</div>
                  <div className="text-xs text-slate-300 leading-relaxed font-sans">{t.desc}</div>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* STEP 4: GOAL & WEIGHTS */}
      {activeStep === 4 && (
        <div className="space-y-8 animate-fade-in-up">
          <div className="pb-4 border-b border-white/10">
            <h3 className="text-2xl font-bold text-white tracking-tight flex items-center space-x-2.5">
              <Settings2 className="w-5 h-5 text-[#34d399]" />
              <span>Optimization Objectives & Decision Weights</span>
            </h3>
            <p className="text-sm text-slate-300 mt-1">
              Shifts multi-criteria ranking weights across barrier protection, circularity, and economic cost margins.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {[
              {
                id: 'Balanced',
                label: 'Balanced Industry Optimum',
                badge: 'Recommended',
                badgeClass: 'tag-pill-yellow',
                desc: '80% Technical Barrier + 10% Recyclability Index + 10% Economic Cost Margin'
              },
              {
                id: 'Performance',
                label: 'Maximum Barrier Protection',
                badge: 'Zero Spoilage',
                badgeClass: 'tag-pill-pink',
                desc: '90% Technical Barrier & Shelf-Life Safety (Prioritizes barrier integrity above cost)'
              },
              {
                id: 'Sustainability',
                label: 'Circular & Eco Focus',
                badge: 'Circular Economy',
                badgeClass: 'tag-pill-emerald',
                desc: '35% Bonus for Bio-based, Compostable, and Mono-Material Recyclable Structures'
              },
              {
                id: 'Cost_Optimized',
                label: 'Cost-Optimized / Economy',
                badge: 'MSME Friendly',
                badgeClass: 'tag-pill-cyan',
                desc: 'Favors accessible commodity films meeting minimum required ASTM barrier margins'
              }
            ].map((goal) => {
              const isSelected = formState.optimization_goal === goal.id;
              return (
                <button
                  key={goal.id}
                  type="button"
                  onClick={() => setFormState({ ...formState, optimization_goal: goal.id as any })}
                  className={`p-6 rounded-3xl text-left transition-all duration-300 cursor-pointer ${
                    isSelected
                      ? 'bg-gradient-to-b from-[#ffd905]/15 to-transparent border-2 border-[#ffd905] shadow-[0_8px_30px_rgba(255,217,5,0.25)] scale-[1.02]'
                      : 'bg-white/[0.04] border border-white/12 text-slate-400 hover:text-white'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className={`text-base font-bold ${isSelected ? 'text-[#ffd905]' : 'text-white'}`}>{goal.label}</span>
                    <span className={`tag-pill ${goal.badgeClass} text-[9px] py-0.5 px-2.5`}>
                      {goal.badge}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed font-sans">{goal.desc}</p>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Navigation Footer with Spacious Tactile Buttons */}
      <div className="flex items-center justify-between mt-12 pt-8 border-t border-white/10">
        <div>
          {activeStep > 1 && (
            <button
              type="button"
              onClick={() => setActiveStep((prev) => prev - 1)}
              className="btn-luxury-glass px-5 py-2.5 text-xs font-semibold flex items-center space-x-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>
          )}
        </div>

        <div className="flex space-x-4">
          {activeStep < 4 ? (
            <button
              type="button"
              onClick={() => setActiveStep((prev) => prev + 1)}
              className="btn-luxury-glass px-6 py-2.5 text-xs font-semibold flex items-center space-x-2"
            >
              <span>Continue</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="button"
              disabled={isLoading}
              onClick={onSubmit}
              className={`btn-luxury-yellow px-8 py-3.5 text-sm font-bold tracking-wide shadow-xl flex items-center space-x-2.5 ${
                isLoading ? 'opacity-70 cursor-not-allowed' : ''
              }`}
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                  <span>Computing Mass-Transfer & AI Ranking...</span>
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4 fill-current" />
                  <span>Generate AI Recommendation ⚡</span>
                </>
              )}
            </button>
          )}
        </div>
      </div>

    </div>
  );
};
