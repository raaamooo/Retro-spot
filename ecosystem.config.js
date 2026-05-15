// PM2 ecosystem config — manages both the backend API and the Next.js frontend.
// Usage:
//   pm2 start ecosystem.config.js   (start both)
//   pm2 stop all                     (stop both)
//   pm2 restart all                  (restart both)
//   pm2 logs                         (live logs)
//   pm2 save && pm2 startup          (persist across reboots)

module.exports = {
  apps: [
    {
      name: 'retro-backend',
      cwd: './backend',
      // In production use the compiled JS output; in dev use tsx directly.
      script: 'node',
      args: 'dist/server.js',
      interpreter: 'none',
      env: {
        NODE_ENV: 'production',
      },
      // Auto-restart on crash, with exponential back-off
      autorestart: true,
      max_restarts: 10,
      restart_delay: 2000,
      // Log rotation
      error_file: '../logs/backend-error.log',
      out_file: '../logs/backend-out.log',
      merge_logs: true,
    },
    {
      name: 'retro-frontend',
      cwd: './frontend',
      script: 'node',
      args: '.next/standalone/server.js',
      interpreter: 'none',
      env: {
        NODE_ENV: 'production',
        PORT: '3000',
        HOSTNAME: '0.0.0.0',
      },
      autorestart: true,
      max_restarts: 10,
      restart_delay: 2000,
      error_file: '../logs/frontend-error.log',
      out_file: '../logs/frontend-out.log',
      merge_logs: true,
    },
  ],
};
