'use client';

import { useRouter } from 'next/navigation';
import { useCallback } from 'react';

export function usePrefetch() {
  const router = useRouter();

  const prefetch = useCallback((href: string) => {
    if (href && href.startsWith('/')) {
      router.prefetch(href);
    }
  }, [router]);

  return { prefetch };
}
