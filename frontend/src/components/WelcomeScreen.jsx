import { useState, useRef, useEffect } from 'react';

export function WelcomeScreen({ onEnter }) {
    const [currentOffset, setCurrentOffset] = useState(0);
    const [dragging, setDragging] = useState(false);
    const [unlocked, setUnlocked] = useState(false);
    const sliderTrackRef = useRef(null);
    const sliderThumbRef = useRef(null);
    const startXRef = useRef(0);
    const maxOffsetRef = useRef(0);

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        if (params.get('skipWelcome') === '1') {
            onEnter();
        }
    }, [onEnter]);

    useEffect(() => {
        const updateBounds = () => {
            if (sliderTrackRef.current && sliderThumbRef.current) {
                maxOffsetRef.current = Math.max(
                    0,
                    sliderTrackRef.current.clientWidth - sliderThumbRef.current.offsetWidth - 8
                );
            }
        };
        updateBounds();
        window.addEventListener('resize', updateBounds);
        return () => window.removeEventListener('resize', updateBounds);
    }, []);

    const handleStart = (clientX) => {
        setDragging(true);
        startXRef.current = clientX;
    };

    const handleMove = (clientX) => {
        if (!dragging) return;
        const delta = clientX - startXRef.current;
        const newOffset = Math.max(0, Math.min(delta, maxOffsetRef.current));
        setCurrentOffset(newOffset);

        if (newOffset >= maxOffsetRef.current * 0.85 && !unlocked) {
            setUnlocked(true);
            setTimeout(() => onEnter(), 100);
        }
    };

    const handleEnd = () => {
        if (!unlocked && currentOffset < maxOffsetRef.current * 0.85) {
            setCurrentOffset(0);
        }
        setDragging(false);
    };

    const ratio = maxOffsetRef.current > 0 ? currentOffset / maxOffsetRef.current : 0;
    const progressWidth = 56 + ratio * (sliderTrackRef.current?.clientWidth || 400) - 56;

    return (
        <section id="welcome-screen" aria-label="安行伴欢迎页">
            <div className="welcome-mask"></div>
            <div className="welcome-card">
                <p className="welcome-kicker">欢迎来到</p>
                <h2 className="welcome-title">安行伴</h2>
                <p className="welcome-subtitle">陪伴好他们的每场旅行</p>

                <div
                    ref={sliderTrackRef}
                    className="enter-slider"
                    id="enter-slider-track"
                    role="button"
                    aria-label="向右滑动进入应用"
                >
                    <div
                        className="enter-slider-progress"
                        style={{ width: `${progressWidth}px` }}
                    ></div>
                    <span
                        className="enter-slider-hint"
                        style={{ opacity: Math.max(0.12, 1 - ratio * 1.15) }}
                    >
                        {unlocked ? '欢迎回来' : '向右滑动进入'}
                    </span>
                    <button
                        ref={sliderThumbRef}
                        type="button"
                        className="enter-slider-thumb"
                        aria-label="向右滑动进入"
                        style={{ transform: `translateX(${currentOffset}px)` }}
                        onMouseDown={(e) => handleStart(e.clientX)}
                        onTouchStart={(e) => handleStart(e.touches[0].clientX)}
                    >
                        <span>→</span>
                    </button>
                </div>
            </div>
        </section>
    );
}

// Global mouse/touch handlers
if (typeof window !== 'undefined') {
    let globalDragging = false;
    let globalCallback = null;

    window.addEventListener('mousemove', (e) => {
        if (globalDragging && globalCallback) globalCallback(e.clientX);
    });

    window.addEventListener('mouseup', () => {
        if (globalDragging && globalCallback) {
            globalCallback = null;
            globalDragging = false;
        }
    });

    window.addEventListener('touchmove', (e) => {
        if (globalDragging && globalCallback && e.touches[0]) {
            globalCallback(e.touches[0].clientX);
        }
    });

    window.addEventListener('touchend', () => {
        if (globalDragging && globalCallback) {
            globalCallback = null;
            globalDragging = false;
        }
    });
}
