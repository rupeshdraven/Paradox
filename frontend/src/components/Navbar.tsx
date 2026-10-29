import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  User, 
  Target, 
  Sparkles, 
  TrendingUp, 
  BookOpen, 
  Bell, 
  ChevronDown, 
  Menu, 
  X, 
  RotateCcw,
  Bot,
  ShieldCheck
} from 'lucide-react';
import { useFinancial, AppPage } from '../context/FinancialContext';

export const Navbar: React.FC = () => {
  const { currentPage, setCurrentPage, profile, resetToDemo, setIsChatOpen, notification } = useFinancial();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [showNotificationToast, setShowNotificationToast] = useState(false);

  const navItems: Array<{ id: AppPage; label: string; icon: React.ReactNode }> = [
    { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard className="w-4 h-4" /> },
    { id: 'onboarding-profile', label: 'My Profile', icon: <User className="w-4 h-4" /> },
    { id: 'onboarding-goals', label: 'Goals', icon: <Target className="w-4 h-4" /> },
    { id: 'recommendations', label: 'Recommendations', icon: <Sparkles className="w-4 h-4" /> },
    { id: 'insights', label: 'Insights', icon: <TrendingUp className="w-4 h-4" /> },
    { id: 'learn', label: 'Learn', icon: <BookOpen className="w-4 h-4" /> },
  ];

  const handleNavClick = (page: AppPage) => {
    setCurrentPage(page);
    setIsMobileMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-[#DCE5EC] shadow-xs">
      {/* Toast Notification */}
      {notification && (
        <div className="bg-[#28B89A] text-white text-xs py-1.5 px-4 text-center font-medium animate-fadeIn">
          ✓ {notification}
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => handleNavClick('dashboard')}>
            <div className="flex items-end gap-0.5 h-7">
              <div className="w-1.5 h-3 bg-[#28B89A] rounded-xs" />
              <div className="w-1.5 h-5 bg-[#28B89A] rounded-xs" />
              <div className="w-1.5 h-6 bg-[#092B49] rounded-xs" />
              <div className="w-1.5 h-7 bg-[#092B49] rounded-xs" />
            </div>
            <div className="flex items-center">
              <span className="text-xl font-bold text-[#092B49] tracking-tight">FinWise</span>
              <span className="text-xl font-bold text-[#28B89A] ml-1">AI</span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = currentPage === item.id || 
                (item.id === 'onboarding-profile' && currentPage.startsWith('onboarding-'));
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-[#EEF6FF] text-[#092B49] font-semibold shadow-xs'
                      : 'text-[#64748B] hover:text-[#102A43] hover:bg-slate-50'
                  }`}
                >
                  <span className={isActive ? 'text-[#28B89A]' : 'text-[#64748B]'}>{item.icon}</span>
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Right Actions */}
          <div className="flex items-center gap-3">
            {/* Ask AI Copilot button */}
            <button
              onClick={() => setIsChatOpen(true)}
              className="flex items-center gap-2 px-3 py-1.5 bg-[#DDF7F0] hover:bg-[#cbf1e6] text-[#092B49] rounded-full text-xs font-semibold border border-[#28B89A]/30 transition-all shadow-xs cursor-pointer"
              title="Open AI Financial Copilot"
            >
              <Bot className="w-3.5 h-3.5 text-[#28B89A]" />
              <span className="hidden sm:inline">Ask Copilot</span>
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#28B89A] opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-[#28B89A]"></span>
              </span>
            </button>

            {/* Notification Bell */}
            <div className="relative">
              <button 
                onClick={() => setShowNotificationToast(!showNotificationToast)}
                className="relative p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-full transition-colors"
                title="Notifications"
              >
                <Bell className="w-5 h-5 text-[#64748B]" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-[#28B89A] rounded-full ring-2 ring-white"></span>
              </button>

              {showNotificationToast && (
                <div className="absolute right-0 mt-2 w-72 bg-white rounded-xl shadow-lg border border-[#DCE5EC] p-3 text-xs z-50 animate-fadeIn">
                  <div className="font-semibold text-[#102A43] mb-1 flex items-center justify-between">
                    <span>Notifications</span>
                    <span className="text-[10px] text-[#28B89A] bg-[#DDF7F0] px-1.5 py-0.5 rounded">Active</span>
                  </div>
                  <p className="text-[#64748B] text-[11px] mt-1">
                    ✓ Financial profile calibrated for <strong>{profile.name}</strong>.
                  </p>
                  <p className="text-[#64748B] text-[11px] mt-1">
                    ✓ Emergency fund reserve target evaluated (covers {roundMonths(profile.existing_savings, profile.monthly_expenses)} mo).
                  </p>
                </div>
              )}
            </div>

            {/* User Dropdown */}
            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center gap-2 p-1 pl-2 pr-2.5 rounded-full hover:bg-slate-100 transition-colors border border-transparent hover:border-slate-200"
              >
                <div className="w-8 h-8 rounded-full bg-[#092B49] text-white flex items-center justify-center font-bold text-sm shadow-xs">
                  {profile.name.charAt(0).toUpperCase()}
                </div>
                <span className="text-sm font-medium text-[#102A43] hidden sm:inline">{profile.name}</span>
                <ChevronDown className="w-3.5 h-3.5 text-[#64748B]" />
              </button>

              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-[#DCE5EC] py-2 z-50 animate-fadeIn">
                  <div className="px-4 py-2 border-b border-slate-100">
                    <p className="text-xs text-[#64748B]">Signed in as</p>
                    <p className="text-sm font-semibold text-[#102A43]">{profile.name}</p>
                    <div className="flex items-center gap-1 mt-1 text-[11px] text-[#28B89A]">
                      <ShieldCheck className="w-3 h-3" /> Demo Account Active
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      handleNavClick('onboarding-profile');
                      setIsUserMenuOpen(false);
                    }}
                    className="w-full text-left px-4 py-2 text-xs text-[#102A43] hover:bg-slate-50 flex items-center gap-2"
                  >
                    <User className="w-3.5 h-3.5 text-[#64748B]" /> Edit Investor Profile
                  </button>
                  <button
                    onClick={() => {
                      resetToDemo();
                      setIsUserMenuOpen(false);
                    }}
                    className="w-full text-left px-4 py-2 text-xs text-[#092B49] font-medium hover:bg-slate-50 flex items-center gap-2"
                  >
                    <RotateCcw className="w-3.5 h-3.5 text-[#28B89A]" /> Reset to Rupesh Demo
                  </button>
                </div>
              )}
            </div>

            {/* Mobile menu button */}
            <div className="flex md:hidden">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="p-2 text-slate-600 hover:text-slate-900 focus:outline-none"
              >
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {isMobileMenuOpen && (
        <div className="md:hidden border-t border-[#DCE5EC] bg-white px-4 pt-2 pb-4 space-y-1 animate-fadeIn">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => handleNavClick(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium ${
                currentPage === item.id ? 'bg-[#EEF6FF] text-[#092B49] font-semibold' : 'text-[#64748B]'
              }`}
            >
              {item.icon}
              {item.label}
            </button>
          ))}
          <div className="pt-2 border-t border-slate-100 flex flex-col gap-2">
            <button
              onClick={() => {
                resetToDemo();
                setIsMobileMenuOpen(false);
              }}
              className="flex items-center justify-center gap-2 w-full py-2 bg-slate-100 text-xs font-semibold text-[#092B49] rounded-lg"
            >
              <RotateCcw className="w-3.5 h-3.5 text-[#28B89A]" /> Reset Demo Profile
            </button>
          </div>
        </div>
      )}
    </header>
  );
};

function roundMonths(savings: number, expenses: number): number {
  if (!expenses || expenses <= 0) return 3.3;
  return Math.round((savings / expenses) * 10) / 10;
}

