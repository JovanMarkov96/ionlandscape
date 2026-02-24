import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';

/**
 * FeedbackForm Component
 * 
 * A compact, inline form for users to report outdated or incorrect information.
 * Submits data directly to Formspree. Appears as a small hoverable button at the 
 * bottom-left of the profile card, which opens a centralized modal.
 * 
 * @param {Object} props
 * @param {string} props.entityType - Type of entity (e.g., 'Person', 'Company', 'Institution')
 * @param {string} props.entityName - Name of the entity
 * @param {string} props.entityId - ID of the entity
 */
export default function FeedbackForm({ entityType, entityName, entityId }) {
    const [isOpen, setIsOpen] = useState(false);
    const [status, setStatus] = useState(''); // '', 'submitting', 'success', 'error'
    const [isHovered, setIsHovered] = useState(false);

    // Prevent body scrolling when modal is open
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
        return () => {
            document.body.style.overflow = '';
        };
    }, [isOpen]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('submitting');

        const form = e.target;
        const data = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: data,
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (response.ok) {
                setStatus('success');
                form.reset();
                // Auto-close after 3 seconds
                setTimeout(() => {
                    setIsOpen(false);
                    setStatus('');
                }, 3000);
            } else {
                setStatus('error');
            }
        } catch (error) {
            console.error("Feedback submission error:", error);
            setStatus('error');
        }
    };

    return (
        <div className="feedback-wrapper">
            {/* Minimal floating button at bottom left of panel */}
            <button
                className={`feedback-trigger-btn ${isHovered ? 'expanded' : ''}`}
                onClick={() => setIsOpen(true)}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                aria-label="Report Issue"
            >
                <span className="feedback-icon" aria-label="flag">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"></path>
                        <line x1="4" y1="22" x2="4" y2="15"></line>
                    </svg>
                </span>
                <span className="feedback-text">Report an issue</span>
            </button>

            {/* Centralized Modal Overlay using Portal */}
            {isOpen && typeof document !== 'undefined' && createPortal(
                <div className="feedback-modal-overlay" onClick={() => setIsOpen(false)}>
                    <div className="feedback-modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="feedback-modal-header">
                            <h5>Report Issue with {entityName}</h5>
                            <button
                                className="feedback-close-btn"
                                onClick={() => setIsOpen(false)}
                                aria-label="Close form"
                            >
                                ✕
                            </button>
                        </div>

                        {status === 'success' ? (
                            <div className="feedback-success-message">
                                Thank you! Your feedback has been sent.
                            </div>
                        ) : (
                            <form
                                action="https://formspree.io/f/xzdakvdz"
                                method="POST"
                                onSubmit={handleSubmit}
                                className="feedback-form"
                            >
                                {/* Context Data (Hidden) */}
                                <input type="hidden" name="Entity Type" value={entityType} />
                                <input type="hidden" name="Entity Name" value={entityName} />
                                <input type="hidden" name="Entity ID" value={entityId || 'Unknown'} />

                                <div className="feedback-form-group">
                                    <label htmlFor="message">What is missing or incorrect?</label>
                                    <textarea
                                        id="message"
                                        name="message"
                                        required
                                        rows="4"
                                        placeholder="Please provide details..."
                                        disabled={status === 'submitting'}
                                    />
                                </div>

                                <div className="feedback-form-group">
                                    <label htmlFor="email">Your Email (Optional, for follow-up)</label>
                                    <input
                                        type="email"
                                        id="email"
                                        name="email"
                                        placeholder="you@email.com"
                                        disabled={status === 'submitting'}
                                    />
                                </div>

                                <div className="feedback-form-actions">
                                    <button
                                        type="button"
                                        className="btn-secondary"
                                        onClick={() => setIsOpen(false)}
                                        disabled={status === 'submitting'}
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        type="submit"
                                        className="btn-primary"
                                        disabled={status === 'submitting'}
                                    >
                                        {status === 'submitting' ? 'Sending...' : 'Submit'}
                                    </button>
                                </div>

                                {status === 'error' && (
                                    <div className="feedback-error-message">
                                        Oops! There was a problem sending your feedback. Please try again.
                                    </div>
                                )}
                            </form>
                        )}
                    </div>
                </div>,
                document.body
            )}
        </div>
    );
}
