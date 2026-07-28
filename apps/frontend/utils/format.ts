export const formatCurrency = (value: number) => {
  return new Intl.NumberFormat().format(value);
};
