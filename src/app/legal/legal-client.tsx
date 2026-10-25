"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { Search, BookOpen, Calendar, ArrowUpRight, FileSpreadsheet, ShieldCheck, Tag } from "lucide-react";

export interface LegalDoc {
  slug: string;
  title: string;
  shortTitle: string;
  description: string;
  effectiveDate: string;
  docType: string;
  categories: string[];
  status: string;
  hasForms: boolean;
  crossRefsCount: number;
}

interface LegalClientProps {
  initialDocs: LegalDoc[];
}

const CATEGORIES = [
  "Tất cả",
  "Chế độ kế toán",
  "Thuế TNDN",
  "Thuế GTGT",
  "Thuế TNCN",
  "Quản lý thuế",
  "Hóa đơn chứng từ",
  "Lao động & Tiền lương",
  "BHXH & Phúc lợi",
];

export function LegalClient({ initialDocs }: LegalClientProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("Tất cả");
  const [selectedDocType, setSelectedDocType] = useState("Tất cả");

  const filteredDocs = useMemo(() => {
    return initialDocs.filter((doc) => {
      // Search filter
      const q = searchQuery.toLowerCase().trim();
      const matchSearch =
        !q ||
        doc.title.toLowerCase().includes(q) ||
        doc.shortTitle.toLowerCase().includes(q) ||
        doc.description.toLowerCase().includes(q) ||
        doc.slug.toLowerCase().includes(q);

      // Category filter
      const matchCategory =
        selectedCategory === "Tất cả" ||
        doc.categories.some(
          (c) =>
            c.toLowerCase().includes(selectedCategory.toLowerCase()) ||
            selectedCategory.toLowerCase().includes(c.toLowerCase())
        );

      // Doc type filter
      const matchDocType =
        selectedDocType === "Tất cả" || doc.docType === selectedDocType;

      return matchSearch && matchCategory && matchDocType;
    });
  }, [initialDocs, searchQuery, selectedCategory, selectedDocType]);

  const docTypes = ["Tất cả", "Luật", "Nghị định", "Thông tư", "Công văn"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 pb-20">
      {/* Hero Header */}
      <div className="relative border-b border-slate-800 bg-gradient-to-b from-slate-900 via-slate-950 to-slate-950 px-4 py-12 md:py-16">
        <div className="max-w-7xl mx-auto text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Hệ thống Pháp luật & Kế toán Doanh nghiệp Chuẩn 2026</span>
          </div>

          <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-white">
            Tra cứu <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Văn bản Pháp luật</span>
          </h1>

          <p className="text-sm md:text-base text-slate-400 max-w-2xl mx-auto">
            Tổng hợp đầy đủ quy định, thông tư kế toán, luật thuế, biểu mẫu và cẩm nang thủ tục cập nhật mới nhất cho doanh nghiệp và hộ kinh doanh.
          </p>

          {/* Search Box */}
          <div className="max-w-2xl mx-auto pt-4">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                placeholder="Tìm kiếm theo số hiệu (89/2026, 99/2025...), tên luật, nội dung..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-4 py-3.5 bg-slate-900 border border-slate-700 rounded-xl text-sm md:text-base text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all shadow-lg"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery("")}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-400 hover:text-white"
                >
                  Xóa
                </button>
              )}
            </div>
          </div>

          {/* Category Filter Pills */}
          <div className="flex flex-wrap items-center justify-center gap-2 pt-4 max-w-4xl mx-auto">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  selectedCategory === cat
                    ? "bg-blue-600 text-white shadow-md shadow-blue-500/25"
                    : "bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-800"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Doc Type Filter Pills */}
          <div className="flex flex-wrap items-center justify-center gap-2 pt-1 text-xs">
            <span className="text-slate-500 mr-1 flex items-center gap-1">
              <Tag className="w-3 h-3" /> Loại VB:
            </span>
            {docTypes.map((type) => (
              <button
                key={type}
                onClick={() => setSelectedDocType(type)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium transition-all ${
                  selectedDocType === type
                    ? "bg-slate-700 text-white"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Grid Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between pb-6 border-b border-slate-800/80 mb-6">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-400" />
            <span className="font-semibold text-slate-200">
              Danh sách văn bản ({filteredDocs.length})
            </span>
          </div>

          {searchQuery && (
            <span className="text-xs text-slate-400">
              Kết quả cho &ldquo;{searchQuery}&rdquo;
            </span>
          )}
        </div>

        {filteredDocs.length === 0 ? (
          <div className="text-center py-20 text-slate-500 space-y-3">
            <p className="text-base">Không tìm thấy văn bản phù hợp với tìm kiếm của bạn.</p>
            <button
              onClick={() => {
                setSearchQuery("");
                setSelectedCategory("Tất cả");
                setSelectedDocType("Tất cả");
              }}
              className="text-xs text-blue-400 hover:underline"
            >
              Đặt lại bộ lọc
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filteredDocs.map((doc) => {
              const isHighlight = doc.slug === "tt89";

              return (
                <Link
                  key={doc.slug}
                  href={`/legal/${doc.slug}`}
                  className={`group flex flex-col justify-between p-5 rounded-xl border transition-all duration-200 hover:-translate-y-1 hover:shadow-xl ${
                    isHighlight
                      ? "bg-gradient-to-br from-blue-950/40 via-slate-900 to-slate-900 border-blue-500/50 hover:border-blue-400 hover:shadow-blue-500/10 ring-1 ring-blue-500/30"
                      : "bg-slate-900/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900"
                  }`}
                >
                  <div className="space-y-3">
                    {/* Top Row: Type, ShortTitle, Form badge */}
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="text-[11px] px-2 py-0.5 rounded font-mono font-bold bg-slate-800 text-slate-300 border border-slate-700">
                          {doc.docType}
                        </span>
                        <span
                          className={`text-xs font-bold font-mono px-2 py-0.5 rounded ${
                            isHighlight
                              ? "bg-blue-500 text-white"
                              : "bg-blue-500/15 text-blue-300 border border-blue-500/30"
                          }`}
                        >
                          {doc.shortTitle}
                        </span>
                      </div>

                      {doc.hasForms && (
                        <span className="flex items-center gap-1 text-[11px] font-medium text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
                          <FileSpreadsheet className="w-3 h-3" />
                          Có biểu mẫu
                        </span>
                      )}
                    </div>

                    {/* Title */}
                    <h3 className="font-semibold text-slate-100 group-hover:text-blue-400 transition-colors line-clamp-2 text-base">
                      {doc.title}
                    </h3>

                    {/* Description */}
                    <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed">
                      {doc.description}
                    </p>
                  </div>

                  {/* Bottom Meta */}
                  <div className="pt-4 mt-4 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                    <div className="flex items-center gap-1.5">
                      <Calendar className="w-3.5 h-3.5 text-slate-500" />
                      <span>{doc.effectiveDate}</span>
                    </div>

                    <div className="flex items-center gap-1 text-blue-400 group-hover:text-blue-300 font-medium">
                      <span>Mở</span>
                      <ArrowUpRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
