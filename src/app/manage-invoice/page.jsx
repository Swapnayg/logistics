import FormManageInvoice from "@/components/FormManageInvoice";
import Breadcrumb from "@/components/Breadcrumb";
import MasterLayout from "@/masterLayout/MasterLayout";

export const metadata = {
  title: "Sales Dashboard",
  description:
    "Sales Dashboard.",
};

const Page = () => {
  return (
    <>
      {/* MasterLayout */}
      <MasterLayout>
        {/* Breadcrumb */}
        <Breadcrumb title='Blog Details' />

        {/* AddBlogLayer */}
        <FormManageInvoice />
      </MasterLayout>
    </>
  );
};

export default Page;
