/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://dclaw-patent-backend:8140/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
