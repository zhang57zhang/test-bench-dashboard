'use client';

import { useEffect, useState } from 'react';
import { aiAssistantAPI, AIAssistantMetrics } from '@/lib/ai-assistant-api';

export default function AIAssistantDashboard() {
  const [metrics, setMetrics] = useState<AIAssistantMetrics | null>(null);
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
      const data = await aiAssistantAPI.getMetrics(period);
      setMetrics(data);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching AI assistant metrics:', err);
      setError(err.message || '加载数据失败');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
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
            className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            🔄 重试
          </button>
        </div>
      </div>
    );
  }

  const { overview, by_activity, by_period } = metrics;

  // 颜色配置
  const activityColors = [
    'from-blue-500 to-blue-600',
    'from-green-500 to-green-600',
    'from-purple-500 to-purple-600',
    'from-orange-500 to-orange-600',
    'from-cyan-500 to-cyan-600',
    'from-pink-500 to-pink-600',
    'from-indigo-500 to-indigo-600',
    'from-red-500 to-red-600',
    'from-teal-500 to-teal-600',
    'from-yellow-500 to-yellow-600',
    'from-violet-500 to-violet-600',
  ];

  return (
    <div className="flex-1 flex flex-col p-6">
      {/* 页面标题和周期选择 */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">AI辅助看板</h2>
          <p className="text-gray-600 mt-1">AI辅助测试全流程统计分析</p>
        </div>
        
        {/* 周期选择器 */}
        <div className="flex gap-2">
          {['day', 'week', 'month', 'year'].map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                period === p
                  ? 'bg-purple-600 text-white'
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
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-lg shadow-lg">
          <p className="text-sm opacity-90">总辅助次数</p>
          <p className="text-3xl font-bold mt-2">{overview.total_assistances.toLocaleString()}</p>
          <p className="text-xs opacity-75 mt-1">AI辅助总次数</p>
        </div>
        
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow-lg">
          <p className="text-sm opacity-90">节省人力</p>
          <p className="text-3xl font-bold mt-2">{Math.floor(overview.total_manual_effort_saved_hours / 8)}</p>
          <p className="text-xs opacity-75 mt-1">人天 (8h/天)</p>
        </div>
        
        <div className="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-lg shadow-lg">
          <p className="text-sm opacity-90">活动类型</p>
          <p className="text-3xl font-bold mt-2">{overview.total_activities}</p>
          <p className="text-xs opacity-75 mt-1">辅助活动种类</p>
        </div>
        
        <div className="bg-gradient-to-br from-orange-500 to-orange-600 text-white p-6 rounded-lg shadow-lg">
          <p className="text-sm opacity-90">最常用</p>
          <p className="text-xl font-bold mt-2 truncate">{overview.top_activity}</p>
          <p className="text-xs opacity-75 mt-1">高频活动</p>
        </div>
      </div>

      {/* 活动类型统计 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* 左侧：活动列表 */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-4 border-b bg-gray-50">
            <h3 className="font-semibold text-gray-900">活动类型统计</h3>
          </div>
          
          <div className="p-4 space-y-3 max-h-96 overflow-auto">
            {by_activity.map((activity, index) => (
              <div key={index} className="flex items-center gap-3">
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-900">{activity.name}</span>
                    <span className="text-sm text-gray-600">{activity.count}</span>
                  </div>
                  <div className="relative h-2 bg-gray-200 rounded overflow-hidden">
                    <div
                      className={`absolute h-full bg-gradient-to-r ${activityColors[index % activityColors.length]}`}
                      style={{ width: `${activity.percentage}%` }}
                    />
                  </div>
                </div>
                <span className="text-xs text-gray-500 w-12 text-right">
                  {activity.percentage}%
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* 右侧：饼图占位（简化为列表） */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-4 border-b bg-gray-50">
            <h3 className="font-semibold text-gray-900">Top 5 活动占比</h3>
          </div>
          
          <div className="p-4">
            <div className="grid grid-cols-1 gap-3">
              {by_activity.slice(0, 5).map((activity, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-lg bg-gradient-to-r ${activityColors[index]} text-white`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">{activity.name}</p>
                      <p className="text-sm opacity-90 mt-1">{activity.count} 次</p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold">{activity.percentage}%</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 趋势图表（简化版） */}
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="font-semibold text-gray-900 mb-4">辅助趋势（最近30天）</h3>
        <div className="h-32 flex items-end gap-1">
          {by_period.slice(-30).map((day, index) => {
            const maxCount = Math.max(...by_period.map(d => d.total_count));
            const height = (day.total_count / maxCount) * 100;
            
            return (
              <div
                key={index}
                className="flex-1 bg-purple-400 hover:bg-purple-500 rounded-t transition-colors cursor-pointer"
                style={{ height: `${height}%` }}
                title={`${day.date}: ${day.total_count} 次辅助`}
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
