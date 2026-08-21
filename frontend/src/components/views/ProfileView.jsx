import { useState } from 'react';
import { profilesAPI } from '../../api/client';
import { useToast } from '../Toast';

export function ProfileView({ onNavigate, onProfileCreated }) {
    const { showToast } = useToast();
    const [profiles, setProfiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        parent_name: '',
        parent_phone: '',
        child_name: '',
        child_phone: '',
        chronic_diseases: '',
        allergies: '',
        mobility_limitations: '',
        interests: 'culture,food',
        wechat_webhook_url: '',
    });

    const loadProfiles = async () => {
        setLoading(true);
        try {
            const data = await profilesAPI.list(20);
            setProfiles(data);
            showToast('档案列表已刷新', 'success');
        } catch (error) {
            showToast(`加载失败：${error.message}`, 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const profile = await profilesAPI.create(formData);
            showToast('档案创建成功', 'success');
            onProfileCreated(profile.id);
            setProfiles([profile, ...profiles]);
            setFormData({
                parent_name: '',
                parent_phone: '',
                child_name: '',
                child_phone: '',
                chronic_diseases: '',
                allergies: '',
                mobility_limitations: '',
                interests: 'culture,food',
                wechat_webhook_url: '',
            });
        } catch (error) {
            showToast(`创建失败：${error.message}`, 'error');
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
                <h2>家庭建档</h2>
            </section>

            <section className="glass-panel module">
                <div className="module-head">
                    <span className="module-index">1</span>
                    <h2>新建档案</h2>
                </div>
                <p className="hint">填写家庭成员信息，便于紧急联系和个性化服务。</p>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        name="parent_name"
                        placeholder="长辈姓名 *"
                        value={formData.parent_name}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="tel"
                        name="parent_phone"
                        placeholder="长辈手机号 *"
                        value={formData.parent_phone}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="text"
                        name="child_name"
                        placeholder="子女姓名 *"
                        value={formData.child_name}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="tel"
                        name="child_phone"
                        placeholder="子女手机号 *"
                        value={formData.child_phone}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="text"
                        name="chronic_diseases"
                        placeholder="慢性疾病（选填）"
                        value={formData.chronic_diseases}
                        onChange={handleChange}
                    />
                    <input
                        type="text"
                        name="allergies"
                        placeholder="过敏史（选填）"
                        value={formData.allergies}
                        onChange={handleChange}
                    />
                    <input
                        type="text"
                        name="mobility_limitations"
                        placeholder="行动限制（选填）"
                        value={formData.mobility_limitations}
                        onChange={handleChange}
                    />
                    <input
                        type="text"
                        name="interests"
                        placeholder="兴趣偏好（如：文化,美食）"
                        value={formData.interests}
                        onChange={handleChange}
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? '创建中...' : '创建档案'}
                    </button>
                </form>
            </section>

            <section className="glass-panel module">
                <div className="module-head">
                    <span className="module-index">2</span>
                    <h2>已有档案</h2>
                </div>
                <button type="button" onClick={loadProfiles} disabled={loading}>
                    {loading ? '加载中...' : '刷新档案列表'}
                </button>
                {profiles.length > 0 && (
                    <ul className="profiles-list">
                        {profiles.map((profile) => (
                            <li key={profile.id}>
                                <div className="title">
                                    {profile.parent_name} & {profile.child_name}
                                </div>
                                <div className="meta">
                                    ID: {profile.id} · {profile.parent_phone} / {profile.child_phone}
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
                {profiles.length === 0 && <p className="hint">暂无档案，请先创建。</p>}
            </section>
        </>
    );
}
