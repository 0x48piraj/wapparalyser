import { useMemo } from "react";
import { motion } from "motion/react";
import { Search } from "lucide-react";
import { Service } from "../App";
import { ServiceCard } from "./ServiceCard";

interface SidebarProps {
  services: Service[];
  selected: Set<string>;
  expandImplies: boolean;
  serviceMap: Record<string, Service>;
  searchQuery: string;
  onSearchChange: (query: string) => void;
  onToggleService: (serviceName: string) => void;
}

export function Sidebar({
  services,
  selected,
  expandImplies,
  serviceMap,
  searchQuery,
  onSearchChange,
  onToggleService,
}: SidebarProps) {
  // Calculate implied services
  const getImpliedServices = () => {
    if (!expandImplies) return new Set<string>();

    const impliedSet = new Set<string>();
    const queue = [...selected];

    while (queue.length) {
      const name = queue.pop()!;
      const service = serviceMap[name];
      const implies = service?.implies || [];

      implies.forEach(dep => {
        const depName = dep.split(";")[0];
        if (!selected.has(depName) && !impliedSet.has(depName)) {
          impliedSet.add(depName);
          queue.push(depName);
        }
      });
    }

    return impliedSet;
  };

  const impliedServices = useMemo(getImpliedServices, [selected, expandImplies, serviceMap]);

  return (
    <motion.aside
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="w-80 border-r border-zinc-800 bg-zinc-950/30 backdrop-blur-sm flex flex-col overflow-hidden min-h-0"
    >
      <div className="p-4 border-b border-zinc-800">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
          <input
            type="text"
            placeholder="Search services…"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-zinc-900/50 border border-zinc-700 rounded-lg text-sm 
                     focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500
                     transition-all duration-200 placeholder:text-zinc-500"
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <div className="grid grid-cols-2 gap-3">
          {services.map(service => (
            <ServiceCard
              key={service.name}
              service={service}
              isSelected={selected.has(service.name)}
              isImplied={impliedServices.has(service.name)}
              onToggle={onToggleService}
            />
          ))}
        </div>
      </div>
    </motion.aside>
  );
}
