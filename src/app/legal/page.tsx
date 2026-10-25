import { Navbar } from "@/components/layout/navbar";
import { LegalClient } from "./legal-client";
import legalDocs from "@/data/legal-docs.json";

export const metadata = {
  title: "Văn bản Pháp luật — Hệ thống Tra cứu KKhome",
  description:
    "Kho tra cứu văn bản pháp luật, thuế và chế độ kế toán chuyên nghiệp cho doanh nghiệp và hộ kinh doanh.",
};

export default function LegalPage() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <Navbar />
      <main className="flex-1">
        <LegalClient initialDocs={legalDocs} />
      </main>
    </div>
  );
}
