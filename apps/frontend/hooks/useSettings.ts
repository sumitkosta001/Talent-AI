'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidateSettings } from '@/types/settings';
import { SettingsService } from '@/services/settings.service';

export function useSettings() {
  const [initialSettings, setInitialSettings] = useState<CandidateSettings | null>(null);
  const [currentSettings, setCurrentSettings] = useState<CandidateSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const fetchSettings = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await SettingsService.getSettings();
      setInitialSettings(JSON.parse(JSON.stringify(data)));
      setCurrentSettings(JSON.parse(JSON.stringify(data)));

      // Apply theme choice immediately
      if (typeof window !== 'undefined') {
        if (data.theme === 'Dark') {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to retrieve settings details');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const updateSettingNode = useCallback((section: keyof CandidateSettings, field: string, value: any) => {
    setCurrentSettings((prev) => {
      if (!prev) return null;
      const sectionData = prev[section];
      
      if (typeof sectionData === 'object' && sectionData !== null) {
        return {
          ...prev,
          [section]: {
            ...sectionData,
            [field]: value,
          },
        };
      } else {
        return {
          ...prev,
          [section]: value,
        };
      }
    });
  }, []);

  const hasUnsavedChanges = useCallback(() => {
    if (!initialSettings || !currentSettings) return false;
    return JSON.stringify(initialSettings) !== JSON.stringify(currentSettings);
  }, [initialSettings, currentSettings]);

  const discardChanges = useCallback(() => {
    if (initialSettings) {
      setCurrentSettings(JSON.parse(JSON.stringify(initialSettings)));
    }
  }, [initialSettings]);

  const saveSettings = useCallback(async () => {
    if (!currentSettings) return false;
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      const updated = await SettingsService.updateSettings(currentSettings);
      setInitialSettings(JSON.parse(JSON.stringify(updated)));
      setCurrentSettings(JSON.parse(JSON.stringify(updated)));
      setSuccess('Settings changes saved successfully');
      setTimeout(() => setSuccess(null), 3000);
      return true;
    } catch (err: any) {
      setError(err?.message || 'Failed to save settings modification');
      return false;
    } finally {
      setSaving(false);
    }
  }, [currentSettings]);

  const changePassword = useCallback(async (passwordData: any) => {
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      await SettingsService.changePassword(passwordData);
      setSuccess('Password updated successfully');
      setTimeout(() => setSuccess(null), 3000);
      return true;
    } catch (err: any) {
      setError(err?.message || 'Failed to update account password');
      return false;
    } finally {
      setSaving(false);
    }
  }, []);

  const deleteAccount = useCallback(async () => {
    setSaving(true);
    setError(null);
    try {
      await SettingsService.deleteAccount();
      setSuccess('Account deleted');
      return true;
    } catch (err: any) {
      setError(err?.message || 'Failed to delete account');
      return false;
    } finally {
      setSaving(false);
    }
  }, []);

  return {
    settings: currentSettings,
    loading,
    saving,
    error,
    success,
    updateSettingNode,
    hasUnsavedChanges: hasUnsavedChanges(),
    discardChanges,
    saveSettings,
    changePassword,
    deleteAccount,
  };
}
