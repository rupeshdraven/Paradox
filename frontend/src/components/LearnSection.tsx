import React, { useState } from 'react';
import { 
  BookOpen, 
  Sparkles, 
  TrendingUp, 
  ShieldCheck, 
  Coins, 
  FileText, 
  Layers, 
  Building2, 
  Heart,
  Bot,
  ArrowRight,
  CheckCircle2
} from 'lucide-react';
import { useFinancial } from '../context/FinancialContext';

interface Article {
  id: string;
  category: string;
  title: string;
  readTime: string;
  summary: string;
  keyPoints: string[];
  aiPrompt: string;
}

export const LearnSection: React.FC = () => {
  const { setIsChatOpen, sendChatMessage } = useFinancial();
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const categories = [
    'All',
    'Investing Basics',
    'Mutual Funds',
    'Government Schemes',
    'Tax Planning',
    'Emergency Funds',
    'Retirement Planning',
  ];

  const articles: Article[] = [
    {
      id: 'sip-basics',
      category: 'Mutual Funds',
      title: 'What is a Systematic Investment Plan (SIP)?',
      readTime: '3 min read',
      summary: 'A disciplined approach allowing you to invest a fixed sum into mutual funds at regular intervals, harnessing rupee-cost averaging and compounding.',
      keyPoints: [
        'Rupee-cost averaging: You buy more units when market drops and fewer when it rises.',
        'Compounding magic: Returns earn additional returns over multi-year horizons.',
        'Start small: High flexibility with monthly contributions starting as low as ₹500.'
      ],
      aiPrompt: 'Explain SIP to me like I am a beginner.'
    },
    {
      id: 'emergency-fund',
      category: 'Emergency Funds',
      title: 'The Cornerstone: 6-Month Emergency Cushion',
      readTime: '4 min read',
      summary: 'Before putting money into equities, an emergency fund provides psychological armor and prevents premature liquidation during unforeseen crises.',
      keyPoints: [
        'Target 3 to 6 months of non-negotiable living costs (rent, EMIs, food, utilities).',
        'Store in highly liquid, capital-safe avenues (Liquid Debt Funds or Bank FDs).',
        'Never lock emergency money in long-term illiquid schemes like PPF or real estate.'
      ],
      aiPrompt: 'How do I build a 6-month emergency fund step by step?'
    },
    {
      id: 'ppf-guide',
      category: 'Government Schemes',
      title: 'Public Provident Fund (PPF): The EEE Sovereign Anchor',
      readTime: '4 min read',
      summary: 'A 15-year statutory government-backed scheme carrying sovereign security and coveted Exempt-Exempt-Exempt (EEE) tax status.',
      keyPoints: [
        'Triple tax exemption: investment, annual accrued interest, and maturity corpus are 100% tax-free.',
        'Sovereign backing: Zero credit or market default risk.',
        'Current government notified rate: 7.1% p.a. compounded annually.'
      ],
      aiPrompt: 'Why is PPF considered one of the safest investments in India?'
    },
    {
      id: 'elss-vs-fd',
      category: 'Tax Planning',
      title: 'Tax Saving 101: ELSS vs. Traditional 80C Instruments',
      readTime: '3 min read',
      summary: 'Understand the trade-offs between market-linked equity tax savers and fixed sovereign options under Section 80C.',
      keyPoints: [
        'ELSS offers the lowest lock-in (3 years) compared to 5 years for Tax-Saver FD and 15 years for PPF.',
        'Market-linked potential: Delivers higher inflation-adjusted returns over 5+ year cycles.',
        'Subject to capital gains tax: LTCG above ₹1.25 Lakh per year taxed at 12.5%.'
      ],
      aiPrompt: 'Should I choose ELSS or PPF for Section 80C tax saving?'
    },
    {
      id: 'nps-retirement',
      category: 'Retirement Planning',
      title: 'National Pension System (NPS): Building Your Nest Egg',
      readTime: '5 min read',
      summary: 'A low-cost, regulated pension system combining market growth with structured post-retirement regular income.',
      keyPoints: [
        'Exclusive tax benefit: Additional deduction of ₹50,000 under Section 80CCD(1B).',
        'Lowest fund management fee globally (~0.09% p.a.).',
        'At age 60: 60% lump sum is 100% tax-free; 40% purchases lifetime pension annuity.'
      ],
      aiPrompt: 'Explain how NPS helps in long term retirement planning.'
    },
    {
      id: '50-30-20-rule',
      category: 'Investing Basics',
      title: 'The 50/30/20 Budgeting Rule for Young Professionals',
      readTime: '3 min read',
      summary: 'A timeless blueprint to balance living expenses, lifestyle desires, and long-term financial independence without deprivation.',
      keyPoints: [
        '50% for Needs: Rent, groceries, bills, EMIs, and healthcare.',
        '30% for Wants: Dining out, gadgets, vacations, and leisure.',
        '20% for Savings & Investments: SIPs, emergency reserve, and debt prepayments.'
      ],
      aiPrompt: 'How can I apply the 50/30/20 rule to my monthly salary?'
    }
  ];

  const filteredArticles = selectedCategory === 'All'
    ? articles
    : articles.filter((a) => a.category === selectedCategory);

  const handleAskAI = (prompt: string) => {
    setIsChatOpen(true);
    sendChatMessage(prompt);
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#F8FBFC] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs bg-[#DDF7F0] text-[#092B49] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
              FinWise Academy
            </span>
            <span className="text-xs text-[#28B89A] font-semibold flex items-center gap-1">
              <BookOpen className="w-3.5 h-3.5" /> Plain-English Financial Education
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#092B49] tracking-tight">
            Learn Financial Fundamentals
          </h1>
          <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">
            Bite-sized, zero-jargon guides explaining mutual funds, sovereign schemes, and prudent money management.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-2">
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setSelectedCategory(c)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                selectedCategory === c
                  ? 'bg-[#092B49] text-white shadow-xs'
                  : 'bg-white border border-[#DCE5EC] text-[#64748B] hover:bg-slate-50'
              }`}
            >
              {c}
            </button>
          ))}
        </div>

        {/* Articles Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredArticles.map((article) => (
            <div
              key={article.id}
              className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs hover:shadow-md transition-all flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between text-[11px] mb-3">
                  <span className="bg-[#DDF7F0] text-[#092B49] font-bold px-2 py-0.5 rounded-md">
                    {article.category}
                  </span>
                  <span className="text-slate-400 font-medium">{article.readTime}</span>
                </div>

                <h3 className="text-base font-bold text-[#102A43] group-hover:text-[#28B89A] transition-colors leading-snug mb-2">
                  {article.title}
                </h3>

                <p className="text-xs text-[#64748B] leading-relaxed mb-4">
                  {article.summary}
                </p>

                <div className="space-y-1.5 pt-3 border-t border-slate-100 mb-4 text-xs text-slate-700">
                  {article.keyPoints.map((pt, idx) => (
                    <div key={idx} className="flex items-start gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-[#28B89A] shrink-0 mt-0.5" />
                      <span className="text-[11px] leading-tight">{pt}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Ask Copilot Button */}
              <button
                onClick={() => handleAskAI(article.aiPrompt)}
                className="w-full py-2.5 px-3 bg-[#F8FBFC] hover:bg-[#EEF6FF] border border-slate-200 hover:border-[#28B89A] text-[#092B49] rounded-xl text-xs font-semibold transition-all flex items-center justify-center gap-1.5 cursor-pointer mt-2"
              >
                <Bot className="w-3.5 h-3.5 text-[#28B89A]" />
                <span>Ask AI to Explain Simply</span>
                <ArrowRight className="w-3 h-3 text-slate-400 ml-auto" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

