interface Props {
  videoPath: string | null
}

export default function VideoPlayer({ videoPath }: Props) {
  if (!videoPath) return null

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 overflow-hidden">
      <div className="px-4 py-3 border-b border-slate-800 text-sm font-medium text-slate-400">
        Output Video
      </div>
      <div className="p-4">
        <video
          key={videoPath}
          src={`/video/${videoPath}`}
          controls
          autoPlay
          className="w-full rounded-lg bg-black"
        />
      </div>
    </div>
  )
}
