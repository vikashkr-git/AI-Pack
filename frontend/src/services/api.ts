import {
  FoodProfile,
  PackagingItem,
  ScientificSource,
  ModelInfo,
  RecommendationResponse,
  FoodInputFormState
} from '../types';

const API_BASE = 'https://ai-pack-c7vn.onrender.com/api/v1';

export async function fetchHealth(): Promise<{ status: string }> {
  try {
    const res = await fetch('https://ai-pack-c7vn.onrender.com/health');
    if (!res.ok) throw new Error('Health check failed');
    return await res.json();
  } catch (err) {
    return { status: 'offline' };
  }
}

export async function fetchFoods(): Promise<FoodProfile[]> {
  const res = await fetch(`${API_BASE}/foods`);
  if (!res.ok) throw new Error('Failed to fetch food catalog');
  return res.json();
}

export async function fetchPackaging(): Promise<PackagingItem[]> {
  const res = await fetch(`${API_BASE}/packaging`);
  if (!res.ok) throw new Error('Failed to fetch packaging catalog');
  return res.json();
}

export async function fetchSources(): Promise<ScientificSource[]> {
  const res = await fetch(`${API_BASE}/sources`);
  if (!res.ok) throw new Error('Failed to fetch sources');
  return res.json();
}

export async function fetchModelInfo(): Promise<ModelInfo> {
  const res = await fetch(`${API_BASE}/model-info`);
  if (!res.ok) throw new Error('Failed to fetch model info');
  return res.json();
}

export async function validateInput(partial: Partial<FoodInputFormState>): Promise<{
  is_valid: boolean;
  warnings: string[];
  suggested_values?: Partial<FoodInputFormState>;
}> {
  const res = await fetch(`${API_BASE}/validate-input`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(partial)
  });
  if (!res.ok) throw new Error('Input validation failed');
  return res.json();
}

export async function requestRecommendation(payload: FoodInputFormState): Promise<RecommendationResponse> {
  const res = await fetch(`${API_BASE}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({ detail: 'Network error occurred' }));
    throw new Error(errData.detail || 'Failed to generate recommendations');
  }
  return res.json();
}

export async function fetchHistory(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/history`);
  if (!res.ok) throw new Error('Failed to fetch history');
  return res.json();
}
