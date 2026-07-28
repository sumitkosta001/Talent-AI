export interface RecruiterOffer {
  salary: string;
  joiningDate: string;
  position: string;
  department: string;
  reportingManager: string;
  expiryDate: string;
  status: 'Pending' | 'Accepted' | 'Declined' | 'Withdrawn';
}
