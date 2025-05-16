import FormManageCustomerGp from "@/components/FormManageCustomerGp";
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
        <FormManageCustomerGp />
      </MasterLayout>
    </>
  );
};

export default Page;
