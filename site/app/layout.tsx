import type { Metadata, Viewport } from 'next';
import { IBM_Plex_Sans, IBM_Plex_Mono } from 'next/font/google';
import { Nav } from '@/components/nav';
import { Footer } from '@/components/footer';
import { Reveal } from '@/components/reveal';
import { TAGLINE, HOME } from '@/lib/copy';
import './globals.css';

const sans = IBM_Plex_Sans({ subsets: ['latin'], weight: ['300', '400', '500'], variable: '--font-sans', display: 'swap' });
const mono = IBM_Plex_Mono({ subsets: ['latin'], weight: ['400', '500'], variable: '--font-mono', display: 'swap' });

export const metadata: Metadata = {
  title: { default: `Mustard Bio · ${TAGLINE}`, template: '%s · Mustard Bio' },
  description: HOME.hero.sub,
  icons: { icon: '/assets/logo/app-icon.svg' },
  openGraph: { title: 'Mustard Bio', description: HOME.hero.sub, images: ['/assets/render/asset-mark-dark.jpg'] },
};
export const viewport: Viewport = { width: 'device-width', initialScale: 1, viewportFit: 'cover', themeColor: '#222F30' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${sans.variable} ${mono.variable}`}>
      <body>
        <noscript><style>{`[data-r]{opacity:1!important;transform:none!important}.title .ln>span,.rule rect,.ftr-rule i{transform:none!important}`}</style></noscript>
        <a href="#main" className="skip">Skip to content</a>
        <Nav />
        <main id="main">{children}</main>
        <Footer />
        <Reveal />
      </body>
    </html>
  );
}
