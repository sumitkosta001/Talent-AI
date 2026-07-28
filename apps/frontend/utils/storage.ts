export const storage = {
  get: (key: string) => typeof window !== 'undefined' ? localStorage.getItem(key) : null,
  set: (key: string, value: string) => typeof window !== 'undefined' ? localStorage.setItem(key, value) : null,
  remove: (key: string) => typeof window !== 'undefined' ? localStorage.removeItem(key) : null,
};
