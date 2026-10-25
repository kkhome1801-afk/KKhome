import Link from "next/link";
import { ArrowLeft, BookOpen, ExternalLink } from "lucide-react";
import legalDocs from "@/data/legal-docs.json";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { slug } = await params;
  const doc = legalDocs.find((d) => d.slug === slug);
  return {
    title: doc ? `${doc.shortTitle} · Tra cứu đầy đủ — KKhome` : "Tra cứu Văn bản Pháp luật — KKhome",
    description: doc?.description || "Hệ thống tra cứu Văn bản Pháp luật KKhome",
  };
}

export default async function LegalDocPage({ params }: PageProps) {
  const { slug } = await params;
  const doc = legalDocs.find((d) => d.slug === slug);

  const title = doc?.title || slug.toUpperCase();
  const shortTitle = doc?.shortTitle || slug;
  const iframeSrc = `/api/legal/${slug}`;

  return (
    <div className="flex flex-col h-screen bg-[#0e1220] text-gray-100 overflow-hidden">
      {/* Top Header Bar */}
      <header className="h-14 border-b border-[#2b3566] bg-[#141a30] px-4 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3 min-w-0">
          <Link
            href="/legal"
            className="flex items-center gap-1.5 text-xs sm:text-sm font-medium text-blue-400 hover:text-blue-300 transition-colors px-2.5 py-1.5 rounded-lg bg-[#1a2140] hover:bg-[#202a52] shrink-0"
          >
            <ArrowLeft className="w-4 h-4" />
            <span className="hidden sm:inline">Pháp luật</span>
          </Link>

          <span className="text-[#6f78ad] hidden sm:inline">/</span>

          <div className="flex items-center gap-2 min-w-0">
            <span className="text-xs px-2 py-0.5 rounded font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 shrink-0">
              {shortTitle}
            </span>
            <h1 className="text-sm font-semibold truncate text-[#eef1ff]">
              {title}
            </h1>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          {doc?.hasForms && (
            <span className="hidden md:inline-flex text-xs px-2 py-0.5 rounded font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              Có biểu mẫu
            </span>
          )}
          <a
            href={iframeSrc}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-xs text-[#9aa3d4] hover:text-white px-2.5 py-1.5 rounded-lg bg-[#1a2140] hover:bg-[#202a52] transition-colors"
            title="Mở toàn màn hình"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Cửa sổ mới</span>
          </a>
        </div>
      </header>

      {/* Main Interactive Viewer Iframe */}
      <main className="flex-1 w-full bg-[#0e1220] relative">
        <iframe
          src={iframeSrc}
          className="w-full h-full border-0"
          title={title}
          style={{ backgroundColor: "#0e1220" }}
          sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-top-navigation-by-user-activation allow-forms"
        />
      </main>
    </div>
  );
}
