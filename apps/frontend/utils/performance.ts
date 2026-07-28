export function debounce<T extends (...args: any[]) => any>(fn: T, delayMs = 300): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout> | null = null;
  return function (...args: Parameters<T>) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      fn(...args);
    }, delayMs);
  };
}

export function throttle<T extends (...args: any[]) => any>(fn: T, limitMs = 300): (...args: Parameters<T>) => void {
  let inThrottle = false;
  return function (...args: Parameters<T>) {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limitMs);
    }
  };
}

export function measureRenderTime(componentName: string, startTimeMs: number): void {
  if (process.env.NODE_ENV === 'development' && typeof performance !== 'undefined') {
    const duration = performance.now() - startTimeMs;
    console.debug(`[Performance] ${componentName} rendered in ${duration.toFixed(2)}ms`);
  }
}

export function requestIdleTask(task: () => void, timeoutMs = 2000): void {
  if (typeof window !== 'undefined' && 'requestIdleCallback' in window) {
    (window as any).requestIdleCallback(task, { timeout: timeoutMs });
  } else {
    setTimeout(task, 1);
  }
}
