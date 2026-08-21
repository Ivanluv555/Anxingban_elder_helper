import { useState } from 'react';
import { guideAPI } from '../../api/client';
import { useToast } from '../Toast';

export function GuideView({ onNavigate }) {
    const { showToast } = useToast();
    const [loading, setLoading] = useState(false);
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question.trim()) return;

        setLoading(true);
        try {
            const data = await guideAPI.ask(question);
            setAnswer(data);
            showToast('导游回答已生成', 'success');
        } catch (error) {
            showToast(`请求失败：${error.message}`, 'error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <section className="glass-panel view-head">
                <button type="button" className="back-btn" onClick={() => onNavigate('home')}>
                    ← 返回首页
                </button>
                <h2>景点讲解</h2>
            </section>

            <section className="glass-panel module">
                <div className="module-head">
                    <span className="module-index">🎧</span>
                    <h2>AI智能导游</h2>
                </div>
                <p className="hint">
                    输入您想了解的景点或问题，AI导游将为您提供详细的讲解和建议。
                </p>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="例如：洪崖洞有什么特色？"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        required
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? '查询中...' : '询问导游'}
                    </button>
                </form>
                <p className="muted">
                    AI导游基于{answer?.scope || '重庆市'}的景点知识库，为您提供专业解答。
                </p>
            </section>

            {answer && (
                <section className="glass-panel module">
                    <div className="module-head">
                        <span className="module-index">💬</span>
                        <h2>导游回答</h2>
                    </div>
                    <div className="result-panel">{answer.answer}</div>
                    <p className="muted">
                        置信度: {(answer.confidence * 100).toFixed(1)}% · 范围: {answer.scope}
                    </p>
                </section>
            )}
        </>
    );
}
