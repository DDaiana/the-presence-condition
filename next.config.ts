import type { NextConfig } from 'next';

const isGitHubPages = process.env.GITHUB_ACTIONS === 'true';

const nextConfig: NextConfig = {
  output: isGitHubPages ? 'export' : undefined,
  trailingSlash: isGitHubPages,
  basePath: isGitHubPages ? '/the-presence-condition' : '',
  assetPrefix: isGitHubPages ? '/the-presence-condition/' : undefined,
  images: { unoptimized: true },
};

export default nextConfig;
