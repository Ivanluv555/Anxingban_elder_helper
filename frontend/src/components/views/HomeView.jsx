import { useState } from 'react';

const FEATURE_DEFS = [
    { label: '家庭建档', desc: '建立家庭成员档案', icon: '👤', view: 'profile' },
    { label: '创建行程', desc: '定制专属旅行计划', icon: '📅', view: 'trip' },
    { label: '紧急求助', desc: '一键联系紧急救助', icon: 'SOS', view: 'sos' },
    { label: '亲子任务', desc: '亲子互动趣味任务', icon: '👥', view: 'task' },
    { label: '景点讲解', desc: '智能语音景点介绍', icon: '🎧', view: 'guide' },
    { label: '回忆卡片', desc: '记录旅行美好瞬间', icon: '🖼', view: 'card' },
];

export function HomeView({ onNavigate }) {
    const [selectedIndex, setSelectedIndex] = useState(3);

    const handleRotate = (direction) => {
        setSelectedIndex((prev) => (prev + direction + FEATURE_DEFS.length) % FEATURE_DEFS.length);
    };

    const handleWheel = (e) => {
        e.preventDefault();
        if (Math.abs(e.deltaY) < 4) return;
        handleRotate(e.deltaY > 0 ? 1 : -1);
    };

    const renderOrbitItem = (slotIndex, totalSlots) => {
        const middleSlot = Math.floor(totalSlots / 2);
        const relative = slotIndex - middleSlot;
        const featureIndex = (selectedIndex + relative + FEATURE_DEFS.length) % FEATURE_DEFS.length;
        const feature = FEATURE_DEFS[featureIndex];
        const isActive = slotIndex === middleSlot;

        return (
            <button
                key={slotIndex}
                type="button"
                className={`orbit-item ${isActive ? 'active' : ''}`}
                data-slot={slotIndex}
                onClick={() => isActive && onNavigate(feature.view)}
                tabIndex={isActive ? 0 : -1}
                aria-disabled={!isActive}
            >
                <span className="orbit-text">
                    <span className="orbit-title">{feature.label}</span>
                    <span className="orbit-desc">{feature.desc}</span>
                </span>
                <span className="orbit-icon">{feature.icon}</span>
            </button>
        );
    };

    return (
        <section className="home-canvas home-selector-layout">
            <section className="semi-wheel-zone" aria-label="半圆功能选择器">
                <div
                    className="semi-wheel"
                    tabIndex={0}
                    aria-label="旋转半圆选择功能"
                    onWheel={handleWheel}
                    onKeyDown={(e) => {
                        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
                            e.preventDefault();
                            handleRotate(1);
                        } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
                            e.preventDefault();
                            handleRotate(-1);
                        } else if (e.key === 'Enter') {
                            e.preventDefault();
                            onNavigate(FEATURE_DEFS[selectedIndex].view);
                        }
                    }}
                ></div>
                <div className="selector-arc arc-outer" aria-hidden="true"></div>
                <div className="selector-arc arc-inner" aria-hidden="true"></div>

                <div className="feature-orbit" role="list" aria-label="功能选择" onWheel={handleWheel}>
                    {[0, 1, 2, 3, 4, 5].map((i) => renderOrbitItem(i, 6))}
                </div>

                <div className="scenic-tabs" aria-label="推荐分类">
                    <button type="button" className="scenic-tab active" onClick={() => onNavigate('scenic-list')}>
                        <span className="scenic-tab-icon">☾</span>
                        <span className="scenic-tab-label">夜景</span>
                    </button>
                    <button type="button" className="scenic-tab" onClick={() => onNavigate('scenic-list')}>
                        <span className="scenic-tab-icon">🏯</span>
                        <span className="scenic-tab-label">人文</span>
                    </button>
                    <button type="button" className="scenic-tab" onClick={() => onNavigate('scenic-list')}>
                        <span className="scenic-tab-icon">⛰</span>
                        <span className="scenic-tab-label">山水</span>
                    </button>
                    <button type="button" className="scenic-tab" onClick={() => onNavigate('scenic-list')}>
                        <span className="scenic-tab-icon">♡</span>
                        <span className="scenic-tab-label">亲子</span>
                    </button>
                </div>
            </section>
        </section>
    );
}
