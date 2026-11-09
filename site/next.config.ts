import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Static export: deploy the out/ folder to any host.
  output: 'export',
  // Brand renders are served exactly as produced by the render pipeline: never resized or recompressed.
  images: { unoptimized: true },
};

export default nextConfig;
