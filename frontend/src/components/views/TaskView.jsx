import { useState } from 'react';
import { tasksAPI } from '../../api/client';
import { useToast } from '../Toast';

export function TaskView({ onNavigate, profileId, tripId, onTaskCreated }) {
    const { showToast } = useToast();
    const [loading, setLoading] = useState(false);
    const [tasks, setTasks] = useState([]);
    const [formData, setFormData] = useState({
        title: '',
        description: '',
    });

    const loadTasks = async () => {
        if (!profileId) {
            showToast('请先创建档案', 'warn');
            return;
        }
        setLoading(true);
        try {
            const data = await tasksAPI.listByProfile(parseInt(profileId));
            setTasks(data);
            showToast('任务列表已刷新', 'success');
        } catch (error) {
            showToast(`加载失败：${error.message}`, 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!profileId || !tripId) {
            showToast('请先创建档案和行程', 'warn');
            return;
        }

        setLoading(true);
        try {
            const task = await tasksAPI.create({
                profile_id: parseInt(profileId),
                trip_id: parseInt(tripId),
                title: formData.title,
                description: formData.description,
            });
            setTasks([task, ...tasks]);
            onTaskCreated(task.id);
            showToast('任务创建成功', 'success');
            setFormData({ title: '', description: '' });
        } catch (error) {
            showToast(`创建失败：${error.message}`, 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleComplete = async (taskId) => {
        setLoading(true);
        try {
            const task = await tasksAPI.complete(taskId, {
                completed_note: '任务已完成',
                photo_url: '',
            });
            setTasks(tasks.map((t) => (t.id === taskId ? task : t)));
            showToast('任务已完成', 'success');
        } catch (error) {
            showToast(`操作失败：${error.message}`, 'error');
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
                <h2>亲子任务</h2>
            </section>

            <section className="glass-panel module">
                <div className="module-head">
                    <span className="module-index">1</span>
                    <h2>创建任务</h2>
                </div>
                <p className="hint">设置亲子互动任务，增进旅途中的家庭情感交流。</p>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        name="title"
                        placeholder="任务标题 *"
                        value={formData.title}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="text"
                        name="description"
                        placeholder="任务描述 *"
                        value={formData.description}
                        onChange={handleChange}
                        required
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? '创建中...' : '创建任务'}
                    </button>
                </form>
            </section>

            <section className="glass-panel module">
                <div className="module-head">
                    <span className="module-index">2</span>
                    <h2>任务列表</h2>
                </div>
                <button type="button" className="secondary" onClick={loadTasks} disabled={loading}>
                    {loading ? '加载中...' : '刷新任务列表'}
                </button>
                {tasks.length > 0 && (
                    <ul className="profiles-list">
                        {tasks.map((task) => (
                            <li key={task.id}>
                                <div className="title">{task.title}</div>
                                <div className="meta">
                                    {task.description} · 状态: {task.status} · ❤ {task.hearts}
                                </div>
                                {task.status === 'pending' && (
                                    <button
                                        type="button"
                                        onClick={() => handleComplete(task.id)}
                                        disabled={loading}
                                        style={{ marginTop: '8px' }}
                                    >
                                        完成任务
                                    </button>
                                )}
                            </li>
                        ))}
                    </ul>
                )}
                {tasks.length === 0 && <p className="hint">暂无任务，请先创建。</p>}
            </section>
        </>
    );
}
