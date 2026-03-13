/**
 * 自动化测试看板 API 客户端
 */

import axios from 'axios';
import { loadConfig } from './config';

const automationApi = axios.create({
  baseURL: 'http://localhost:8000/api/v1/automation',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 动态设置 baseURL
automationApi.interceptors.request.use(async (config) => {
  try {
    const appConfig = await loadConfig();
    config.baseURL = appConfig.apiUrl + '/automation';
  } catch (error) {
    console.warn('[Automation API] Using default baseURL');
  }
  return config;
});

// ============ 数据类型 ============

export interface AutomationStats {
  total_test_cases: number;
  total_execution_time_hours: number;
  total_manual_effort_saved_hours: number;
  total_projects: number;
  pass_rate: number;
}

export interface ProjectAutomationStats {
  project_name: string;
  test_cases: number;
  execution_time_hours: number;
  pass_rate: number;
  failed_count: number;
}

export interface DailyStats {
  date: string;
  test_cases: number;
  execution_time_hours: number;
  pass_rate: number;
  failed_count: number;
}

export interface AutomationMetrics {
  overview: AutomationStats;
  by_project: ProjectAutomationStats[];
  by_period: DailyStats[];
}

// ============ API 方法 ============

export const automationAPI = {
  getMetrics: async (period: string = 'day', project?: string): Promise<AutomationMetrics> => {
    const params = new URLSearchParams({ period });
    if (project) params.append('project', project);
    
    const response = await automationApi.get(`/metrics?${params}`);
    return response.data;
  },

  getOverview: async (): Promise<AutomationStats> => {
    const response = await automationApi.get('/overview');
    return response.data;
  },

  getByProject: async (): Promise<ProjectAutomationStats[]> => {
    const response = await automationApi.get('/by-project');
    return response.data;
  },

  getByPeriod: async (period: string = 'day'): Promise<DailyStats[]> => {
    const response = await automationApi.get(`/by-period?period=${period}`);
    return response.data;
  },
};

export default automationApi;
