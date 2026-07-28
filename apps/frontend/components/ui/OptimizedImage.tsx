'use client';

import React, { useState } from 'react';
import Image, { ImageProps } from 'next/image';
import Skeleton from './Skeleton';

interface OptimizedImageProps extends Omit<ImageProps, 'onLoad' | 'onError'> {
  fallbackSrc?: string;
  containerClassName?: string;
}

export default function OptimizedImage({
  src,
  alt,
  fallbackSrc = '/placeholder.png',
  containerClassName = '',
  className = '',
  ...props
}: OptimizedImageProps) {
  const [loading, setLoading] = useState(true);
  const [imgSrc, setImgSrc] = useState(src);

  return (
    <div className={`relative overflow-hidden ${containerClassName}`}>
      {loading && <Skeleton className="absolute inset-0 z-10 w-full h-full" />}
      <Image
        src={imgSrc}
        alt={alt}
        className={`transition-opacity duration-300 ${loading ? 'opacity-0' : 'opacity-100'} ${className}`}
        onLoad={() => setLoading(false)}
        onError={() => {
          setImgSrc(fallbackSrc);
          setLoading(false);
        }}
        {...props}
      />
    </div>
  );
}
