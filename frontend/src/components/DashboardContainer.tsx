'use client';

import { useState } from 'react';
import { DashboardType } from '@/types/dashboard';
import Header from '@/components/Header';
import TestBenchDashboard from '@/components/TestBenchDashboard';
import DVPDashboard from '@/components/DVPDashboard';

export default function DashboardContainer() {
  const [currentDashboard, setCurrentDashboard] = useState<DashboardType>('test-bench');

  const renderDashboard = () => {
    switch (currentDashboard) {
      case 'test-bench':
        return <TestBenchDashboard />;
      case 'dvp':
        return <DVPDashboard />;
      case 'automation':
        return (
          <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="text-center">
              <span className="text-6xl mb-4 block">🤖</span>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">自动化测试看板</h2>
              <p className="text-gray-600">功能开发中，敬请期待...</p>
            </div>
          </div>
        );
      case 'ai-assistant':
        return (
          <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="text-center">
              <span className="text-6xl mb-4 block">🧠</span>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">AI辅助看板</h2>
              <p className="text-gray-600">功能开发中，敬请期待...</p>
            </div>
          </div>
        );
      default:
        return <TestBenchDashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* 统一的顶部导航 */}
      <Header 
        currentDashboard={currentDashboard}
        onDashboardChange={setCurrentDashboard}
      />
      
      {/* 看板内容 */}
      {renderDashboard()}
    </div>
  );
}
