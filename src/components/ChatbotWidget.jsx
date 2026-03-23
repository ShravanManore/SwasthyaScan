import { AnimatePresence, motion } from 'framer-motion';
import { MessageCircleHeart, SendHorizonal, X } from 'lucide-react';
import { useState } from 'react';
import { chatbotResponses } from '../utils/mockData';

function ChatbotWidget() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { from: 'bot', text: 'Hi, I am the SwasthyaScan assistant. Ask about symptoms, precautions, or doctor consultation.' },
  ]);

  const resolveResponse = (text) => {
    const normalized = text.toLowerCase();
    if (normalized.includes('symptom')) return chatbotResponses.symptoms;
    if (normalized.includes('precaution') || normalized.includes('prevent')) return chatbotResponses.precautions;
    if (normalized.includes('doctor') || normalized.includes('consult')) return chatbotResponses.doctor;
    return chatbotResponses.default;
  };

  const sendMessage = () => {
    if (!input.trim()) return;
    const userText = input.trim();
    const botText = resolveResponse(userText);

    setMessages((prev) => [...prev, { from: 'user', text: userText }, { from: 'bot', text: botText }]);
    setInput('');
  };

  return (
    <div className="fixed bottom-5 right-5 z-50">
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 16, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10 }}
            className="mb-3 flex h-[420px] w-[340px] flex-col rounded-2xl border border-slate-200 bg-white shadow-soft dark:border-slate-700 dark:bg-slate-900"
          >
            <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3 dark:border-slate-700">
              <p className="font-semibold">SwasthyaScan AI Chatbot</p>
              <button type="button" onClick={() => setOpen(false)}>
                <X size={18} />
              </button>
            </div>

            <div className="flex-1 space-y-3 overflow-y-auto p-4">
              {messages.map((msg, idx) => (
                <div
                  key={`${msg.from}-${idx}`}
                  className={`max-w-[85%] rounded-xl px-3 py-2 text-sm ${
                    msg.from === 'user'
                      ? 'ml-auto bg-brand-600 text-white'
                      : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
                  }`}
                >
                  {msg.text}
                </div>
              ))}
            </div>

            <div className="flex gap-2 border-t border-slate-200 p-3 dark:border-slate-700">
              <input
                value={input}
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={(event) => event.key === 'Enter' && sendMessage()}
                placeholder="Ask about TB symptoms..."
                className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-brand-500 dark:border-slate-600 dark:bg-slate-800"
              />
              <button type="button" onClick={sendMessage} className="btn-primary px-3 py-2">
                <SendHorizonal size={15} />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-r from-brand-600 to-care-600 text-white shadow-soft"
        aria-label="Toggle chatbot"
      >
        <MessageCircleHeart />
      </button>
    </div>
  );
}

export default ChatbotWidget;
