import { Navbar } from '@/components/layout/navbar'
import { createClient } from '@/lib/supabase/server'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Thông tư 89/2026/TT-BTC - Tra cứu pháp luật | KKhome',
  description: 'Hệ thống tra cứu điện tử và phân tích chuyên sâu Thông tư số 89/2026/TT-BTC của Bộ Tài chính.',
}

export default async function ThongTu89Page() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  let profile = null
  if (user) {
    const { data } = await supabase.from('profiles').select('*').eq('id', user.id).single()
    profile = data
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <Navbar user={user} isAdmin={profile?.is_admin} />
      <main className="flex-1 w-full h-[calc(100vh-64px)] relative">
        <iframe
          src="/vbpl/thong-tu-89-2026/index.html"
          className="w-full h-full border-none block"
          title="Thông tư 89/2026/TT-BTC - Tra cứu toàn văn và phân tích"
        />
      </main>
    </div>
  )
}
