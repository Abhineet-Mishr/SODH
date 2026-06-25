export type PreviewRow = Record<string, string | number | null | undefined>

export type ConvertResponse = {
  job_id: string
  source_type: string
  conversion: string
  records: number
  preview: PreviewRow[]
  download_name: string
  download_url: string
  artifact: {
    artifact_id: string
    filename: string
    download_url: string
    mime_type: string
    size_bytes: number
  }
}

export type ArtifactInfo = {
  artifact_id: string
  filename: string
  download_url: string
  mime_type: string
  size_bytes: number
}

export type DeduplicateResponse = {
  job_id: string
  preview: PreviewRow[]
  master_preview: PreviewRow[]
  review_preview: PreviewRow[]
  report: Record<string, unknown>
  artifacts: Record<string, ArtifactInfo>
  finalized: boolean
}
