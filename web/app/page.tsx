import { Sidebar, MobileBar } from '@/components/nav';
import { Lightbox } from '@/components/lightbox';
import Overview from '@/components/sections/01-overview';
import Brief from '@/components/sections/02-brief';
import Logo from '@/components/sections/03-logo';
import Colour from '@/components/sections/04-colour';
import Type from '@/components/sections/05-type';
import Icons from '@/components/sections/06-icons';
import Components from '@/components/sections/07-components';
import Three from '@/components/sections/08-three';
import Motion from '@/components/sections/09-motion';
import Imagery from '@/components/sections/10-imagery';
import Stationery from '@/components/sections/11-stationery';
import Marketing from '@/components/sections/12-marketing';
import Merch from '@/components/sections/13-merch';
import Facility from '@/components/sections/14-facility';
import Products from '@/components/sections/15-products';
import Files from '@/components/sections/16-files';

export default function Page() {
  return (
    <>
      <MobileBar />
      <div className="shell">
        <Sidebar />
        <main>
          <Overview /><Brief /><Logo /><Colour /><Type /><Icons /><Components />
          <Three /><Motion /><Imagery />
          <Stationery /><Marketing /><Merch /><Facility /><Products /><Files />
          <footer>
            <img src="/assets/logo/primary-charcoal.svg" alt="Mustard Bio" style={{ width: '220px' }} />
            <span className="lab">Mustard Bio · Brand identity v1.2 · Measured, not guessed.</span>
          </footer>
        </main>
      </div>
      <Lightbox />
    </>
  );
}
