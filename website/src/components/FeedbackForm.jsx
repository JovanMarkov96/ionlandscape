import React, { useState } from 'react';

/**
 * FeedbackForm Component
 * 
 * A compact, inline button for users to report outdated or incorrect information.
 * It opens a new GitHub Issue pre-filled with the entity details.
 * 
 * @param {Object} props
 * @param {string} props.entityType - Type of entity (e.g., 'Person', 'Company', 'Institution')
 * @param {string} props.entityName - Name of the entity
 * @param {string} props.entityId - ID of the entity
 */
export default function FeedbackForm({ entityType, entityName, entityId }) {
    const [isHovered, setIsHovered] = useState(false);

    const handleFeedbackClick = () => {
        const title = encodeURIComponent(`Data Correction: ${entityName}`);
        const body = encodeURIComponent(`Please describe the issue or missing information for **${entityName}** (${entityType}, ID: \`${entityId}\`) below:\n\n`);
        const githubUrl = `https://github.com/JovanMarkov96/quantum-landscape/issues/new?title=${title}&body=${body}`;
        window.open(githubUrl, '_blank', 'noopener,noreferrer');
    };

    return (
        <div className="feedback-wrapper">
            <button
                className={`feedback-trigger-btn ${isHovered ? 'expanded' : ''}`}
                onClick={handleFeedbackClick}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                aria-label="Report Issue on GitHub"
            >
                <span className="feedback-icon" aria-label="flag">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"></path>
                        <line x1="4" y1="22" x2="4" y2="15"></line>
                    </svg>
                </span>
                <span className="feedback-text">Report an issue</span>
            </button>
        </div>
    );
}
