import React from 'react';

interface DownloadButtonProps {
    fileName: string;
    data: string;
}

const DownloadButton: React.FC<DownloadButtonProps> = ({ fileName, data }) => {
    const handleDownload = () => {
        const blob = new Blob([data], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <button onClick={handleDownload}>
            Download {fileName}
        </button>
    );
};

export default DownloadButton;