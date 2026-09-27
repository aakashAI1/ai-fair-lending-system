"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { apiClient, createUploadConfig } from "@/lib/api-client"

interface UploadStatus {
  status: "idle" | "uploading" | "processing" | "success" | "error"
  message: string
  imported?: number
  total?: number
}

export default function DataUpload() {
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>({
    status: "idle",
    message: "",
  })
  const [isDragging, setIsDragging] = useState(false)

  const handleFileUpload = async (file: File) => {
    if (!file.name.endsWith(".zip") && !file.name.endsWith(".csv")) {
      setUploadStatus({
        status: "error",
        message: "Please upload a ZIP file (containing .pl or .csv files) or a CSV file",
      })
      return
    }

    const formData = new FormData()
    formData.append("file", file)

    try {
      setUploadStatus({
        status: "uploading",
        message: "Uploading file...",
      })

      // Upload file - use special config for file uploads
      const uploadResponse = await apiClient.post("/profiles/upload", formData, createUploadConfig(120000))

      setUploadStatus({
        status: "processing",
        message: "Processing and importing data...",
      })

      // Poll for processing status
      const checkStatus = async (jobId: string) => {
        try {
          const statusResponse = await apiClient.get(`/api/v1/profiles/upload/status/${jobId}`)
          const { status, progress, imported, total, error } = statusResponse.data

          if (status === "completed") {
            setUploadStatus({
              status: "success",
              message: `Successfully imported ${imported} student profiles!`,
              imported,
              total,
            })
            // Refresh the page after 2 seconds to show new data
            setTimeout(() => {
              window.location.reload()
            }, 2000)
          } else if (status === "failed") {
            setUploadStatus({
              status: "error",
              message: error || "Failed to process file",
            })
          } else if (status === "processing") {
            setUploadStatus({
              status: "processing",
              message: `Processing... ${progress || 0}%`,
              imported,
              total,
            })
            // Poll again after 1 second
            setTimeout(() => checkStatus(jobId), 1000)
          }
        } catch (err: any) {
          setUploadStatus({
            status: "error",
            message: err.response?.data?.detail || "Error checking status",
          })
        }
      }

      if (uploadResponse.data.job_id) {
        await checkStatus(uploadResponse.data.job_id)
      } else {
        // If no job ID, assume immediate completion
        setUploadStatus({
          status: "success",
          message: "File uploaded successfully!",
        })
        setTimeout(() => {
          window.location.reload()
        }, 2000)
      }
    } catch (error: any) {
      setUploadStatus({
        status: "error",
        message: error.response?.data?.detail || error.message || "Failed to upload file",
      })
    }
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file) {
      handleFileUpload(file)
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFileUpload(file)
    }
  }

  const getStatusColor = () => {
    switch (uploadStatus.status) {
      case "success":
        return "border-green-500 bg-green-50"
      case "error":
        return "border-red-500 bg-red-50"
      case "uploading":
      case "processing":
        return "border-blue-500 bg-blue-50"
      default:
        return "border-gray-300 bg-white"
    }
  }

  const getStatusIcon = () => {
    switch (uploadStatus.status) {
      case "success":
        return "✅"
      case "error":
        return "❌"
      case "uploading":
      case "processing":
        return "⏳"
      default:
        return "📁"
    }
  }

  return (
    <Card className={`${getStatusColor()} transition-colors`}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <span>{getStatusIcon()}</span>
          Upload Student Profile Data
        </CardTitle>
        <CardDescription>
          Upload a ZIP file containing student loan data. The system will automatically process and import the profiles.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div
          onDrop={handleDrop}
          onDragOver={(e) => {
            e.preventDefault()
            setIsDragging(true)
          }}
          onDragLeave={() => setIsDragging(false)}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
            transition-all duration-200
            ${isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-gray-400"}
          `}
          onClick={() => document.getElementById("file-upload")?.click()}
        >
            <input
            id="file-upload"
            type="file"
            accept=".zip,.csv"
            className="hidden"
            onChange={handleFileSelect}
          />
          <div className="space-y-4">
            <div className="text-4xl">📤</div>
            <div>
              <p className="text-lg font-medium">
                {isDragging ? "Drop file here" : "Click to upload or drag and drop"}
              </p>
              <p className="text-sm text-gray-500 mt-2">
                ZIP file (with .pl or .csv) or CSV file containing student profile data
              </p>
            </div>
          </div>
        </div>

        {uploadStatus.status !== "idle" && (
          <div className="mt-4 p-4 bg-white rounded-lg border">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{uploadStatus.message}</p>
                {uploadStatus.imported !== undefined && uploadStatus.total !== undefined && (
                  <p className="text-sm text-gray-500 mt-1">
                    Imported {uploadStatus.imported} of {uploadStatus.total} profiles
                  </p>
                )}
              </div>
              {uploadStatus.status === "processing" && (
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
              )}
            </div>
            {uploadStatus.status === "processing" && uploadStatus.total && (
              <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{
                    width: `${((uploadStatus.imported || 0) / uploadStatus.total) * 100}%`,
                  }}
                ></div>
              </div>
            )}
          </div>
        )}

        <div className="mt-4 text-xs text-gray-500">
          <p>Supported formats:</p>
          <ul className="list-disc list-inside mt-1 space-y-1">
            <li>ZIP files containing Prolog (.pl) files</li>
            <li>ZIP files containing CSV files</li>
            <li>Direct CSV file upload</li>
          </ul>
          <p className="mt-2">
            The system will automatically detect the format and process student loan data.
          </p>
        </div>
      </CardContent>
    </Card>
  )
}

