/**
 * 看板类型定义
 */

export type DashboardType = 
  | 'test-bench'      // 测试台架看板
  | 'dvp'             // DVP进度看板
  | 'automation'      // 自动化测试看板（预留）
  | 'ai-assistant';   // AI辅助看板（预留）

export interface DashboardConfig {
  id: DashboardType;
  name: string;
  icon: string;
  description: string;
  available: boolean;
  badge?: string;
}

export const DASHBOARD_CONFIGS: DashboardConfig[] = [
  {
    id: 'test-bench',
    name: '测试台架看板',
    icon: '🏭',
    description: '智能测试台架工厂数字孪生看板',
    available: true,
  },
  {
    id: 'dvp',
    name: 'DVP进度看板',
    icon: '📊',
    description: '车辆控制器DVP进度监控',
    available: true,
  },
  {
    id: 'automation',
    name: '自动化测试看板',
    icon: '🤖',
    description: '自动化测试执行监控（开发中）',
    available: false,
    badge: '即将推出',
  },
  {
    id: 'ai-assistant',
    name: 'AI辅助看板',
    icon: '🧠',
    description: 'AI智能分析与辅助决策（开发中）',
    available: false,
    badge: '即将推出',
  },
];

export const getDashboardConfig = (type: DashboardType): DashboardConfig => {
  return DASHBOARD_CONFIGS.find(d => d.id === type) || DASHBOARD_CONFIGS[0];
};
