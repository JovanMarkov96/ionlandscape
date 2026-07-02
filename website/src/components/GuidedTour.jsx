import React, { useState, useEffect, useCallback, useRef } from 'react';
import ReactDOM from 'react-dom';

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
    const [rect, setRect] = useState(null);        // spotlight rect (union of target(s))
    const [anchorRect, setAnchorRect] = useState(null); // optional element to position the tip beside
    const [vp, setVp] = useState({ w: 1200, h: 800 });
    const tipRef = useRef(null);

    // Reset to the first step whenever the tour (re)opens.
    useEffect(() => { if (open) setI(0); }, [open]);

    const step = steps[i];

    const measure = useCallback(() => {
        setVp({ w: window.innerWidth, h: window.innerHeight });
        if (!step) { setRect(null); setAnchorRect(null); return; }
        // Spotlight target(s): union of one or many elements.
        const sels = step.selectors || (step.selector ? [step.selector] : []);
        let u = null;
        sels.forEach(s => {
            const el = document.querySelector(s);
            if (!el) return;
            const r = el.getBoundingClientRect();
            if (r.width === 0 && r.height === 0) return;
            u = u
                ? { top: Math.min(u.top, r.top), left: Math.min(u.left, r.left), right: Math.max(u.right, r.right), bottom: Math.max(u.bottom, r.bottom) }
                : { top: r.top, left: r.left, right: r.right, bottom: r.bottom };
        });
        setRect(u ? { top: u.top, left: u.left, width: u.right - u.left, height: u.bottom - u.top } : null);
        // Optional separate anchor for the coachmark (keeps the tip clear of the target).
        let a = null;
        if (step.anchor) {
            const el = document.querySelector(step.anchor);
            if (el) {
                const r = el.getBoundingClientRect();
                if (r.width || r.height) a = { top: r.top, left: r.left, width: r.width, height: r.height, right: r.right };
            }
        }
        setAnchorRect(a);
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

    const finish = useCallback(() => { onClose && onClose(); }, [onClose]);
    // Side effects (finish → parent setState/localStorage) must stay outside
    // the setI updater: React updaters are pure and StrictMode double-invokes them.
    const next = useCallback(() => {
        if (i < steps.length - 1) setI(i + 1);
        else finish();
    }, [i, steps.length, finish]);

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
    }, [open, finish, next]);

    if (!open || !step || typeof document === 'undefined') return null;

    const PAD = 8;
    const spot = rect && {
        top: rect.top - PAD,
        left: rect.left - PAD,
        width: rect.width + PAD * 2,
        height: rect.height + PAD * 2,
    };

    // ---- Coachmark position ----
    const isWelcome = !!step.brand;
    // Clamp the card to the viewport so it never spills off a narrow phone screen.
    const TIP_W = Math.min(isWelcome ? 430 : 330, vp.w - 32);
    const tipH = (tipRef.current && tipRef.current.offsetHeight) || 190;
    // Cursor follows the spotlight target; the coachmark may be anchored elsewhere.
    let cursor = rect
        ? { left: rect.left + rect.width / 2, top: rect.top + rect.height / 2 }
        : { left: vp.w / 2, top: vp.h / 2 };
    const posRect = anchorRect || rect;
    let tipStyle;
    if (!posRect) {
        // Centre horizontally with a pixel left (not translateX) so a mobile
        // `left` override can't fight an inline transform and push us off-screen.
        tipStyle = { top: '50%', left: Math.max(16, (vp.w - TIP_W) / 2), transform: 'translateY(-50%)', width: TIP_W };
    } else {
        const placement = step.placement || 'auto';
        const rightOk = posRect.left + posRect.width + TIP_W + 24 < vp.w;
        const spaceBelow = vp.h - (posRect.top + posRect.height);
        let top, left;
        if (placement === 'right' && rightOk) {
            top = posRect.top; left = posRect.left + posRect.width + 18;
        } else if (placement === 'bottom' || (placement === 'auto' && spaceBelow > tipH + 24)) {
            top = posRect.top + posRect.height + 18; left = posRect.left + posRect.width / 2 - TIP_W / 2;
        } else {
            top = posRect.top - tipH - 18; left = posRect.left + posRect.width / 2 - TIP_W / 2;
        }
        left = Math.max(16, Math.min(left, vp.w - TIP_W - 16));
        top = Math.max(16, Math.min(top, vp.h - tipH - 16));
        tipStyle = { top, left, width: TIP_W };
    }

    const isLast = i === steps.length - 1;

    return ReactDOM.createPortal((
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
            <div className={`tour-tip${isWelcome ? ' tour-tip--welcome' : ''}`} ref={tipRef} style={tipStyle}>
                {isWelcome ? (
                    <div className="tour-brand">
                        <img className="ql-stacked ql-stacked-dark" src="/quantum-landscape/img/brand/wordmark-stacked-on-dark.png" alt="Quantum Landscape" />
                        <img className="ql-stacked ql-stacked-light" src="/quantum-landscape/img/brand/wordmark-stacked-on-light.png" alt="Quantum Landscape" />
                    </div>
                ) : (
                    <div className="tour-tip-step">Step {i + 1} of {steps.length}</div>
                )}
                <h3>{step.title}</h3>
                <p>{step.body}</p>
                <div className="tour-tip-actions">
                    <button className="tour-skip" onClick={finish}>{isWelcome ? 'Skip' : (isLast ? 'Close' : 'Skip tour')}</button>
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
    ), document.body);
}
