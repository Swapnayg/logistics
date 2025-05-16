import FormRecNewInvoice from "@/components/FormRecNewInvoice";
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
        <FormRecNewInvoice />
      </MasterLayout>
    </>
  );
};

export default Page;
