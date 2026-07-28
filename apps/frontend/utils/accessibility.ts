export function announceToScreenReader(message: string, politeness: 'polite' | 'assertive' = 'polite'): void {
  if (typeof window === 'undefined') return;

  let announcer = document.getElementById('sr-announcer');
  if (!announcer) {
    announcer = document.createElement('div');
    announcer.id = 'sr-announcer';
    announcer.setAttribute('aria-live', politeness);
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only';
    document.body.appendChild(announcer);
  } else {
    announcer.setAttribute('aria-live', politeness);
  }

  announcer.textContent = '';
  setTimeout(() => {
    if (announcer) announcer.textContent = message;
  }, 50);
}

export function handleFocusTrap(containerRef: React.RefObject<HTMLElement | null>, e: React.KeyboardEvent): void {
  if (e.key !== 'Tab' || !containerRef.current) return;

  const focusable = containerRef.current.querySelectorAll<HTMLElement>(
    'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
  );

  if (focusable.length === 0) return;

  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  if (e.shiftKey) {
    if (document.activeElement === first) {
      e.preventDefault();
      last.focus();
    }
  } else {
    if (document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }
}
