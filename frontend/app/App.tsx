import { useState, useEffect, useCallback, useMemo } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Menu, X } from "lucide-react";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { MainPanel } from "./components/MainPanel";
import { apiGet } from "./api/client";
import { useDebounce } from "./hooks/useDebounce";
import { useServices } from "./hooks/useServices";

export interface Service {
  name: string;
  icon?: string;
  implies?: string[];
}

export interface Preset {
  services: string[];
  expand: boolean;
  seed: string;
}

export default function App() {
  const [services, setServices] = useState<Service[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [expandImplies, setExpandImplies] = useState(false);
  const [rawQuery, setRawQuery] = useState("");
  const searchQuery = useDebounce(rawQuery, 120);
  const [seed, setSeed] = useState("");
  const [target, setTarget] = useState("");
  const [output, setOutput] = useState("Ready.");
  const [presets, setPresets] = useState<Record<string, Preset>>({});
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const { serviceMap, impliedMap } = useServices(services);

  // Load services
  useEffect(() => {
    apiGet("/services").then(setServices).catch(console.error);
  }, []);

  // Load presets from localStorage
  useEffect(() => {
    const stored = localStorage.getItem("wapparalyser.presets");
    if (stored) {
      try {
        setPresets(JSON.parse(stored));
      } catch (e) {
        console.error("Failed to parse presets", e);
      }
    }
  }, []);

  // Save presets to localStorage
  const savePresetsToStorage = (newPresets: Record<string, Preset>) => {
    localStorage.setItem("wapparalyser.presets", JSON.stringify(newPresets));
    setPresets(newPresets);
  };

  const toggleService = useCallback((serviceName: string) => {
    setSelected(prev => {
      const next = new Set(prev);
      next.has(serviceName) ? next.delete(serviceName) : next.add(serviceName);
      return next;
    });
  }, []);

  const filteredServices = useMemo(() => {
    const q = searchQuery.toLowerCase();
    return services.filter(s => s.name.toLowerCase().includes(q));
  }, [services, searchQuery]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-950 via-zinc-900 to-black text-zinc-100">
      <Header />
      
      {/* Mobile menu button */}
      <motion.button
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        className="lg:hidden fixed bottom-6 right-6 z-50 p-4 bg-emerald-600 hover:bg-emerald-500 
                 text-white rounded-full shadow-2xl shadow-emerald-500/30"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </motion.button>
      
      <div className="flex h-[calc(100vh-72px)] overflow-hidden relative min-h-0">
        {/* Desktop Sidebar */}
        <div className="hidden lg:flex min-h-0">
          <Sidebar
            services={filteredServices}
            selected={selected}
            expandImplies={expandImplies}
            serviceMap={serviceMap}
            onSearchChange={setRawQuery}
            searchQuery={rawQuery}
            onToggleService={toggleService}
          />
        </div>

        {/* Mobile Sidebar Overlay */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setIsMobileMenuOpen(false)}
                className="lg:hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
              />
              <motion.div
                initial={{ x: "-100%" }}
                animate={{ x: 0 }}
                exit={{ x: "-100%" }}
                transition={{ type: "spring", damping: 25, stiffness: 200 }}
                className="lg:hidden fixed left-0 top-[72px] bottom-0 z-40 w-full max-w-sm flex flex-col min-h-0"
              >
                <Sidebar
                  services={filteredServices}
                  selected={selected}
                  expandImplies={expandImplies}
                  serviceMap={serviceMap}
                  searchQuery={rawQuery}
                  onSearchChange={setRawQuery}
                  onToggleService={toggleService}
                />
              </motion.div>
            </>
          )}
        </AnimatePresence>

        <MainPanel
          selected={selected}
          expandImplies={expandImplies}
          impliedMap={impliedMap}
          setExpandImplies={setExpandImplies}
          seed={seed}
          setSeed={setSeed}
          target={target}
          setTarget={setTarget}
          output={output}
          setOutput={setOutput}
          presets={presets}
          savePresets={savePresetsToStorage}
          setSelected={setSelected}
        />
      </div>
    </div>
  );
}
