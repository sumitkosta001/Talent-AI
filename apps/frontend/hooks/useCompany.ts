'use client';

import { useState, useEffect, useCallback } from 'react';
import { Company, CompanyDetail } from '@/types/company';
import { CompanyService, RecruiterCompanyService } from '@/services/company.service';
import { MOCK_COMPANY_CULTURE } from '@/mock/companyCulture';
import { MOCK_COMPANY_BENEFITS } from '@/mock/companyBenefits';
import { MOCK_COMPANY_GALLERY } from '@/mock/companyGallery';
import { MOCK_COMPANY_EMPLOYEES } from '@/mock/companyEmployees';
import { MOCK_COMPANY_RATINGS } from '@/mock/companyRatings';
import { CompanyRating } from '@/types/companyRating';
import { CompanyBenefit } from '@/types/companyBenefit';
import { CompanyEmployee } from '@/types/companyEmployee';
import { CompanyGalleryImage } from '@/types/companyGallery';

export function useCompany(id?: string) {
  // Recruiter mode if id is empty/undefined
  const isRecruiter = !id;

  const [company, setCompany] = useState<Company | null>(null);
  const [recruiterCompany, setRecruiterCompany] = useState<CompanyDetail | null>(null);
  const [culture, setCulture] = useState<{ title: string; desc: string }[]>([]);
  const [benefits, setBenefits] = useState<CompanyBenefit[]>([]);
  const [gallery, setGallery] = useState<CompanyGalleryImage[]>([]);
  const [employees, setEmployees] = useState<CompanyEmployee[]>([]);
  const [ratings, setRatings] = useState<CompanyRating | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      if (isRecruiter) {
        const data = await RecruiterCompanyService.getCompany();
        setRecruiterCompany(data);
      } else {
        const main = await CompanyService.getCompanyById(id!);
        setCompany(main);

        // Load linked sub-attributes
        setCulture(MOCK_COMPANY_CULTURE[id!] || []);
        setBenefits(MOCK_COMPANY_BENEFITS[id!] || []);
        setGallery(MOCK_COMPANY_GALLERY[id!] || []);
        setEmployees(MOCK_COMPANY_EMPLOYEES[id!] || []);
        setRatings(MOCK_COMPANY_RATINGS[id!] || null);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to load company details profile');
    } finally {
      setLoading(false);
    }
  }, [id, isRecruiter]);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  const handleUpdate = useCallback(async (updates: CompanyDetail) => {
    try {
      const updated = await RecruiterCompanyService.updateCompany(updates);
      setRecruiterCompany(updated);
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  return {
    company: (isRecruiter ? recruiterCompany : company) as (Company & CompanyDetail) | null,
    culture,
    benefits,
    gallery,
    employees,
    ratings,
    loading,
    error,
    updateCompany: handleUpdate,
    refetch: loadAll,
  };
}
