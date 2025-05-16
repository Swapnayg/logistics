import Breadcrumb from "@/components/Breadcrumb";
import VoiceGeneratorLayer from "@/components/VoiceGeneratorLayer";
import WalletLayer from "@/components/WalletLayer";
import MasterLayout from "@/masterLayout/MasterLayout";

export const metadata = {
  title: "Wallet",
  description:
    "Wallet.",
};

const Page = () => {
  return (
    <>
      {/* MasterLayout */}
      <MasterLayout>
        {/* Breadcrumb */}
        <Breadcrumb title='Wallet' />

        {/* WalletLayer */}
        <WalletLayer />
      </MasterLayout>
    </>
  );
};

export default Page;
