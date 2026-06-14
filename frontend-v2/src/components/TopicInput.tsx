interface Props {
  onSubmit: (topic: string) => void
  disabled: boolean
}

export default function TopicInput({ onSubmit, disabled }: Props) {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const form = e.currentTarget
    const input = form.elements.namedItem('topic') as HTMLInputElement
    const val = input.value.trim()
    if (val) onSubmit(val)
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        name="topic"
        type="text"
        placeholder="輸入數學主題，例如：畢達哥拉斯定理、微積分基本定理…"
        disabled={disabled}
        className="flex-1 rounded-xl border border-slate-700 bg-slate-800/60 px-4 py-3 text-slate-100 placeholder-slate-500 outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={disabled}
        className="rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {disabled ? '生成中…' : '開始生成'}
      </button>
    </form>
  )
}
