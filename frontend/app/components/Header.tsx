import { motion } from "motion/react";

export function Header() {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="border-b border-zinc-800 bg-zinc-950/50 backdrop-blur-sm"
    >
      <div className="px-6 py-4 flex items-center gap-3">
        <motion.img
          src="/logo.svg"
          alt="Wapparalyser"
          initial={{ rotate: -180, scale: 0 }}
          animate={{ rotate: 0, scale: 1 }}
          transition={{
            type: "spring",
            stiffness: 260,
            damping: 20,
            delay: 0.1
          }}
          className="w-8 h-8"
        />
        <div>
          <h1 className="text-xl font-bold tracking-tight">Wapparalyser</h1>
          <p className="text-sm text-zinc-400">Fuzzing 'n' Fooling Wappalyzer</p>
        </div>
      </div>
    </motion.header>
  );
}
