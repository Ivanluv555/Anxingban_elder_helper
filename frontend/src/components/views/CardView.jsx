import { useState } from 'react';
import { cardsAPI } from '../../api/client';
import { useToast } from '../Toast';

export function CardView({ onNavigate, tripId }) {
    const { showToast } = useToast();
    const [loading, setLoading] = useState(false);
    const [card, setCard] = useState(null);
    const [formData, setFormData] = useState({
        title: '旅行回忆卡片',
        image_url: '',
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!tripId) {
            showToast('请先创建行程', 'warn');
            return;
        }

        setLoading(true);
        try {
            const data = await cardsAPI.generate({
                trip_id: parseInt(tripId),
                title: formData.title,
                image_url: formData.image_url,
            });
            setCard(data);
            showToast('卡片生成成功', 'success');
        } catch (error) {
            showToast(`生成失败：${error.message}`, 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <>
            <section className="glass-panel view-head">
                <button type="button" className="back-btn" onClick={() => onNavigate('home')}>
                    ← 返回首页
                </button>
                <h2>回忆卡片</h2>
            </section>

            <section className="glass-panel module">
                <div className="module-head">
                    <span className="module-index">🖼</span>
                    <h2>生成回忆卡片</h2>
                </div>
                <p className="hint">
                    为您的旅行生成精美的回忆卡片，记录美好瞬间，分享给家人朋友。
                </p>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        name="title"
                        placeholder="卡片标题"
                        value={formData.title}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="text"
                        name="image_url"
                        placeholder="照片URL（选填）"
                        value={formData.image_url}
                        onChange={handleChange}
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? '生成中...' : '生成卡片'}
                    </button>
                </form>
                <p className="muted">
                    卡片将自动包含行程信息、完成的任务和旅行照片。
                </p>
            </section>

            {card && (
                <section className="glass-panel module">
                    <div className="module-head">
                        <span className="module-index">✓</span>
                        <h2>{card.title}</h2>
                    </div>
                    {card.image_url && (
                        <img
                            src={card.image_url}
                            alt={card.title}
                            style={{
                                width: '100%',
                                borderRadius: '12px',
                                marginBottom: '12px',
                            }}
                        />
                    )}
                    <div className="result-panel">{card.summary}</div>
                    <p className="muted">
                        卡片ID: {card.id} · 创建时间: {new Date(card.created_at).toLocaleString()}
                    </p>
                </section>
            )}
        </>
    );
}
