interface Props {
  videoPath: string | null
}

export default function VideoPlayer({ videoPath }: Props) {
  if (!videoPath) return null

  return (
    <div className="rounded-2xl overflow-hidden border border-slate-800 bg-black">
      <video
        key={videoPath}
        src={`/video/${videoPath}`}
        controls
        autoPlay
        className="w-full"
      />
    </div>
  )
}
