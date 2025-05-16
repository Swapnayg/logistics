import FormAccountReports from "@/components/FormAccountReports";
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
        <FormAccountReports />
      </MasterLayout>
    </>
  );
};

export default Page;
