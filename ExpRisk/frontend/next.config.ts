import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      // API routes
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/api/:path*',
      },
      // WebSocket route
      {
        source: '/chat',
        destination: 'http://127.0.0.1:8000/chat',
      },
      // Documentation routes
      {
        source: '/docs',
        destination: 'http://127.0.0.1:8000/api/docs',
      },
      {
        source: '/redoc',
        destination: 'http://127.0.0.1:8000/api/redoc',
      },
    ];
  },
};

export default nextConfig;
