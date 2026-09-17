export interface TechnicalSpecs {
  thickness_um: number;
  otr_value: number;
  otr_unit: string;
  otr_class: string;
  wvtr_value: number;
  wvtr_unit: string;
  wvtr_class: string;
  co2_permeability?: number;
  puncture_resistance_n?: number;
  tensile_strength_mpa?: number;
  sealing_temp_range_c?: string;
  seal_strength_n_15mm?: number;
  min_temperature_c?: number;
  breathable?: boolean;
  micro_perforated?: boolean;
  map_suitable?: boolean;
  light_barrier?: string;
}

export interface SustainabilityProfile {
  recyclability_class?: string;
  recyclability_stream?: string;
  recycled_content_pct?: number;
  biodegradable?: boolean;
  compostable?: boolean;
  bio_based_pct?: number;
  relative_cost_index?: number;
}

export interface MaterialLayer {
  layer_no: number;
  position?: string;
  name: string;
  thickness_um?: number;
  function?: string;
  work?: string;
}

export interface MaterialComposition {
  layers: MaterialLayer[];
  why_this_material_short: string;
}

export interface ProcurementMarket {
  estimated_cost_per_kg_inr?: string;
  estimated_cost_per_pouch_inr?: string;
  approx_cost_usd?: string;
  moq?: string;
  lead_time?: string;
  sourcing_channels: string[];
}

export interface QualityInspectionPoint {
  check_item: string;
  standard?: string;
  acceptance_criteria: string;
  how_to_test: string;
  criticality: "Critical" | "Major";
}

export interface MaterialDurability {
  virgin_material_shelf_life: string;
  packaged_product_protection_duration: string;
  unfilled_storage_conditions?: string;
  aging_failure_modes?: string;
}

export interface RecommendationItem {
  rank: number;
  id: string;
  short_name: string;
  name: string;
  structure: string;
  category: string;
  suitability_score: number;
  sample_photo_url?: string;
  technical_specifications: TechnicalSpecs;
  sustainability_profile: SustainabilityProfile;
  scientific_provenance: {
    source_ref?: string;
    astm_standard?: string;
    doi?: string;
  };
  material_composition?: MaterialComposition;
  procurement_market?: ProcurementMarket;
  quality_inspection_checklist?: QualityInspectionPoint[];
  material_durability?: MaterialDurability;
  explanation: {
    reasons_why: string[];
    cautions_limitations: string[];
    radar_metrics: {
      oxygen_barrier: number;
      moisture_barrier: number;
      mechanical_strength: number;
      thermal_stability: number;
      sustainability: number;
      cost_efficiency: number;
    };
    suitability_score: number;
    is_top_choice: boolean;
  };
}

export interface SustainableAlternative {
  id: string;
  name: string;
  short_name: string;
  structure: string;
  suitability_score: number;
  sample_photo_url?: string;
  eco_highlights: {
    bio_based_pct?: number;
    recycled_content_pct?: number;
    recyclability_stream?: string;
    compostable?: boolean;
  };
  trade_off_analysis: string;
  material_composition?: MaterialComposition;
  procurement_market?: ProcurementMarket;
  material_durability?: MaterialDurability;
}

export interface ScientificRequirements {
  commodity: string;
  category: string;
  is_fresh_produce: boolean;
  is_frozen: boolean;
  is_chilled: boolean;
  is_long_transit: boolean;
  water_activity_aw_estimated: number;
  vapor_pressure_delta_kpa: number;
  oxidation_risk_index: number;
  target_wvtr_range: { min: number; max: number; unit: string };
  wvtr_class_demand: string;
  moisture_risk_analysis: string;
  target_otr_range: { min: number; max: number; unit: string };
  otr_class_demand: string;
  oxygen_risk_analysis: string;
  thermal_mechanical_demands: {
    min_operating_temp_c: number;
    required_puncture_n: number;
    required_tensile_mpa: number;
    thermal_risk: string;
  };
  map_recommendations: {
    active_mode?: boolean;
    respiration_severity?: string;
    respiration_rate_mg_co2_kg_hr?: number;
    breathable_packaging_required?: boolean;
    micro_perforation_recommended?: boolean;
    recommended_headspace_gas?: string;
    scientific_rationale?: string;
    map_suitable?: boolean;
  };
}

export interface RecommendationResponse {
  query_summary: {
    commodity: string;
    category: string;
    storage_type: string;
    transportation: string;
    target_shelf_life_days: number;
    optimization_goal: string;
  };
  scientific_requirements: ScientificRequirements;
  top_recommendations: RecommendationItem[];
  sustainable_alternative?: SustainableAlternative;
  disqualified_candidates?: Array<{
    id: string;
    short_name: string;
    name: string;
    reasons: string[];
  }>;
  confidence_assessment: {
    overall_confidence: string;
    score_separation: number;
    evidence_sources_count: number;
    empirical_measurements_analyzed: number;
    model_version: string;
  };
  disclaimer: string;
}

export interface FoodProfile {
  id: number;
  commodity: string;
  category: string;
  moisture_pct: number;
  fat_pct: number;
  protein_pct: number;
  ph: number;
  respiration_rate_val: number;
  respiration_rate_class: string;
  standard_shelf_life_days: number;
  optimal_storage_type: string;
  optimal_temp_c: number;
  optimal_rh_pct: number;
  map_suitable: boolean;
  optimal_map_gas?: string;
  primary_degradation_modes?: string[];
  critical_barrier_needs?: Record<string, string>;
}

export interface PackagingItem {
  id: string;
  name: string;
  short_name: string;
  structure: string;
  total_thickness_um: number;
  category: string;
  otr_value: number;
  otr_class: string;
  wvtr_value: number;
  wvtr_class: string;
  co2_permeability?: number;
  tensile_strength_mpa?: number;
  puncture_resistance_n?: number;
  heat_seal_temp_c_min?: number;
  heat_seal_temp_c_max?: number;
  seal_strength_n_15mm?: number;
  min_temperature_c?: number;
  max_temperature_c?: number;
  breathable?: boolean;
  micro_perforated?: boolean;
  map_suitable?: boolean;
  light_barrier?: string;
  recyclability_class?: string;
  recyclability_stream?: string;
  recycled_content_pct?: number;
  biodegradable?: boolean;
  compostable?: boolean;
  bio_based_pct?: number;
  cost_index_relative?: number;
  primary_applications?: string[];
  astm_standard?: string;
  doi?: string;
  sample_photo_url?: string;
  material_composition?: MaterialComposition;
  procurement_market?: ProcurementMarket;
  quality_inspection_checklist?: QualityInspectionPoint[];
  material_durability?: MaterialDurability;
}

export interface ScientificSource {
  id: string;
  source_name: string;
  title: string;
  authors?: string;
  year?: number;
  publisher_or_journal?: string;
  url?: string;
  doi?: string;
  scope?: string;
  confidence_score: number;
}

export interface ModelInfo {
  model_status: string;
  model_version: string;
  evaluation_strategy: string;
  model_comparisons: Record<string, any>;
  final_model_metrics: {
    mean_mae: number;
    mean_rmse: number;
    mean_r2: number;
    mean_top1_accuracy: number;
    mean_top3_accuracy: number;
    mean_ndcg_at_3: number;
  };
  feature_importances: Record<string, number>;
  total_training_samples: number;
  dataset_audit_summary: {
    total_raw_rows: number;
    flagged_anomalies_count: number;
    target_leakage_finding: string;
    architectural_remedy: string;
  };
}

export interface FoodInputFormState {
  commodity: string;
  category: string;
  moisture_pct: number;
  fat_pct: number;
  protein_pct: number;
  ph: number;
  respiration_rate: number;
  shelf_life_days: number;
  storage_temp_c: number;
  relative_humidity_pct: number;
  storage_type: "Ambient" | "Chilled" | "Frozen";
  transportation: "Normal" | "Refrigerated" | "Long_Distance";
  optimization_goal: "Performance" | "Balanced" | "Sustainability" | "Cost_Optimized";
}
