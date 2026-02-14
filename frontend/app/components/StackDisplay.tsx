import { motion } from "motion/react";
import { Layers } from "lucide-react";

interface StackDisplayProps {
  selected: Set<string>;
  expandImplies: boolean;
  setExpandImplies: (value: boolean) => void;
  impliedMap: Record<string, string[]>;
}

export function StackDisplay({
  selected,
  expandImplies,
  setExpandImplies,
  impliedMap,
}: StackDisplayProps) {
  // Expand implied services
  const expandImpliedServices = (baseServices: Set<string>) => {
    const expanded = new Set(baseServices);
    const queue = [...baseServices];

    while (queue.length) {
      const name = queue.pop()!;
      const implies = impliedMap[name] || [];

      implies.forEach(dep => {
        if (!expanded.has(dep)) {
          expanded.add(dep);
          queue.push(dep);
        }
      });
    }

    return expanded;
  };

  const impliedServices = new Set<string>();
  let displaySet = new Set(selected);

  if (expandImplies) {
    displaySet = expandImpliedServices(selected);
    displaySet.forEach(s => {
      if (!selected.has(s)) impliedServices.add(s);
    });
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="bg-zinc-900/40 backdrop-blur-sm border border-zinc-800 rounded-xl p-6 shadow-xl"
    >
      <div className="flex items-center gap-3 mb-4">
        <Layers className="w-5 h-5 text-emerald-500" />
        <h2 className="text-lg font-semibold">Selected Stack</h2>
      </div>

      <motion.div
        className={`
          min-h-24 p-4 rounded-lg border-2 border-dashed
          ${displaySet.size === 0 ? "border-zinc-700 bg-zinc-900/20" : "border-zinc-700 bg-zinc-950/50"}
        `}
        layout
      >
        {displaySet.size === 0 ? (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-zinc-500 text-center py-4"
          >
            No services selected
          </motion.p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {[...displaySet].map((name) => (
              <motion.span
                key={name}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.2 }}
                className={`
                  inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium
                  ${
                    impliedServices.has(name)
                      ? "bg-zinc-800/50 text-zinc-400 border border-zinc-700 italic"
                      : "bg-emerald-900/30 text-emerald-300 border border-emerald-700/50"
                  }
                `}
                whileHover={{ scale: 1.05 }}
              >
                {name}
                {impliedServices.has(name) && (
                  <span className="text-xs opacity-70">(implied)</span>
                )}
              </motion.span>
            ))}
          </div>
        )}
      </motion.div>

      <motion.label
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="flex items-center gap-2 mt-4 cursor-pointer group"
      >
        <motion.input
          type="checkbox"
          checked={expandImplies}
          onChange={(e) => setExpandImplies(e.target.checked)}
          className="w-4 h-4 rounded border-zinc-600 bg-zinc-800 text-emerald-500 
                   focus:ring-2 focus:ring-emerald-500/50 focus:ring-offset-0
                   transition-all cursor-pointer"
          whileTap={{ scale: 0.9 }}
        />
        <span className="text-sm text-zinc-300 group-hover:text-zinc-100 transition-colors">
          Expand implied technologies
        </span>
      </motion.label>
    </motion.section>
  );
}
