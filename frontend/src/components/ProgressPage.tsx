import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import CircularProgress from '@mui/material/CircularProgress';

const ProgressPage: React.FC = () => {
    const { jobId } = useParams<{ jobId: string }>();
    const [status, setStatus] = useState<string>('In Progress');
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!jobId) return;
        const interval = setInterval(async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/status/${jobId}`);
                const data = await response.json();
                if (data.status === 'completed') {
                    setStatus('Completed');
                    clearInterval(interval);
                    navigate(`/results/${jobId}`);
                } else if (data.status === 'failed') {
                    setStatus('Failed');
                    setError('An error occurred while extracting the blog.');
                    clearInterval(interval);
                }
            } catch (err) {
                setError('Error checking job status.');
                clearInterval(interval);
            }
        }, 2000);

        return () => clearInterval(interval);
    }, [jobId, navigate]);

    return (
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <h1>Progress Page</h1>
            {status !== 'Completed' && !error && (
                <div>
                    <CircularProgress />
                    <p>Status: {status}</p>
                </div>
            )}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default ProgressPage;