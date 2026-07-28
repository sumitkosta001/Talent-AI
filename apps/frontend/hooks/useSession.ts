'use client';

import { useState, useEffect } from 'react';

export function useSession(timeoutSeconds = 60) {
  const [showTimeoutModal, setShowTimeoutModal] = useState(false);
  const [secondsRemaining, setSecondsRemaining] = useState(timeoutSeconds);

  useEffect(() => {
    let idleTimer: NodeJS.Timeout;
    
    const resetIdleTimer = () => {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => {
        setShowTimeoutModal(true);
        setSecondsRemaining(timeoutSeconds);
      }, 1000 * 60 * 15);
    };

    window.addEventListener('mousemove', resetIdleTimer);
    window.addEventListener('keydown', resetIdleTimer);

    resetIdleTimer();

    return () => {
      clearTimeout(idleTimer);
      window.removeEventListener('mousemove', resetIdleTimer);
      window.removeEventListener('keydown', resetIdleTimer);
    };
  }, [timeoutSeconds]);

  useEffect(() => {
    if (!showTimeoutModal) return;
    if (secondsRemaining <= 0) {
      if (typeof window !== 'undefined') {
        window.location.href = '/session-expired';
      }
      return;
    }

    const countdownTimer = setInterval(() => {
      setSecondsRemaining((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(countdownTimer);
  }, [showTimeoutModal, secondsRemaining]);

  const stayLoggedIn = () => {
    setShowTimeoutModal(false);
    setSecondsRemaining(timeoutSeconds);
  };

  return {
    showTimeoutModal,
    setShowTimeoutModal,
    secondsRemaining,
    stayLoggedIn,
  };
}
