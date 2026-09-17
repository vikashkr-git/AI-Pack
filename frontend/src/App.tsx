import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { HeroSection } from './components/HeroSection';
import { RecommendationWizard } from './components/RecommendationWizard';
import { ResultsView } from './components/ResultsView';
import { ComparisonView } from './components/ComparisonView';
import { SustainabilityView } from './components/SustainabilityView';
import { SourcesView } from './components/SourcesView';
import { ModelDashboard } from './components/ModelDashboard';
import { ExportDossierModal } from './components/ExportDossierModal';
import { MaterialsLibraryModal } from './components/MaterialsLibraryModal';
import { MarqueeTicker } from './components/MarqueeTicker';
import { BackgroundEffects } from './components/BackgroundEffects';
import { ArrowLeft, Sparkles, Scale, Leaf, BookOpen, Activity } from 'lucide-react';

import {
  fetchHealth,
  fetchFoods,
  fetchSources,
  fetchModelInfo,
  requestRecommendation
} from './services/api';
import {
  FoodInputFormState,
  FoodProfile,
  ScientificSource,
  ModelInfo,
  RecommendationResponse
} from './types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('wizard');
  const [hasResults, setHasResults] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isExportOpen, setIsExportOpen] = useState<boolean>(false);
  const [isMaterialsOpen, setIsMaterialsOpen] = useState<boolean>(false);

  // Reference Data State
  const [foodsList, setFoodsList] = useState<FoodProfile[]>([]);
  const [sourcesList, setSourcesList] = useState<ScientificSource[]>([]);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);

  // Form State
  const [formState, setFormState] = useState<FoodInputFormState>({
    commodity: 'Tomato',
    category: 'Fresh Produce',
    moisture_pct: 94.5,
    fat_pct: 0.2,
    protein_pct: 0.9,
    ph: 4.3,
    respiration_rate: 18.5,
    shelf_life_days: 14,
    storage_temp_c: 12.0,
    relative_humidity_pct: 90.0,
    storage_type: 'Chilled',
    transportation: 'Refrigerated',
    optimization_goal: 'Balanced'
  });

  // Results State
  const [results, setResults] = useState<RecommendationResponse | null>(null);

  // Load backend data on mount
  useEffect(() => {
    async function initData() {
      try {
        const [foods, sources, model] = await Promise.all([
          fetchFoods().catch(() => []),
          fetchSources().catch(() => []),
          fetchModelInfo().catch(() => null)
        ]);

        setFoodsList(foods);
        setSourcesList(sources);
        setModelInfo(model);
      } catch (err) {
        console.error('Initialization error:', err);
      }
    }
    initData();
  }, []);

  const handleGenerateRecommendation = async (overrideState?: FoodInputFormState) => {
    setIsLoading(true);
    setErrorMsg(null);
    const targetPayload = overrideState || formState;

    try {
      const data = await requestRecommendation(targetPayload);
      setResults(data);
      setHasResults(true);
      setActiveTab('results');
    } catch (err: any) {
      setErrorMsg(err.message || 'An unexpected error occurred while analyzing packaging requirements.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectPreset = (preset: FoodInputFormState) => {
    setFormState(preset);
    handleGenerateRecommendation(preset);
  };

  // 1-Click Quick Demo Handler
  const handleQuickDemo = () => {
    const demoPayload: FoodInputFormState = {
      commodity: 'Potato Chips',
      category: 'Snacks',
      moisture_pct: 2.0,
      fat_pct: 34.5,
      protein_pct: 6.5,
      ph: 6.2,
      respiration_rate: 0.0,
      shelf_life_days: 180,
      storage_temp_c: 22.0,
      relative_humidity_pct: 50.0,
      storage_type: 'Ambient',
      transportation: 'Long_Distance',
      optimization_goal: 'Balanced'
    };
    setFormState(demoPayload);
    handleGenerateRecommendation(demoPayload);
  };

  // Random Food Surprise Me Handler
  const handleRandomCommodity = () => {
    if (foodsList.length === 0) return;
    const randomFood = foodsList[Math.floor(Math.random() * foodsList.length)];
    const randomPayload: FoodInputFormState = {
      commodity: randomFood.commodity,
      category: randomFood.category,
      moisture_pct: randomFood.moisture_pct,
      fat_pct: randomFood.fat_pct,
      protein_pct: randomFood.protein_pct,
      ph: randomFood.ph,
      respiration_rate: randomFood.respiration_rate_val,
      shelf_life_days: randomFood.standard_shelf_life_days,
      storage_temp_c: randomFood.optimal_temp_c,
      relative_humidity_pct: randomFood.optimal_rh_pct,
      storage_type: randomFood.optimal_storage_type as any,
      transportation: 'Refrigerated',
      optimization_goal: 'Balanced'
    };
    setFormState(randomPayload);
    handleGenerateRecommendation(randomPayload);
  };

  // Reset Handler
  const handleReset = () => {
    setFormState({
      commodity: 'Tomato',
      category: 'Fresh Produce',
      moisture_pct: 94.5,
      fat_pct: 0.2,
      protein_pct: 0.9,
      ph: 4.3,
      respiration_rate: 18.5,
      shelf_life_days: 14,
      storage_temp_c: 12.0,
      relative_humidity_pct: 90.0,
      storage_type: 'Chilled',
      transportation: 'Refrigerated',
      optimization_goal: 'Balanced'
    });
    setActiveTab('wizard');
  };

  // Ensure dossier has data to display even if user opens before running
  const handleOpenDossier = async () => {
    if (!results) {
      try {
        const defaultData = await requestRecommendation(formState);
        setResults(defaultData);
        setHasResults(true);
      } catch (err) {
        // Fallback
      }
    }
    setIsExportOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-ambient-canvas bg-subtle-grid text-slate-100 relative overflow-x-hidden">
      
      {/* Soft Luminous Aurora Atmosphere Layer */}
      <BackgroundEffects />

      {/* Top Floating Glass Capsule Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        hasResults={hasResults}
        onOpenExport={handleOpenDossier}
        onOpenMaterialsLibrary={() => setIsMaterialsOpen(true)}
        onQuickDemo={handleQuickDemo}
        onRandomCommodity={handleRandomCommodity}
        onReset={handleReset}
      />

      {/* Main Spacious Content Container */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-8 py-8 w-full relative z-10">
        
        {/* Global Error Banner */}
        {errorMsg && (
          <div className="mb-8 p-5 rounded-3xl bg-rose-500/15 border border-rose-500/30 text-rose-200 text-xs flex justify-between items-center shadow-xl">
            <span>{errorMsg}</span>
            <button onClick={() => setErrorMsg(null)} className="font-bold hover:underline cursor-pointer uppercase tracking-wider ml-4">Dismiss</button>
          </div>
        )}

        {/* Home / Advisor View */}
        {activeTab === 'wizard' && (
          <div className="space-y-10 animate-fade-in-up">
            <HeroSection onSelectPreset={handleSelectPreset} />
            
            {/* Elegant Marquee Ticker */}
            <MarqueeTicker />

            <RecommendationWizard
              formState={formState}
              setFormState={setFormState}
              onSubmit={() => handleGenerateRecommendation()}
              isLoading={isLoading}
              foodsList={foodsList}
            />
          </div>
        )}

        {/* Results & Analysis Exploration Views */}
        {activeTab !== 'wizard' && (
          <div className="space-y-8 animate-fade-in-up">
            
            {/* Elegant In-Page Sub-Navigation Bar */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-[30px] bg-white/[0.03] border border-white/12 shadow-xl backdrop-blur-xl">
              <div className="flex flex-wrap items-center gap-2.5">
                <button
                  onClick={() => setActiveTab('results')}
                  className={`px-4 py-2 rounded-full text-xs font-bold transition-all cursor-pointer flex items-center space-x-1.5 ${
                    activeTab === 'results' ? 'btn-luxury-yellow' : 'btn-luxury-glass'
                  }`}
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>AI Picks</span>
                </button>

                <button
                  onClick={() => setActiveTab('compare')}
                  className={`px-4 py-2 rounded-full text-xs font-bold transition-all cursor-pointer flex items-center space-x-1.5 ${
                    activeTab === 'compare' ? 'btn-luxury-yellow' : 'btn-luxury-glass'
                  }`}
                >
                  <Scale className="w-3.5 h-3.5" />
                  <span>3-Way Compare</span>
                </button>

                <button
                  onClick={() => setActiveTab('sustainability')}
                  className={`px-4 py-2 rounded-full text-xs font-bold transition-all cursor-pointer flex items-center space-x-1.5 ${
                    activeTab === 'sustainability' ? 'btn-luxury-yellow' : 'btn-luxury-glass'
                  }`}
                >
                  <Leaf className="w-3.5 h-3.5" />
                  <span>Eco & Circularity</span>
                </button>

                <button
                  onClick={() => setActiveTab('sources')}
                  className={`px-4 py-2 rounded-full text-xs font-bold transition-all cursor-pointer flex items-center space-x-1.5 ${
                    activeTab === 'sources' ? 'btn-luxury-yellow' : 'btn-luxury-glass'
                  }`}
                >
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>Scientific Sources</span>
                </button>

                <button
                  onClick={() => setActiveTab('diagnostics')}
                  className={`px-4 py-2 rounded-full text-xs font-bold transition-all cursor-pointer flex items-center space-x-1.5 ${
                    activeTab === 'diagnostics' ? 'btn-luxury-yellow' : 'btn-luxury-glass'
                  }`}
                >
                  <Activity className="w-3.5 h-3.5" />
                  <span>ML Diagnostics</span>
                </button>
              </div>

              <button
                onClick={() => setActiveTab('wizard')}
                className="btn-luxury-glass px-5 py-2 text-xs font-semibold flex items-center space-x-2 self-end sm:self-auto"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Configure New Commodity</span>
              </button>
            </div>

            {/* View Components */}
            {activeTab === 'results' && results && (
              <ResultsView
                results={results}
                onNavigateToCompare={() => setActiveTab('compare')}
                onNavigateToSustainability={() => setActiveTab('sustainability')}
              />
            )}

            {activeTab === 'compare' && results && (
              <ComparisonView results={results} />
            )}

            {activeTab === 'sustainability' && results && (
              <SustainabilityView results={results} />
            )}

            {activeTab === 'sources' && (
              <SourcesView sources={sourcesList} />
            )}

            {activeTab === 'diagnostics' && (
              <ModelDashboard modelInfo={modelInfo} />
            )}

          </div>
        )}

      </main>

      {/* Materials Library Modal */}
      <MaterialsLibraryModal
        isOpen={isMaterialsOpen}
        onClose={() => setIsMaterialsOpen(false)}
      />

      {/* Export Dossier Modal */}
      <ExportDossierModal
        isOpen={isExportOpen}
        onClose={() => setIsExportOpen(false)}
        results={results}
      />

      {/* Spacious Modern Luxury Footer */}
      <footer className="border-t border-white/10 py-12 text-xs text-slate-400 glass-luxury mt-24 relative z-10 mx-4 sm:mx-8 rounded-t-[36px]">
        <div className="max-w-7xl mx-auto px-6 sm:px-10 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center space-x-3">
            <span className="text-xl font-bold text-white tracking-tight">Pack<span className="text-[#ffd905]">AI</span></span>
            <span className="tag-pill tag-pill-yellow text-[9px] py-0.5 px-2.5 font-mono">v1.0 Production</span>
            <span className="text-slate-400 hidden sm:inline">• Autonomous Food Packaging Decision Intelligence</span>
          </div>
          <div className="flex flex-wrap items-center gap-3 text-xs font-mono text-slate-400">
            <span>Arrhenius Mass Transfer</span>
            <span>•</span>
            <span>ASTM D3985 / F1249</span>
            <span>•</span>
            <span className="text-[#ffd905]">Zero Target Leakage</span>
          </div>
        </div>
      </footer>

    </div>
  );
};

export default App;
