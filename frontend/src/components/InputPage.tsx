import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { postBlogUrl } from '../utils/extractor';

const InputPage: React.FC = () => {
    const [url, setUrl] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUrl(event.target.value);
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const data = await postBlogUrl(url);
            // Assume backend returns { job_id: "..." }
            navigate(`/progress/${data.job_id}`);
        } catch (err: any) {
            setError(err.message || 'Failed to start extraction.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Enter Blog URL</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="url"
                    value={url}
                    onChange={handleInputChange}
                    placeholder="https://example.com/blog"
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Starting...' : 'Start'}
                </button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default InputPage;