'use client';

import { useState, useRef, useEffect } from 'react';
import { DashboardType, DASHBOARD_CONFIGS, getDashboardConfig } from '@/types/dashboard';

interface DashboardSelectorProps {
  currentDashboard: DashboardType;
  onDashboardChange: (type: DashboardType) => void;
}

export default function DashboardSelector({ 
  currentDashboard, 
  onDashboardChange 
}: DashboardSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const currentConfig = getDashboardConfig(currentDashboard);

  // 点击外部关闭下拉菜单
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (type: DashboardType) => {
    const config = getDashboardConfig(type);
    if (config.available) {
      onDashboardChange(type);
      setIsOpen(false);
    }
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* 当前看板按钮 */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors"
      >
        <span className="text-xl">{currentConfig.icon}</span>
        <span className="font-medium">{currentConfig.name}</span>
        <svg
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* 下拉菜单 */}
      {isOpen && (
        <div className="absolute top-full mt-2 w-72 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden z-50">
          <div className="p-2 bg-gray-50 border-b border-gray-200">
            <p className="text-xs text-gray-600 font-medium">选择看板</p>
          </div>
          
          <div className="py-2">
            {DASHBOARD_CONFIGS.map((config) => (
              <button
                key={config.id}
                onClick={() => handleSelect(config.id)}
                disabled={!config.available}
                className={`w-full flex items-start gap-3 px-4 py-3 text-left transition-colors ${
                  config.available
                    ? 'hover:bg-blue-50 cursor-pointer'
                    : 'opacity-50 cursor-not-allowed'
                } ${currentDashboard === config.id ? 'bg-blue-50' : ''}`}
              >
                <span className="text-2xl">{config.icon}</span>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-gray-900">{config.name}</span>
                    {config.badge && (
                      <span className="px-2 py-0.5 text-[10px] font-medium bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-full">
                        {config.badge}
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-gray-500 mt-0.5">{config.description}</p>
                </div>
                
                {currentDashboard === config.id && config.available && (
                  <svg className="w-5 h-5 text-blue-600 mt-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
            ))}
          </div>
          
          <div className="p-3 bg-gray-50 border-t border-gray-200">
            <p className="text-[10px] text-gray-500 text-center">
              💡 更多看板功能正在开发中，敬请期待
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
