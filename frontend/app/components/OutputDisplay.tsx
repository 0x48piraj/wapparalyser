import { motion } from "motion/react";
import { Terminal, Copy, Check } from "lucide-react";
import { useState } from "react";

interface OutputDisplayProps {
  output: string;
}

export function OutputDisplay({ output }: OutputDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6 }}
      className="bg-zinc-900/40 backdrop-blur-sm border border-zinc-800 rounded-xl p-6 shadow-xl"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <Terminal className="w-5 h-5 text-emerald-500" />
          <h3 className="text-lg font-semibold">Fingerprint preview</h3>
        </div>
        <motion.button
          onClick={handleCopy}
          className="px-3 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-lg text-sm
                   transition-all duration-200 flex items-center gap-2"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {copied ? (
            <>
              <Check className="w-4 h-4 text-emerald-500" />
              Copied!
            </>
          ) : (
            <>
              <Copy className="w-4 h-4" />
              Copy
            </>
          )}
        </motion.button>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7 }}
        className="relative"
      >
        <pre className="bg-black/50 border border-zinc-700 rounded-lg p-4 max-h-80 overflow-auto 
                       text-sm text-zinc-300 font-mono scrollbar-thin scrollbar-thumb-zinc-700 
                       scrollbar-track-transparent whitespace-pre-wrap break-words">
          {output}
        </pre>
      </motion.div>
    </motion.section>
  );
}
