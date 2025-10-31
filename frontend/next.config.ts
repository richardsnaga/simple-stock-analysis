import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: 'export',
  // Production di comment
  // async rewrites() {
  //   return [
  //     {
  //       source: "/api/:path*",
  //       // destination: "http://localhost:8000/api/:path*", // dev
  //       destination: "http://backend:8000/api/:path*", // production
  //     },
  //   ];
  // },
};

export default nextConfig;
