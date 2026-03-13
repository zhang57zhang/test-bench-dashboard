'use client';

import { useEffect, useState } from 'react';
import { automationAPI, AutomationMetrics } from '@/lib/automation-api';

export default function AutomationDashboard() {
  const [metrics, setMetrics] = useState<AutomationMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [period, setPeriod] = useState('month');

  useEffect(() => {
    fetchMetrics();
    
    // 定时刷新（每5分钟）
    const interval = setInterval(fetchMetrics, 300000);
    return () => clearInterval(interval);
  }, [period]);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      const data = await automationAPI.getMetrics(period);
      setMetrics(data);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching automation metrics:', err);
      setError(err.message || '加载数据失败');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">加载中...</p>
        </div>
      </div>
    );
  }

  if (error || !metrics) {
    return (
      <div className="flex-1 flex items-center justify-center p-6">
        <div className="text-center">
          <span className="text-6xl mb-4 block">⚠️</span>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">数据加载失败</h2>
          <p className="text-gray-600 mb-6">{error || '未知错误'}</p>
          <button
            onClick={fetchMetrics}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            🔄 重试
          </button>
        </div>
      </div>
    );
  }

  const { overview, by_project, by_period } = metrics;

  return (
    <div className="flex-1 flex flex-col p-6">
      {/* 页面标题和周期选择 */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">自动化测试看板</h2>
          <p className="text-gray-600 mt-1">实时监控自动化测试执行情况</p>
        </div>
        
        {/* 周期选择器 */}
        <div className="flex gap-2">
          {['day', 'week', 'month', 'year'].map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                period === p
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {p === 'day' && '按天'}
              {p === 'week' && '按周'}
              {p === 'month' && '按月'}
              {p === 'year' && '按年'}
            </button>
          ))}
        </div>
      </div>

      {/* 顶部总览卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow-lg">
          <p className="text-sm opacity-90">总用例数</p>
          <p className="text-3xl font-bold mt-2">{overview.total_test_cases.toLocaleString()}</p>
          <p className="text-xs opacity-75 mt-1">累计执行</p>
        </div>
        
        <div className="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-lg shadow-lg">
          <p className="text-sm opacity-90">总执行时长</p>
          <p className="text-3xl font-bold mt-2">{overview.total_execution_time_hours.toFixed(1)}</p>
          <p className="text-xs opacity-75 mt-1">小时</p>
        </div>
        
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-lg shadow-lg">
          <p className="text-sm opacity-90">节省人力</p>
          <p className="text-3xl font-bold mt-2">{Math.floor(overview.total_manual_effort_saved_hours / 8)}</p>
          <p className="text-xs opacity-75 mt-1">人天 (8h/天)</p>
        </div>
        
        <div className="bg-gradient-to-br from-orange-500 to-orange-600 text-white p-6 rounded-lg shadow-lg">
          <p className="text-sm opacity-90">通过率</p>
          <p className="text-3xl font-bold mt-2">{overview.pass_rate}%</p>
          <p className="text-xs opacity-75 mt-1">成功率</p>
        </div>
        
        <div className="bg-gradient-to-br from-cyan-500 to-cyan-600 text-white p-6 rounded-lg shadow-lg">
          <p className="text-sm opacity-90">项目数</p>
          <p className="text-3xl font-bold mt-2">{overview.total_projects}</p>
          <p className="text-xs opacity-75 mt-1">活跃项目</p>
        </div>
      </div>

      {/* 项目统计列表 */}
      <div className="bg-white rounded-lg shadow flex-1 overflow-auto mb-6">
        <div className="p-4 border-b bg-gray-50 flex items-center justify-between">
          <h3 className="font-semibold text-gray-900">项目执行统计</h3>
          <span className="text-sm text-gray-500">共 {by_project.length} 个项目</span>
        </div>
        
        <div className="p-4">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-700">项目名称</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">用例数</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">执行时长(h)</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">通过率</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">失败数</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-700">进度</th>
                </tr>
              </thead>
              <tbody>
                {by_project.map((project, index) => (
                  <tr key={index} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-4 text-sm font-medium text-gray-900">
                      {project.project_name}
                    </td>
                    <td className="py-3 px-4 text-sm text-right text-gray-700">
                      {project.test_cases.toLocaleString()}
                    </td>
                    <td className="py-3 px-4 text-sm text-right text-gray-700">
                      {project.execution_time_hours.toFixed(2)}
                    </td>
                    <td className="py-3 px-4 text-sm text-right">
                      <span className={`font-medium ${
                        project.pass_rate >= 95 ? 'text-green-600' :
                        project.pass_rate >= 90 ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {project.pass_rate}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-sm text-right text-red-600">
                      {project.failed_count}
                    </td>
                    <td className="py-3 px-4">
                      <div className="relative h-2 bg-gray-200 rounded overflow-hidden">
                        <div
                          className={`absolute h-full ${
                            project.pass_rate >= 95 ? 'bg-green-500' :
                            project.pass_rate >= 90 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${project.pass_rate}%` }}
                        />
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* 趋势图表（简化版） */}
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="font-semibold text-gray-900 mb-4">执行趋势（最近30天）</h3>
        <div className="h-32 flex items-end gap-1">
          {by_period.slice(-30).map((day, index) => {
            const maxCases = Math.max(...by_period.map(d => d.test_cases));
            const height = (day.test_cases / maxCases) * 100;
            
            return (
              <div
                key={index}
                className="flex-1 bg-blue-400 hover:bg-blue-500 rounded-t transition-colors cursor-pointer"
                style={{ height: `${height}%` }}
                title={`${day.date}: ${day.test_cases} 用例, 通过率 ${day.pass_rate}%`}
              />
            );
          })}
        </div>
        <div className="flex justify-between mt-2 text-xs text-gray-500">
          <span>{by_period[0]?.date}</span>
          <span>{by_period[by_period.length - 1]?.date}</span>
        </div>
      </div>
    </div>
  );
}
