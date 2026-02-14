import React, { useState } from "react";
import { motion } from "motion/react";
import { Package } from "lucide-react";
import { Service } from "../App";
import { STATIC_BASE } from "../api/config";

interface Props {
  service: Service;
  isSelected: boolean;
  isImplied: boolean;
  onToggle: (name: string) => void;
}

export const ServiceCard = React.memo(function ServiceCard({
  service,
  isSelected,
  isImplied,
  onToggle
}: Props) {

  const [imgFailed, setImgFailed] = useState(false);

  const showFallback = !service.icon || imgFailed;

  const iconUrl = service.icon
    ? `${STATIC_BASE}/icons/${encodeURIComponent(service.icon)}`
    : undefined;

  return (
    <motion.div
      layout={false}
      initial={{ opacity: 0.6 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.15 }}
      onClick={() => onToggle(service.name)}
      className={`
        relative p-3 rounded-lg cursor-pointer
        flex flex-col items-center justify-center gap-2
        transition-all duration-200
        ${
          isSelected
            ? "bg-gradient-to-br from-emerald-900/40 to-emerald-950/40 border-2 border-emerald-500/50 shadow-lg shadow-emerald-500/20"
            : isImplied
            ? "bg-zinc-900/40 border-2 border-dashed border-zinc-600 opacity-60"
            : "bg-zinc-900/30 border-2 border-zinc-700/50 hover:border-emerald-500/30"
        }
        hover:scale-105 active:scale-95
      `}
      whileHover={{ y: -2 }}
      whileTap={{ scale: 0.95 }}
    >

      {/* Icon */}
      <div className="w-8 h-8 flex items-center justify-center">
        {!showFallback ? (
          <motion.img
            src={iconUrl}
            alt={service.name}
            className="w-8 h-8 object-contain"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.1 }}
            onError={() => setImgFailed(true)}
          />
        ) : (
          <Package className="w-8 h-8 text-emerald-500" />
        )}
      </div>

      <span className="text-xs text-center font-medium leading-tight">
        {service.name}
      </span>

      {/* Selected indicator */}
      {isSelected && (
        <motion.div
          layoutId="selected-indicator"
          className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-500 rounded-full"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
        />
      )}
    </motion.div>
  );
});
