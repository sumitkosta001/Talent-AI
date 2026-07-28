import { CompanyGalleryImage } from '../types/companyGallery';

export const MOCK_COMPANY_GALLERY: Record<string, CompanyGalleryImage[]> = {
  stripe: [
    { id: 'img-1', url: 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80', caption: 'Stripe HQ Collaboration Space' },
    { id: 'img-2', url: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80', caption: 'Weekly Design Critique Sessions' },
    { id: 'img-3', url: 'https://images.unsplash.com/photo-1517502884422-41eaaced0168?auto=format&fit=crop&w=800&q=80', caption: 'Stripe Micro-kitchen Lounge' },
  ],
  vercel: [
    { id: 'img-v1', url: 'https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=800&q=80', caption: 'Fully remote coordinate meets' },
  ],
};
