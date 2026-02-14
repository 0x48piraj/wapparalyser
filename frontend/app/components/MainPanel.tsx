import { motion } from "motion/react";
import { Service, Preset } from "../App";
import { StackDisplay } from "./StackDisplay";
import { Controls } from "./Controls";
import { OutputDisplay } from "./OutputDisplay";

interface MainPanelProps {
  selected: Set<string>;
  expandImplies: boolean;
  impliedMap: Record<string, string[]>;
  setExpandImplies: (value: boolean) => void;
  seed: string;
  setSeed: (value: string) => void;
  target: string;
  setTarget: (value: string) => void;
  output: string;
  setOutput: (value: string) => void;
  presets: Record<string, Preset>;
  savePresets: (presets: Record<string, Preset>) => void;
  setSelected: (selected: Set<string>) => void;
}

export function MainPanel({
  selected,
  expandImplies,
  impliedMap,
  setExpandImplies,
  seed,
  setSeed,
  target,
  setTarget,
  output,
  setOutput,
  presets,
  savePresets,
  setSelected,
}: MainPanelProps) {
  return (
    <motion.main
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="flex-1 overflow-y-auto p-6 lg:p-8"
    >
      <div className="max-w-5xl mx-auto space-y-6">
        <StackDisplay
          selected={selected}
          expandImplies={expandImplies}
          setExpandImplies={setExpandImplies}
          impliedMap={impliedMap}
        />

        <Controls
          selected={selected}
          expandImplies={expandImplies}
          seed={seed}
          setSeed={setSeed}
          target={target}
          setTarget={setTarget}
          setOutput={setOutput}
          presets={presets}
          savePresets={savePresets}
          setSelected={setSelected}
        />

        <OutputDisplay output={output} />
      </div>
    </motion.main>
  );
}
