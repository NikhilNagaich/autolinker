export interface BlogData {
    id: string;
    title: string;
    content: string;
    url: string;
    publishedDate: string;
}

export interface JobStatus {
    jobId: string;
    status: 'pending' | 'in_progress' | 'completed' | 'failed';
    progress: number; // percentage
}

export interface ExtractedResults {
    blogs: BlogData[];
    totalCount: number;
}