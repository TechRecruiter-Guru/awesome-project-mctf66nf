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
      // afterFiles rewrites run AFTER static files are checked
      // So /recruiter/static/js/main.js will serve the file directly
      // But /recruiter or /recruiter/apply/1 will serve index.html (SPA routing)
      afterFiles: [
        {
          source: '/recruiter',
          destination: '/recruiter/index.html',
        },
        {
          source: '/recruiter/:path((?!static).*)',
          destination: '/recruiter/index.html',
        },
      ],
    };
  },
};

export default nextConfig;
