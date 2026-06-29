import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { authApi } from '../api'

export function LoginPage() {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [securityKey, setSecurityKey] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const [isForgotPassword, setIsForgotPassword] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (isForgotPassword) {
        if (!email || !password || !securityKey) {
          setError('Email, New Password, and Security Key are required.')
          setLoading(false)
          return
        }
        await authApi.forgotPassword(email, securityKey, password)
        alert('Password successfully reset! Please log in.')
        setIsForgotPassword(false)
        setIsLogin(true)
      } else if (isLogin) {
        const response = await authApi.login(email, password)
        const user = await authApi.fetchMe(response.access_token)
        login(response.access_token, user)
      } else {
        if (!securityKey) {
          setError('Security key is required for registration')
          setLoading(false)
          return
        }
        await authApi.register(email, password, securityKey)
        const response = await authApi.login(email, password)
        const user = await authApi.fetchMe(response.access_token)
        login(response.access_token, user)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-slate-50 items-center justify-center p-4">
      <div className="flex w-full max-w-4xl overflow-hidden rounded-2xl bg-white shadow-xl h-[600px]">
        {/* Left Section - Hero/Branding */}
        <div className="hidden w-1/2 flex-col justify-between bg-[#3F3B7C] p-10 text-white md:flex">
          <div>
            <div className="flex items-center gap-2">
              <span className="rounded-lg bg-white/20 p-2 font-bold leading-none tracking-wider opacity-80 backdrop-blur-sm">SODH</span>
              <div className="flex flex-col">
                <span className="text-lg font-bold leading-none">Literature Toolkit</span>
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-300">Research Collaboration</span>
              </div>
            </div>

            <div className="mt-10 mb-4 inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-white/10 px-3 py-1 text-xs font-medium backdrop-blur-sm">
              ✨ Build Serious Research Teams
            </div>

            <h1 className="mb-6 text-4xl font-extrabold leading-tight">
              From Idea to<br />Published Work,<br />Faster.
            </h1>

            <p className="text-sm leading-relaxed text-slate-200">
              Discover projects, apply with commitment, and execute in a shared workspace built for academic and interdisciplinary teams.
            </p>
          </div>

          <div className="space-y-4">
            <div className="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur-md">
              <h3 className="font-semibold text-white">Cross-Disciplinary Teams</h3>
              <p className="mt-1 text-xs text-slate-300">Find collaborators across CS, bio, engineering, and social science.</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur-md">
              <h3 className="font-semibold text-white">Project Workspace</h3>
              <p className="mt-1 text-xs text-slate-300">Track milestones, assignments, and outcomes in one research dashboard.</p>
            </div>
          </div>
        </div>

        {/* Right Section - Auth Form */}
        <div className="flex w-full flex-col justify-center px-10 py-12 md:w-1/2 lg:px-16">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-slate-900">
              {isForgotPassword ? 'Reset Password' : isLogin ? 'Welcome Back' : 'Create Account'}
            </h2>
            <p className="mt-2 text-sm text-slate-600">
              {isForgotPassword ? 'Enter your email, security key, and new password.' : isLogin ? 'Sign in to continue your research collaborations.' : 'Join to find teams and publish faster.'}
            </p>
          </div>

          {!isForgotPassword && (
            <div className="mb-8 flex rounded-lg bg-slate-100 p-1">
              <button
                type="button"
                className={`flex-1 rounded-md py-2 text-sm font-medium transition-colors ${
                  isLogin ? 'bg-[#3F3B7C] text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
                onClick={() => setIsLogin(true)}
              >
                Sign In
              </button>
              <button
                type="button"
                className={`flex-1 rounded-md py-2 text-sm font-medium transition-colors ${
                  !isLogin ? 'bg-[#3F3B7C] text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
                onClick={() => setIsLogin(false)}
              >
                Create Account
              </button>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
                {error}
              </div>
            )}

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Email</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@university.edu"
                className="w-full rounded-lg border border-slate-300 px-4 py-2.5 text-sm transition-colors focus:border-[#3F3B7C] focus:outline-none focus:ring-1 focus:ring-[#3F3B7C]"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">
                {isForgotPassword ? 'New Password' : 'Password'}
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Minimum 8 characters"
                className="w-full rounded-lg border border-slate-300 px-4 py-2.5 text-sm transition-colors focus:border-[#3F3B7C] focus:outline-none focus:ring-1 focus:ring-[#3F3B7C]"
              />
            </div>

            {(!isLogin || isForgotPassword) && (
              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">Security Key (Recovery)</label>
                <input
                  type="text"
                  required
                  value={securityKey}
                  onChange={(e) => setSecurityKey(e.target.value)}
                  placeholder="Letters + digits + special character"
                  className="w-full rounded-lg border border-slate-300 px-4 py-2.5 text-sm transition-colors focus:border-[#3F3B7C] focus:outline-none focus:ring-1 focus:ring-[#3F3B7C]"
                />
              </div>
            )}

            <div className="flex items-center justify-between">
              {!isForgotPassword && isLogin && (
                <>
                  <label className="flex items-center gap-2">
                    <input type="checkbox" className="rounded border-slate-300 text-[#3F3B7C] focus:ring-[#3F3B7C]" />
                    <span className="text-sm text-slate-600">Remember Me</span>
                  </label>
                  <button
                    type="button"
                    onClick={() => { setIsForgotPassword(true); setError(''); }}
                    className="text-sm font-medium text-[#3F3B7C] hover:underline"
                  >
                    Forgot Password?
                  </button>
                </>
              )}
              {isForgotPassword && (
                 <button
                  type="button"
                  onClick={() => { setIsForgotPassword(false); setIsLogin(true); setError(''); }}
                  className="text-sm font-medium text-[#3F3B7C] hover:underline"
                 >
                   Back to Login
                 </button>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-[#3F3B7C] py-3 text-sm font-medium text-white transition-colors hover:bg-[#322F63] disabled:opacity-70 mt-4"
            >
              {loading ? 'Processing...' : isForgotPassword ? 'Reset Password' : isLogin ? 'Sign In to Toolkit →' : 'Create Account →'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
