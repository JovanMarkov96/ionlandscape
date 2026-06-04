import React, { useState, useEffect, useCallback, useRef } from 'react';

/**
 * GuidedTour — a lightweight, dependency-free interactive product tour.
 *
 * Renders a dimming spotlight over each target element, a coachmark card with
 * copy + navigation, and an animated cursor that glides to the highlighted
 * element. Fully theme-aware (inherits the app's liquid-glass styling) and
 * skippable at any step.
 *
 * Props:
 *   open     {boolean}  controlled visibility
 *   steps    {Array}    [{ selector|null, title, body, placement, cta }]
 *   onClose  {Function} called when finished or skipped
 *
 * A step with `selector: null` (or an element that can't be found) renders a
 * centered card with a full backdrop — used for the welcome / wrap-up steps.
 */
export default function GuidedTour({ open, steps, onClose }) {
    const [i, setI] = useState(0);
    const [rect, setRect] = useState(null);
    const [vp, setVp] = useState({ w: 1200, h: 800 });
    const tipRef = useRef(null);

    // Reset to the first step whenever the tour (re)opens.
    useEffect(() => { if (open) setI(0); }, [open]);

    const step = steps[i];

    const measure = useCallback(() => {
        setVp({ w: window.innerWidth, h: window.innerHeight });
        if (!step || !step.selector) { setRect(null); return; }
        const el = document.querySelector(step.selector);
        if (el) {
            const r = el.getBoundingClientRect();
            if (r.width === 0 && r.height === 0) { setRect(null); return; }
            setRect({ top: r.top, left: r.left, width: r.width, height: r.height });
        } else {
            setRect(null);
        }
    }, [step]);

    useEffect(() => {
        if (!open) return;
        measure();
        // Re-measure shortly after: map markers / panels may mount asynchronously.
        const t1 = setTimeout(measure, 250);
        const t2 = setTimeout(measure, 700);
        window.addEventListener('resize', measure);
        window.addEventListener('scroll', measure, true);
        return () => {
            clearTimeout(t1); clearTimeout(t2);
            window.removeEventListener('resize', measure);
            window.removeEventListener('scroll', measure, true);
        };
    }, [open, i, measure]);

    // Keyboard: Esc to skip, arrows / Enter to navigate.
    useEffect(() => {
        if (!open) return;
        const onKey = (e) => {
            if (e.key === 'Escape') finish();
            else if (e.key === 'ArrowRight' || e.key === 'Enter') next();
            else if (e.key === 'ArrowLeft') setI(p => Math.max(0, p - 1));
        };
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
    });

    const finish = () => { onClose && onClose(); };
    const next = () => { setI(p => (p < steps.length - 1 ? p + 1 : (finish(), p))); };

    if (!open || !step) return null;

    const PAD = 8;
    const spot = rect && {
        top: rect.top - PAD,
        left: rect.left - PAD,
        width: rect.width + PAD * 2,
        height: rect.height + PAD * 2,
    };

    // ---- Coachmark position ----
    const TIP_W = 330;
    const tipH = (tipRef.current && tipRef.current.offsetHeight) || 190;
    let tipStyle;
    let cursor = { left: vp.w / 2, top: vp.h / 2 };
    if (!rect) {
        tipStyle = { top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: TIP_W };
    } else {
        cursor = { left: rect.left + rect.width / 2, top: rect.top + rect.height / 2 };
        const placement = step.placement || 'auto';
        const spaceBelow = vp.h - (rect.top + rect.height);
        const below = placement === 'bottom' || (placement === 'auto' && spaceBelow > tipH + 24) || placement === 'right';
        let top, left;
        if (placement === 'right' && rect.right + TIP_W + 24 < vp.w) {
            top = rect.top; left = rect.left + rect.width + 18;
        } else if (below) {
            top = rect.top + rect.height + 18; left = rect.left + rect.width / 2 - TIP_W / 2;
        } else {
            top = rect.top - tipH - 18; left = rect.left + rect.width / 2 - TIP_W / 2;
        }
        left = Math.max(16, Math.min(left, vp.w - TIP_W - 16));
        top = Math.max(16, Math.min(top, vp.h - tipH - 16));
        tipStyle = { top, left, width: TIP_W };
    }

    const isLast = i === steps.length - 1;

    return (
        <div className="tour-root" role="dialog" aria-modal="true" aria-label="Guided tour">
            {/* Spotlight (or full backdrop for centered steps) */}
            {spot ? (
                <div className="tour-spotlight" style={spot} onClick={next} />
            ) : (
                <div className="tour-backdrop" onClick={next} />
            )}

            {/* Animated cursor */}
            <div className="tour-cursor" style={{ left: cursor.left, top: cursor.top }} aria-hidden="true">
                <svg viewBox="0 0 24 24" width="26" height="26">
                    <path d="M5 3l15 9-6.5 1.5L11 21 5 3z" fill="#fff" stroke="#1c1e26" strokeWidth="1.4" strokeLinejoin="round" />
                </svg>
            </div>

            {/* Coachmark */}
            <div className="tour-tip" ref={tipRef} style={tipStyle}>
                <div className="tour-tip-step">Step {i + 1} of {steps.length}</div>
                <h3>{step.title}</h3>
                <p>{step.body}</p>
                <div className="tour-tip-actions">
                    <button className="tour-skip" onClick={finish}>{isLast ? 'Close' : 'Skip tour'}</button>
                    <div className="tour-nav">
                        {i > 0 && <button className="tour-back" onClick={() => setI(p => Math.max(0, p - 1))}>Back</button>}
                        <button className="tour-next" onClick={next}>{step.cta || (isLast ? 'Done' : 'Next')}</button>
                    </div>
                </div>
                <div className="tour-dots">
                    {steps.map((_, k) => <span key={k} className={k === i ? 'on' : ''} />)}
                </div>
            </div>
        </div>
    );
}
