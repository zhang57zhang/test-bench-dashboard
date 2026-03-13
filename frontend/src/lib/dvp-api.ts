/**
 * DVP API 客户端
 * 用于与 DVP 后端通信（本地实现）
 */

import axios from 'axios';
import { loadConfig } from './config';

// DVP API 基础配置
const dvpApi = axios.create({
  baseURL: 'http://localhost:8000/api/v1/dvp',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 动态设置 baseURL
dvpApi.interceptors.request.use(async (config) => {
  try {
    const appConfig = await loadConfig();
    config.baseURL = appConfig.apiUrl + '/dvp';
  } catch (error) {
    console.warn('[DVP API] Using default baseURL');
  }
  return config;
});

// 响应拦截器 - 统一错误处理
dvpApi.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[DVP API] Error:', error);
    throw error;
  }
);

// ============ 项目 API ============

export interface Project {
  project_id: string;
  name: string;
  total_experiments: number;
  total_devices: number;
  progress: number;
  param_checked: boolean;
  is_interrupted: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProjectStatistics {
  total_projects: number;
  running_projects: number;
  completed_projects: number;
  interrupted_projects: number;
  average_progress: number;
}

export const projectAPI = {
  getAll: async (skip = 0, limit = 100): Promise<Project[]> => {
    const response = await dvpApi.get(`/projects?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getById: async (projectId: string): Promise<Project> => {
    const response = await dvpApi.get(`/projects/${projectId}`);
    return response.data;
  },

  getStatistics: async (): Promise<ProjectStatistics> => {
    const response = await dvpApi.get('/statistics');
    return response.data;
  },

  regenerate: async (): Promise<{ message: string; count: number }> => {
    const response = await dvpApi.post('/projects/generate');
    return response.data;
  },
};

// ============ 实验组 API ============

export interface Experiment {
  project_id: string;
  experiment_id: string;
  name: string;
  total_devices: number;
  completed_devices: number;
  progress: number;
  param_checked: boolean;
  is_interrupted: boolean;
}

export const experimentAPI = {
  getByProject: async (projectId: string): Promise<Experiment[]> => {
    const response = await dvpApi.get(`/projects/${projectId}/experiments`);
    return response.data;
  },

  getById: async (projectId: string, experimentId: string): Promise<Experiment> => {
    const response = await dvpApi.get(`/projects/${projectId}/experiments/${experimentId}`);
    return response.data;
  },
};

// ============ 设备 API ============

export interface Device {
  project_id: string;
  experiment_id: string;
  device_id: string;
  name: string;
  status: 'running' | 'idle' | 'error' | 'completed';
  progress: number;
}

export const deviceAPI = {
  getByExperiment: async (projectId: string, experimentId: string): Promise<Device[]> => {
    const response = await dvpApi.get(`/projects/${projectId}/experiments/${experimentId}/devices`);
    return response.data;
  },

  getById: async (projectId: string, experimentId: string, deviceId: string): Promise<Device> => {
    const response = await dvpApi.get(`/projects/${projectId}/experiments/${experimentId}/devices/${deviceId}`);
    return response.data;
  },
};

export default dvpApi;
