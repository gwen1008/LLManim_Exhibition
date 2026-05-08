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
        placeholder="Enter a math topic, e.g. Pythagorean theorem..."
        disabled={disabled}
        className="flex-1 rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-slate-100 placeholder-slate-500 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={disabled}
        className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {disabled ? 'Generating…' : 'Generate'}
      </button>
    </form>
  )
}
