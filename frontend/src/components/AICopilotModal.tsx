import React, { useState, useRef, useEffect } from 'react';
import { 
  X, 
  Send, 
  Bot, 
  User, 
  Sparkles, 
  ShieldCheck, 
  AlertTriangle, 
  ShieldAlert, 
  CheckCircle2, 
  Clock, 
  FileText,
  Loader2,
  HelpCircle,
  Lightbulb
} from 'lucide-react';
import { useFinancial } from '../context/FinancialContext';

export const AICopilotModal: React.FC = () => {
  const { 
    isChatOpen, 
    setIsChatOpen, 
    chatMessages, 
    sendChatMessage, 
    isAiLoading, 
    profile, 
    goals 
  } = useFinancial();

  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const samplePrompts = [
    'Can I afford a ₹70,000 laptop?',
    'How much should I save every month?',
    'How long will it take me to reach my goal?',
    'What happens if my expenses increase by ₹5,000?',
    'Explain my financial health score.',
    'Why did you recommend this investment?',
    'How can I improve my savings rate?',
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isChatOpen) {
      scrollToBottom();
    }
  }, [chatMessages, isChatOpen]);

  if (!isChatOpen) return null;

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isAiLoading) return;
    const msg = input;
    setInput('');
    sendChatMessage(msg);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full h-[90vh] sm:h-[82vh] flex flex-col shadow-2xl border border-[#DCE5EC] overflow-hidden animate-scaleUp">
        {/* Header */}
        <div className="p-4 bg-gradient-to-r from-[#092B49] to-[#102A43] text-white flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#28B89A] flex items-center justify-center text-white shadow-xs">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold">Ask FinWise AI</h3>
                <span className="bg-[#DDF7F0] text-[#092B49] text-[10px] font-extrabold px-2 py-0.5 rounded-full">
                  COPILOT
                </span>
              </div>
              <p className="text-[11px] text-slate-300">
                Your financial decision companion • Calibrated for {profile.name}
              </p>
            </div>
          </div>

          <button
            onClick={() => setIsChatOpen(false)}
            className="text-slate-300 hover:text-white p-1 rounded-lg transition-colors cursor-pointer"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Quick Sample Prompts Bar */}
        <div className="p-2.5 bg-[#F8FBFC] border-b border-[#DCE5EC] overflow-x-auto flex gap-2 shrink-0 scrollbar-none">
          {samplePrompts.map((p) => (
            <button
              key={p}
              onClick={() => sendChatMessage(p)}
              disabled={isAiLoading}
              className="text-[11px] whitespace-nowrap bg-white hover:bg-[#EEF6FF] text-[#102A43] border border-[#DCE5EC] hover:border-[#28B89A] px-3 py-1 rounded-full font-medium transition-colors cursor-pointer shrink-0 disabled:opacity-50"
            >
              {p}
            </button>
          ))}
        </div>

        {/* Messages Body */}
        <div className="flex-1 p-4 overflow-y-auto space-y-4 bg-slate-50/50">
          {chatMessages.map((msg) => {
            const isAi = msg.sender === 'ai';
            const resp = msg.response;

            return (
              <div
                key={msg.id}
                className={`flex gap-3 ${isAi ? 'items-start' : 'items-start flex-row-reverse'}`}
              >
                {/* Avatar */}
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-xs font-bold ${
                    isAi
                      ? 'bg-[#28B89A] text-white shadow-xs'
                      : 'bg-[#092B49] text-white'
                  }`}
                >
                  {isAi ? <Bot className="w-4 h-4" /> : profile.name.charAt(0)}
                </div>

                {/* Message Content */}
                <div className={`max-w-[85%] ${isAi ? '' : 'text-right'}`}>
                  {isAi && resp ? (
                    /* Structured 4-Part Response matching Section 18 & Guardrail Gate */
                    <div className="bg-white rounded-2xl border border-[#DCE5EC] p-4 text-left shadow-xs space-y-3.5 text-xs text-[#102A43]">
                      {/* Guardrail Status Pill */}
                      <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                        <span
                          className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase flex items-center gap-1 ${
                            resp.guardrail_status === 'ALLOW'
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                              : resp.guardrail_status === 'WARN'
                              ? 'bg-amber-50 text-amber-700 border border-amber-200'
                              : 'bg-rose-50 text-rose-700 border border-rose-200'
                          }`}
                        >
                          <ShieldCheck className="w-3 h-3" />
                          Guardrail Gate: {resp.guardrail_status}
                        </span>
                        <span className="text-[10px] text-slate-400">{msg.timestamp}</span>
                      </div>

                      {/* 1. Short Answer */}
                      <div>
                        <h4 className="text-[10px] font-bold uppercase tracking-wider text-[#64748B] mb-1">
                          Direct Assessment
                        </h4>
                        <p className="text-sm font-semibold text-[#092B49] leading-snug">
                          {resp.short_answer}
                        </p>
                      </div>

                      {/* 2. Why? (Telemetry-grounded) */}
                      <div className="bg-[#F8FBFC] p-3 rounded-xl border border-slate-100 space-y-1.5">
                        <h4 className="text-[10px] font-bold uppercase tracking-wider text-[#64748B] flex items-center gap-1">
                          <Sparkles className="w-3 h-3 text-[#28B89A]" /> Rationale & Calculations
                        </h4>
                        <ul className="space-y-1 text-slate-700">
                          {resp.why.map((w, idx) => (
                            <li key={idx} className="flex items-start gap-1.5">
                              <span className="text-[#28B89A] font-bold mt-0.5">•</span>
                              <span>{w}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* 3. Better Option */}
                      <div className="bg-[#DDF7F0]/40 p-3 rounded-xl border border-[#28B89A]/30 space-y-1">
                        <h4 className="text-[10px] font-bold uppercase tracking-wider text-[#092B49] flex items-center gap-1">
                          <Lightbulb className="w-3 h-3 text-[#28B89A]" /> Better Option / Strategy
                        </h4>
                        <p className="text-slate-800 leading-relaxed font-medium">
                          {resp.better_option}
                        </p>
                      </div>

                      {/* 4. Impact Quantified */}
                      {resp.impact && Object.keys(resp.impact).length > 0 && (
                        <div className="pt-2 border-t border-slate-100">
                          <h4 className="text-[10px] font-bold uppercase tracking-wider text-[#64748B] mb-2">
                            Scenario Impact
                          </h4>
                          <div className="grid grid-cols-2 gap-2 text-center text-[11px]">
                            {Object.entries(resp.impact).map(([key, val]) => (
                              <div key={key} className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                                <span className="text-[10px] text-slate-500 block capitalize">
                                  {key.replace(/_/g, ' ')}
                                </span>
                                <span className="font-bold text-[#092B49]">{String(val)}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Evidence / Citation */}
                      {resp.evidence_citation && (
                        <div className="pt-2 border-t border-slate-100 flex items-center gap-1.5 text-[10px] text-slate-400">
                          <FileText className="w-3 h-3 text-slate-400 shrink-0" />
                          <span>Citation: {resp.evidence_citation}</span>
                        </div>
                      )}
                    </div>
                  ) : (
                    /* User or simple AI text message */
                    <div
                      className={`inline-block p-3.5 rounded-2xl text-xs leading-relaxed ${
                        isAi
                          ? 'bg-white border border-[#DCE5EC] text-[#102A43] shadow-xs'
                          : 'bg-[#092B49] text-white font-medium'
                      }`}
                    >
                      {msg.text}
                    </div>
                  )}
                  <p className="text-[10px] text-slate-400 mt-1 px-1">{msg.timestamp}</p>
                </div>
              </div>
            );
          })}

          {isAiLoading && (
            <div className="flex items-center gap-2 p-3 bg-white rounded-xl border border-slate-200 text-xs text-[#64748B] w-max">
              <Loader2 className="w-4 h-4 text-[#28B89A] animate-spin" />
              <span>Analyzing profile telemetry & evaluating guardrails...</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <form onSubmit={handleSend} className="p-3 bg-white border-t border-[#DCE5EC] flex items-center gap-2 shrink-0">
          <input
            type="text"
            placeholder="Ask anything (e.g. 'Can I afford a ₹70,000 laptop?')..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isAiLoading}
            className="flex-1 px-4 py-2.5 bg-[#F8FBFC] border border-[#DCE5EC] rounded-xl text-xs sm:text-sm text-[#102A43] focus:outline-none focus:ring-2 focus:ring-[#28B89A] focus:bg-white transition-all"
          />
          <button
            type="submit"
            disabled={!input.trim() || isAiLoading}
            className="p-2.5 bg-[#092B49] hover:bg-[#102A43] text-white rounded-xl shadow-xs transition-colors disabled:opacity-50 cursor-pointer"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};

