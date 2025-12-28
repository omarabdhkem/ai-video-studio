import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Video Studio - استوديو الفيديو الذكي',
  description: 'منصة مجانية متكاملة لأتمتة إنتاج فيديوهات اليوتيوب باستخدام الذكاء الاصطناعي',
  keywords: ['AI', 'Video', 'YouTube', 'Automation', 'Arabic', 'الذكاء الاصطناعي', 'فيديو', 'يوتيوب'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ar" dir="rtl">
      <body className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        {children}
      </body>
    </html>
  )
}
