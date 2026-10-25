import Link from 'next/link'
import { Navbar } from '@/components/layout/navbar'
import { createClient } from '@/lib/supabase/server'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, BookOpen, FileText, Download, Scale, ShieldCheck, Sparkles } from 'lucide-react'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Tra cứu Văn bản Pháp luật (VBPL) | KKhome',
  description: 'Hệ thống tra cứu điện tử các thông tư, luật thuế và chế độ kế toán mới nhất.',
}

export default async function VbplIndexPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  let profile = null
  if (user) {
    const { data } = await supabase.from('profiles').select('*').eq('id', user.id).single()
    profile = data
  }

  const documents = [
    {
      id: 'thong-tu-89-2026',
      code: '89/2026/TT-BTC',
      title: 'Thông tư số 89/2026/TT-BTC',
      desc: 'Quy định chi tiết thi hành Luật Quản lý thuế số 108/2025/QH15 và Nghị định số 252/2026/NĐ-CP (Giao dịch điện tử, sàn TMĐT nộp thay thuế, kiểm tra trực tuyến từ xa).',
      effectiveDate: '01/07/2026',
      issuer: 'Bộ Tài chính',
      tags: ['Luật Quản lý thuế mới', '101 Điều', 'Ebook tra cứu', 'Sàn TMĐT'],
      href: '/vbpl/thong-tu-89-2026',
      wordUrl: '/VBan/Th%C3%B4ng%20t%C6%B0%2089-2026/Th%C3%B4ng%20t%C6%B0%2089-2026%20-%20T%E1%BB%95ng%20h%E1%BB%A3p%20&%20Ph%C3%A2n%20t%C3%ADch.docx',
      excelUrl: '/VBan/Th%C3%B4ng%20t%C6%B0%2089-2026/Th%C3%B4ng%20t%C6%B0%2089-2026%20-%20Danh%20m%E1%BB%A5c%20Bi%E1%BB%83u%20m%E1%BA%ABu%20&%20Th%E1%BB%A7%20t%E1%BB%A5c.xlsx',
      isNew: true,
    },
    {
      id: 'luat-67-2025',
      code: '67/2025/QH15',
      title: 'Luật Thuế Thu Nhập Doanh Nghiệp 2025',
      desc: 'Luật Thuế TNDN mới số 67/2025/QH15 điều chỉnh toàn diện về căn cứ tính thuế, thuế suất ưu đãi, thu nhập chịu thuế và điều khoản thi hành.',
      effectiveDate: '01/10/2025',
      issuer: 'Quốc hội Khóa XV',
      tags: ['Thuế TNDN', '20 Điều', 'Ưu đãi thuế', 'Cơ sở thường trú'],
      href: '/VBan/index.html',
      isNew: false,
    },
    {
      id: 'thong-tu-99-2025',
      code: '99/2025/TT-BTC',
      title: 'Thông tư số 99/2025/TT-BTC',
      desc: 'Hướng dẫn chế độ kế toán doanh nghiệp toàn diện: hệ thống chứng từ, tài khoản kế toán, sổ kế toán và lập Báo cáo tài chính.',
      effectiveDate: '01/01/2026',
      issuer: 'Bộ Tài chính',
      tags: ['Chế độ kế toán', 'Hệ thống TK', 'BCTC tự động'],
      href: '/VBan/index.html',
      isNew: false,
    }
  ]

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar user={user} isAdmin={profile?.is_admin} />

      {/* Header */}
      <section className="bg-slate-900 text-white py-14 px-4 sm:px-6 lg:px-8 border-b border-slate-800">
        <div className="max-w-6xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/30 text-blue-400 rounded-full px-3.5 py-1 text-xs font-semibold mb-4">
            <Scale className="w-3.5 h-3.5" />
            <span>Thư Viện Pháp Luật & Chế Độ Kế Toán</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">
            Hệ Thống Tra Cứu Văn Bản Pháp Luật (VBPL)
          </h1>
          <p className="text-slate-400 text-base max-w-2xl">
            Toàn văn thông tư, luật thuế mới, bản phân tích chuyên sâu và hệ thống biểu mẫu được số hóa tương tác giúp bạn tra cứu nhanh chóng, chính xác.
          </p>
        </div>
      </section>

      {/* Main List */}
      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-600" />
            Văn bản nổi bật & Cập nhật mới
          </h2>
          <span className="text-xs text-slate-500">Cập nhật liên tục theo Luật hiện hành</span>
        </div>

        <div className="grid grid-cols-1 gap-6">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-7 shadow-sm hover:shadow-md transition-all duration-200"
            >
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2.5 flex-wrap mb-2">
                    <span className="font-mono text-xs font-bold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-md border border-blue-200/60">
                      {doc.code}
                    </span>
                    <span className="text-xs text-slate-500">Ban hành: {doc.issuer}</span>
                    <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                      Hiệu lực: {doc.effectiveDate}
                    </span>
                    {doc.isNew && (
                      <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2.5 py-0.5 rounded-full border border-amber-200 inline-flex items-center gap-1">
                        <Sparkles className="w-3 h-3 text-amber-500" /> Mới cập nhật
                      </span>
                    )}
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2 hover:text-blue-600 transition-colors">
                    <Link href={doc.href}>{doc.title}</Link>
                  </h3>
                  <p className="text-sm text-slate-600 leading-relaxed mb-4">
                    {doc.desc}
                  </p>

                  <div className="flex items-center gap-2 flex-wrap">
                    {doc.tags.map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs font-medium text-slate-600 bg-slate-100 hover:bg-slate-200">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="flex sm:flex-col gap-2.5 sm:w-48 shrink-0 justify-end">
                  <Link href={doc.href} className="flex-1 sm:flex-initial">
                    <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl h-10 font-semibold gap-1.5 shadow-sm">
                      Vào tra cứu <ArrowRight className="w-4 h-4" />
                    </Button>
                  </Link>

                  {doc.wordUrl && (
                    <a href={doc.wordUrl} download className="flex-1 sm:flex-initial">
                      <Button variant="outline" size="sm" className="w-full text-xs rounded-xl h-8 text-slate-700 hover:text-blue-600 border-slate-200 gap-1.5">
                        <Download className="w-3.5 h-3.5" /> File Word (.docx)
                      </Button>
                    </a>
                  )}

                  {doc.excelUrl && (
                    <a href={doc.excelUrl} download className="flex-1 sm:flex-initial">
                      <Button variant="outline" size="sm" className="w-full text-xs rounded-xl h-8 text-slate-700 hover:text-emerald-600 border-slate-200 gap-1.5">
                        <FileText className="w-3.5 h-3.5" /> Biểu mẫu (.xlsx)
                      </Button>
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
