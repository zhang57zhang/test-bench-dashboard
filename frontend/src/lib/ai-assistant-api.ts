/**
 * AI辅助看板 API 客户端
 */

import axios from 'axios';
import { loadConfig } from './config';

const aiAssistantApi = axios.create({
  baseURL: 'http://localhost:8000/api/v1/ai-assistant',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 动态设置 baseURL
aiAssistantApi.interceptors.request.use(async (config) => {
  try {
    const appConfig = await loadConfig();
    config.baseURL = appConfig.apiUrl + '/ai-assistant';
  } catch (error) {
    console.warn('[AI Assistant API] Using default baseURL');
  }
  return config;
});

// ============ 数据类型 ============

export interface AIActivity {
  name: string;
  count: number;
  percentage: number;
}

export interface AIOverview {
  total_assistances: number;
  total_manual_effort_saved_hours: number;
  total_activities: number;
  top_activity: string;
}

export interface DailyAIStats {
  date: string;
  total_count: number;
  by_activity: Record<string, number>;
}

export interface AIAssistantMetrics {
  overview: AIOverview;
  by_activity: AIActivity[];
  by_period: DailyAIStats[];
}

// ============ API 方法 ============

export const aiAssistantAPI = {
  getMetrics: async (period: string = 'day'): Promise<AIAssistantMetrics> => {
    const response = await aiAssistantApi.get(`/metrics?period=${period}`);
    return response.data;
  },

  getOverview: async (): Promise<AIOverview> => {
    const response = await aiAssistantApi.get('/overview');
    return response.data;
  },

  getByActivity: async (): Promise<AIActivity[]> => {
    const response = await aiAssistantApi.get('/by-activity');
    return response.data;
  },

  getByPeriod: async (period: string = 'day'): Promise<DailyAIStats[]> => {
    const response = await aiAssistantApi.get(`/by-period?period=${period}`);
    return response.data;
  },
};

export default aiAssistantApi;
