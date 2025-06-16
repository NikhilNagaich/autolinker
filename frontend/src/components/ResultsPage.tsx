import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchResults } from '../utils/extractor';
import DownloadButton from './common/DownloadButton';
import CircularProgress from '@mui/material/CircularProgress';

const ResultsPage: React.FC = () => {
    const { jobId } = useParams<{ jobId: string }>();
    const [results, setResults] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<string>('In Progress');

    useEffect(() => {
        if (!jobId) return;
        fetchResults(jobId)
            .then(data => {
                setResults(data);
                setLoading(false);
                setStatus('Completed');
            })
            .catch(err => {
                setError('Failed to fetch results.');
                setLoading(false);
                setStatus('Error');
            });
    }, [jobId]);

    if (loading) return <div>Loading results...</div>;
    if (error) return <div style={{ color: 'red' }}>{error}</div>;
    if (!results || !results.anchor_suggestions) return <div>No anchor suggestions found.</div>;

    // Group anchor suggestions by target_link
    const grouped = results.anchor_suggestions.reduce((acc: any, suggestion: any) => {
        if (!acc[suggestion.target_link]) acc[suggestion.target_link] = [];
        acc[suggestion.target_link].push(suggestion);
        return acc;
    }, {});

    return (
        <div>
            <h1>Progress Page</h1>
            {status !== 'Completed' && <CircularProgress />}
            <p>Status: {status}</p>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {status === 'Completed' && (
                <>
                    <h1>Anchor Suggestions</h1>
                    {Object.entries(grouped).map(([targetLink, suggestions], idx) => (
                        <div key={targetLink} style={{ marginBottom: '2em' }}>
                            <strong>Target Link:</strong> <a href={targetLink} target="_blank" rel="noopener noreferrer">{targetLink}</a>
                            <ul>
                                {(suggestions as any[]).map((suggestion, i) => (
                                    <li key={i}>
                                        <strong>Anchor Text:</strong> {suggestion.anchor_text}<br />
                                        <strong>Anchor Sentence:</strong> {suggestion.anchor_sentence}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                    <DownloadButton fileName="anchor_suggestions.json" data={JSON.stringify(results.anchor_suggestions, null, 2)} />
                </>
            )}
        </div>
    );
};

export default ResultsPage;