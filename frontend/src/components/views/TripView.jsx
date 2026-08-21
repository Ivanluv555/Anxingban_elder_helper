import { useState } from 'react';
import { tripsAPI } from '../../api/client';
import { useToast } from '../Toast';

export function TripView({ onNavigate, profileId, onTripCreated, presetDestination }) {
    const { showToast } = useToast();
    const [loading, setLoading] = useState(false);
    const [tripData, setTripData] = useState(null);
    const [formData, setFormData] = useState({
        profile_id: profileId || '',
        destination: presetDestination || '',
        travel_date: '',
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!formData.profile_id) {
            showToast('请先创建档案', 'warn');
            return;
        }

        setLoading(true);
        try {
            const trip = await tripsAPI.create({
                profile_id: parseInt(formData.profile_id),
                destination: formData.destination,
                travel_date: formData.travel_date,
            });
            setTripData(trip);
            onTripCreated(trip.id);
            showToast('行程创建成功', 'success');
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
                <h2>创建行程</h2>
            </section>

            <section className="glass-panel module">
                <div className="module-head">
                    <span className="module-index">1</span>
                    <h2>行程信息</h2>
                </div>
                <p className="hint">选择目的地和出行日期，系统将生成专属通行证。</p>
                <form onSubmit={handleSubmit}>
                    <input
                        type="number"
                        name="profile_id"
                        placeholder="档案ID *"
                        value={formData.profile_id}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="text"
                        name="destination"
                        placeholder="目的地 *"
                        value={formData.destination}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="date"
                        name="travel_date"
                        value={formData.travel_date}
                        onChange={handleChange}
                        required
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? '创建中...' : '创建行程'}
                    </button>
                </form>
            </section>

            {tripData && (
                <section className="glass-panel module">
                    <div className="module-head">
                        <span className="module-index">2</span>
                        <h2>通行证</h2>
                    </div>
                    <p className="hint">已生成专属通行证，可用于景区验证和紧急联系。</p>
                    <div className="result-panel">
                        <div>行程ID: {tripData.id}</div>
                        <div>目的地: {tripData.destination}</div>
                        <div>出行日期: {tripData.travel_date}</div>
                        <div>状态: {tripData.status}</div>
                    </div>
                    <div className="token">通行令牌: {tripData.pass_token}</div>
                    {tripData.pass_qr_svg && (
                        <div id="qr-box" dangerouslySetInnerHTML={{ __html: tripData.pass_qr_svg }}></div>
                    )}
                </section>
            )}
        </>
    );
}
