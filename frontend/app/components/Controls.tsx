import { useState } from "react";
import { motion } from "motion/react";
import {
  Settings,
  Eye,
  Download,
  ExternalLink,
  Save,
  Trash2,
} from "lucide-react";
import { Preset } from "../App";
import { apiPost, NginxExport, CaddyExport } from "../api/client";
import { PROXY_BASE } from "../api/config";

interface ControlsProps {
  selected: Set<string>;
  expandImplies: boolean;
  seed: string;
  setSeed: (value: string) => void;
  target: string;
  setTarget: (value: string) => void;
  setOutput: (value: string) => void;
  presets: Record<string, Preset>;
  savePresets: (presets: Record<string, Preset>) => void;
  setSelected: (selected: Set<string>) => void;
}

export function Controls({
  selected,
  expandImplies,
  seed,
  setSeed,
  target,
  setTarget,
  setOutput,
  presets,
  savePresets,
  setSelected,
}: ControlsProps) {
  const [presetName, setPresetName] = useState("");
  const [selectedPreset, setSelectedPreset] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handlePreview = async () => {
    if (selected.size === 0) return;

    setIsLoading(true);
    try {
      const data = await apiPost("/emulate", {
        services: [...selected],
        expand_implies: expandImplies,
        seed: seed || null,
      });

      setOutput(JSON.stringify(data, null, 2));
    } catch (e:any) {
      setOutput("Error: " + e.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = async (type: "nginx" | "caddy") => {
    if (selected.size === 0) return;

    setIsLoading(true);
    try {
      if (type === "nginx") {
        const data = await apiPost<NginxExport>("/export/nginx", {
          services: [...selected],
        });
        setOutput(data.nginx);
      } else {
        const data = await apiPost<CaddyExport>("/export/caddy", {
          services: [...selected],
        });
        setOutput(data.caddy);
      }
    } catch (e:any) {
      setOutput("Error: " + e.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLaunch = () => {
    if (selected.size === 0 || !target) return;

    const params = new URLSearchParams({
      target: target,
      services: [...selected].join(","),
      expand_implies: expandImplies ? "1" : "0",
      seed: seed || "",
    });

    window.open(`${PROXY_BASE}?${params.toString()}`, "_blank");
  };

  const handleSavePreset = () => {
    if (selected.size === 0 || !presetName.trim()) return;

    const name = presetName.trim();
    const newPresets = { ...presets };

    if (newPresets[name] && !confirm(`Overwrite existing preset "${name}"?`)) {
      return;
    }

    newPresets[name] = {
      services: [...selected],
      expand: expandImplies,
      seed: seed || "",
    };

    savePresets(newPresets);
    setPresetName("");
  };

  const handleLoadPreset = (name: string) => {
    if (!name) return;

    const preset = presets[name];
    if (!preset) return;

    setSelected(new Set(preset.services));
    setSeed(preset.seed);
    setSelectedPreset(name);
  };

  const handleDeletePreset = () => {
    if (!selectedPreset) return;

    const newPresets = { ...presets };
    delete newPresets[selectedPreset];

    savePresets(newPresets);
    setSelectedPreset("");
  };

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5 }}
      className="bg-zinc-900/40 backdrop-blur-sm border border-zinc-800 rounded-xl p-6 shadow-xl space-y-6"
    >
      <div className="flex items-center gap-3 mb-4">
        <Settings className="w-5 h-5 text-emerald-500" />
        <h2 className="text-lg font-semibold">Controls</h2>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
        >
          <label className="block text-sm font-medium text-zinc-300 mb-2">
            Random seed
          </label>
          <input
            type="text"
            value={seed}
            onChange={(e) => setSeed(e.target.value)}
            placeholder="Optional for repeatable runs (e.g. 1337)"
            className="w-full px-4 py-2.5 bg-zinc-900/50 border border-zinc-700 rounded-lg text-sm
                     focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500
                     transition-all duration-200 placeholder:text-zinc-500"
          />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
        >
          <label className="block text-sm font-medium text-zinc-300 mb-2">
            Target URL
          </label>
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="https://example.com"
            className="w-full px-4 py-2.5 bg-zinc-900/50 border border-zinc-700 rounded-lg text-sm
                     focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500
                     transition-all duration-200 placeholder:text-zinc-500"
          />
        </motion.div>
      </div>

      {/* Presets */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="border-t border-zinc-700 pt-6"
      >
        <h3 className="text-sm font-medium text-zinc-300 mb-3">Presets</h3>
        <div className="grid md:grid-cols-2 gap-3">
          <div className="flex gap-2">
            <input
              type="text"
              value={presetName}
              onChange={(e) => setPresetName(e.target.value)}
              placeholder="Preset name"
              className="flex-1 px-4 py-2.5 bg-zinc-900/50 border border-zinc-700 rounded-lg text-sm
                       focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500
                       transition-all duration-200 placeholder:text-zinc-500"
            />
            <motion.button
              onClick={handleSavePreset}
              disabled={selected.size === 0 || !presetName.trim()}
              className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:bg-zinc-800 
                       disabled:text-zinc-600 text-white rounded-lg text-sm font-medium
                       transition-all duration-200 flex items-center gap-2 disabled:cursor-not-allowed"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Save className="w-4 h-4" />
              Save
            </motion.button>
          </div>

          <div className="flex gap-2">
            <select
              value={selectedPreset}
              onChange={(e) => handleLoadPreset(e.target.value)}
              className="flex-1 px-4 py-2.5 bg-zinc-900/50 border border-zinc-700 rounded-lg text-sm
                       focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500
                       transition-all duration-200"
            >
              <option value="">Load preset…</option>
              {Object.keys(presets).map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
            <motion.button
              onClick={handleDeletePreset}
              disabled={!selectedPreset}
              className="px-4 py-2.5 bg-red-900/30 hover:bg-red-900/50 disabled:bg-zinc-800 
                       disabled:text-zinc-600 text-red-400 rounded-lg text-sm font-medium
                       transition-all duration-200 flex items-center gap-2 disabled:cursor-not-allowed"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Trash2 className="w-4 h-4" />
            </motion.button>
          </div>
        </div>
      </motion.div>

      {/* Action buttons */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="flex flex-wrap gap-3 pt-2"
      >
        <motion.button
          onClick={handlePreview}
          disabled={selected.size === 0 || isLoading}
          className="flex-1 min-w-[160px] px-4 py-3 bg-zinc-800 hover:bg-zinc-700 disabled:bg-zinc-900 
                   disabled:text-zinc-600 text-white rounded-lg text-sm font-medium
                   transition-all duration-200 flex items-center justify-center gap-2 disabled:cursor-not-allowed"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Eye className="w-4 h-4" />
          Preview fingerprint
        </motion.button>

        <motion.button
          onClick={() => handleExport("nginx")}
          disabled={selected.size === 0 || isLoading}
          className="flex-1 min-w-[140px] px-4 py-3 bg-zinc-800 hover:bg-zinc-700 disabled:bg-zinc-900 
                   disabled:text-zinc-600 text-white rounded-lg text-sm font-medium
                   transition-all duration-200 flex items-center justify-center gap-2 disabled:cursor-not-allowed"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Download className="w-4 h-4" />
          Export nginx
        </motion.button>

        <motion.button
          onClick={() => handleExport("caddy")}
          disabled={selected.size === 0 || isLoading}
          className="flex-1 min-w-[140px] px-4 py-3 bg-zinc-800 hover:bg-zinc-700 disabled:bg-zinc-900 
                   disabled:text-zinc-600 text-white rounded-lg text-sm font-medium
                   transition-all duration-200 flex items-center justify-center gap-2 disabled:cursor-not-allowed"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Download className="w-4 h-4" />
          Export Caddy
        </motion.button>

        <motion.button
          onClick={handleLaunch}
          disabled={selected.size === 0 || !target || isLoading}
          className="flex-1 min-w-[180px] px-4 py-3 bg-gradient-to-r from-emerald-600 to-emerald-500 
                   hover:from-emerald-500 hover:to-emerald-400 disabled:from-zinc-900 disabled:to-zinc-900
                   disabled:text-zinc-600 text-white rounded-lg text-sm font-semibold
                   transition-all duration-200 flex items-center justify-center gap-2 
                   shadow-lg shadow-emerald-500/20 disabled:shadow-none disabled:cursor-not-allowed"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <ExternalLink className="w-4 h-4" />
          Open proxied site
        </motion.button>
      </motion.div>
    </motion.section>
  );
}
