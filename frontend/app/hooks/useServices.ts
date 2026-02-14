import { useMemo } from "react";
import { Service } from "../App";

export interface ServiceMaps {
  serviceMap: Record<string, Service>;
  impliedMap: Record<string, string[]>;
}

export function useServices(services: Service[]): ServiceMaps {
  return useMemo<ServiceMaps>(() => {
    const serviceMap: Record<string, Service> = {};
    const impliedMap: Record<string, string[]> = {};

    for (const s of services) {
      serviceMap[s.name] = s;

      // normalize implies once globally
      impliedMap[s.name] = (s.implies ?? []).map(dep => dep.split(";")[0]);
    }

    return { serviceMap, impliedMap };
  }, [services]);
}
