'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Video, Loader2, CheckCircle2, XCircle, Film, Sparkles, Download } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Project {
  id: string;
  title: string;
  topic: string;
  language: string;
  status: string;
  created_at: string;
  updated_at: string;
  progress: number;
  video_url?: string;
  error_message?: string;
}

export default function Home() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    topic: '',
    language: 'ar',
    voice_gender: 'male',
    duration_minutes: 3,
    style: 'informative'
  });

  // Fetch projects
  const fetchProjects = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/projects`);
      setProjects(response.data.projects || []);
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    }
  };

  useEffect(() => {
    fetchProjects();
    const interval = setInterval(fetchProjects, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axios.post(`${API_URL}/api/v1/projects/create`, formData);
      
      // Reset form
      setFormData({
        title: '',
        topic: '',
        language: 'ar',
        voice_gender: 'male',
        duration_minutes: 3,
        style: 'informative'
      });

      // Refresh projects list
      await fetchProjects();
    } catch (error) {
      console.error('Failed to create project:', error);
      alert('فشل في إنشاء المشروع. يرجى المحاولة مرة أخرى.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />;
    }
  };

  const getStatusText = (status: string) => {
    const statusMap: { [key: string]: string } = {
      created: 'تم الإنشاء',
      generating_script: 'توليد السكريبت...',
      generating_voice: 'توليد الصوت...',
      generating_video: 'تجميع الفيديو...',
      completed: 'مكتمل',
      failed: 'فشل'
    };
    return statusMap[status] || status;
  };

  return (
    <div className="min-h-screen p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 animate-fadeIn">
          <div className="flex justify-center items-center gap-3 mb-4">
            <Film className="w-12 h-12 text-primary-500" />
            <h1 className="text-5xl font-bold gradient-text">استوديو الفيديو الذكي</h1>
          </div>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            منصة مجانية متكاملة لأتمتة إنتاج فيديوهات اليوتيوب باستخدام تقنيات الذكاء الاصطناعي 🎬
          </p>
        </div>

        {/* Create Project Form */}
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl shadow-2xl p-8 mb-8 border border-gray-700 card-hover">
          <div className="flex items-center gap-3 mb-6">
            <Sparkles className="w-6 h-6 text-primary-500" />
            <h2 className="text-2xl font-bold text-white">إنشاء فيديو جديد</h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Title */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  عنوان الفيديو *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="مثال: دليل المبتدئين للذكاء الاصطناعي"
                />
              </div>

              {/* Language */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  اللغة
                </label>
                <select
                  value={formData.language}
                  onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                >
                  <option value="ar">العربية</option>
                  <option value="en">English</option>
                </select>
              </div>
            </div>

            {/* Topic */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                موضوع الفيديو *
              </label>
              <textarea
                required
                value={formData.topic}
                onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                rows={4}
                className="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                placeholder="اكتب وصفاً تفصيلياً للموضوع الذي تريد إنشاء فيديو عنه..."
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Voice Gender */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  جنس الصوت
                </label>
                <select
                  value={formData.voice_gender}
                  onChange={(e) => setFormData({ ...formData, voice_gender: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                >
                  <option value="male">ذكر</option>
                  <option value="female">أنثى</option>
                </select>
              </div>

              {/* Duration */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  المدة (دقائق)
                </label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={formData.duration_minutes}
                  onChange={(e) => setFormData({ ...formData, duration_minutes: parseInt(e.target.value) })}
                  className="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                />
              </div>

              {/* Style */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  الأسلوب
                </label>
                <select
                  value={formData.style}
                  onChange={(e) => setFormData({ ...formData, style: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                >
                  <option value="informative">معلوماتي</option>
                  <option value="educational">تعليمي</option>
                  <option value="entertaining">ترفيهي</option>
                  <option value="motivational">تحفيزي</option>
                </select>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-bold py-4 px-6 rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg hover:shadow-primary-500/50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  جاري الإنشاء...
                </>
              ) : (
                <>
                  <Video className="w-5 h-5" />
                  إنشاء الفيديو
                </>
              )}
            </button>
          </form>
        </div>

        {/* Projects List */}
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl shadow-2xl p-8 border border-gray-700">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <Video className="w-6 h-6 text-primary-500" />
            المشاريع
          </h2>

          {projects.length === 0 ? (
            <div className="text-center py-12 text-gray-400">
              <Film className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p>لا توجد مشاريع بعد. ابدأ بإنشاء فيديو جديد!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {projects.map((project) => (
                <div
                  key={project.id}
                  className="bg-gray-700/30 rounded-lg p-6 border border-gray-600 hover:border-primary-500/50 transition-all"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-white mb-2">{project.title}</h3>
                      <p className="text-gray-400 text-sm mb-3 line-clamp-2">{project.topic}</p>
                      <div className="flex items-center gap-3 text-sm text-gray-500">
                        <span>{project.language === 'ar' ? 'العربية' : 'English'}</span>
                        <span>•</span>
                        <span>{new Date(project.created_at).toLocaleDateString('ar-SA')}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {getStatusIcon(project.status)}
                      <span className="text-sm text-gray-300">{getStatusText(project.status)}</span>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  {project.status !== 'completed' && project.status !== 'failed' && (
                    <div className="mb-4">
                      <div className="w-full bg-gray-600 rounded-full h-2 overflow-hidden">
                        <div
                          className="progress-bar bg-gradient-to-r from-primary-500 to-primary-600 h-2"
                          style={{ width: `${project.progress}%` }}
                        />
                      </div>
                      <p className="text-xs text-gray-400 mt-1">{project.progress}%</p>
                    </div>
                  )}

                  {/* Download Button */}
                  {project.status === 'completed' && project.video_url && (
                    <a
                      href={`${API_URL}${project.video_url}`}
                      download
                      className="inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-all"
                    >
                      <Download className="w-4 h-4" />
                      تحميل الفيديو
                    </a>
                  )}

                  {/* Error Message */}
                  {project.status === 'failed' && project.error_message && (
                    <div className="bg-red-900/30 border border-red-700 rounded-lg p-3">
                      <p className="text-red-300 text-sm">{project.error_message}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500">
          <p className="text-sm">
            مصنوع بـ ❤️ باستخدام Groq API + Edge-TTS + MoviePy
          </p>
          <p className="text-xs mt-2">
            100% مجاني • بدون OpenAI • مفتوح المصدر
          </p>
        </div>
      </div>
    </div>
  );
}
