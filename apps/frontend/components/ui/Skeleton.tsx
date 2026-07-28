'use client';

import React from 'react';

interface SkeletonProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  circle?: boolean;
}

export default function Skeleton({ className = '', width, height, circle = false }: SkeletonProps) {
  const style: React.CSSProperties = {
    width: width ? (typeof width === 'number' ? `${width}px` : width) : undefined,
    height: height ? (typeof height === 'number' ? `${height}px` : height) : undefined,
  };

  return (
    <div
      style={style}
      className={`animate-pulse bg-slate-200 dark:bg-slate-700/80 ${
        circle ? 'rounded-full' : 'rounded-xl'
      } ${className}`}
      aria-hidden="true"
    />
  );
}
