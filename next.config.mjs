/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: '10mb',
    },
  },
  async rewrites() {
    return {
      afterFiles: [
        {
          source: '/recruiter',
          destination: '/recruiter/index.html',
        },
        {
          source: '/recruiter/apply/:jobId',
          destination: '/recruiter/index.html',
        },
      ],
    };
  },
};

export default nextConfig;
