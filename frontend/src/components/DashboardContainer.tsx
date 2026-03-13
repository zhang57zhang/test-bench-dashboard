'use client';

import { useState } from 'react';
import { DashboardType } from '@/types/dashboard';
import Header from '@/components/Header';
import TestBenchDashboard from '@/components/TestBenchDashboard';
import DVPDashboard from '@/components/DVPDashboard';
import AutomationDashboard from '@/components/AutomationDashboard';
import AIAssistantDashboard from '@/components/AIAssistantDashboard';

export default function DashboardContainer() {
  const [currentDashboard, setCurrentDashboard] = useState<DashboardType>('test-bench');

  const renderDashboard = () => {
    switch (currentDashboard) {
      case 'test-bench':
        return <TestBenchDashboard />;
      case 'dvp':
        return <DVPDashboard />;
      case 'automation':
        return <AutomationDashboard />;
      case 'ai-assistant':
        return <AIAssistantDashboard />;
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
