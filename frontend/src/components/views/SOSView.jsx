import { useState } from 'react';
import { sosAPI } from '../../api/client';
import { useToast } from '../Toast';

export function SOSView({ onNavigate, profileId, tripId }) {
    const { showToast } = useToast();
    const [loading, setLoading] = useState(false);
    const [sosRecord, setSosRecord] = useState(null);
    const [location, setLocation] = useState({ latitude: null, longitude: null });

    const getLocation = () => {
        if (navigator.geolocation) {
            showToast('正在获取位置...', 'info', 1500);
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setLocation({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                    });
                    showToast('位置获取成功', 'success');
                },
                (error) => {
                    showToast(`位置获取失败：${error.message}`, 'warn');
                }
            );
        } else {
            showToast('浏览器不支持定位', 'warn');
        }
    };

    const handleTriggerSOS = async () => {
        if (!profileId) {
            showToast('请先创建档案', 'warn');
            return;
        }

        setLoading(true);
        try {
            const data = await sosAPI.trigger({
                profile_id: parseInt(profileId),
                trip_id: tripId ? parseInt(tripId) : null,
                latitude: location.latitude,
                longitude: location.longitude,
                network_status: navigator.onLine ? 'online' : 'offline',
            });
            setSosRecord(data);
            showToast('紧急求助已发送', 'success');
        } catch (error) {
            showToast(`求助失败：${error.message}`, 'error');
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
                <h2>紧急求助</h2>
            </section>

            <section className="glass-panel module">
                <div className="module-head">
                    <span className="module-index">SOS</span>
                    <h2>一键求助</h2>
                </div>
                <p className="hint">
                    点击按钮后，系统将立即通过短信和微信通知紧急联系人，并发送当前位置信息。
                </p>
                <button type="button" className="secondary" onClick={getLocation} disabled={loading}>
                    获取当前位置
                </button>
                {location.latitude && location.longitude && (
                    <div className="result-panel">
                        <div>纬度: {location.latitude.toFixed(6)}</div>
                        <div>经度: {location.longitude.toFixed(6)}</div>
                    </div>
                )}
                <button type="button" className="danger" onClick={handleTriggerSOS} disabled={loading}>
                    {loading ? '发送中...' : '触发紧急求助'}
                </button>
                <p className="muted">
                    紧急求助功能将通知您的家人和相关服务机构。请仅在真正需要时使用。
                </p>
            </section>

            {sosRecord && (
                <section className="glass-panel module">
                    <div className="module-head">
                        <span className="module-index">✓</span>
                        <h2>求助记录</h2>
                    </div>
                    <div className="result-panel">
                        <div>记录ID: {sosRecord.id}</div>
                        <div>短信状态: {sosRecord.sms_status}</div>
                        <div>微信状态: {sosRecord.wechat_status}</div>
                        <div>网络状态: {sosRecord.network_status}</div>
                        <div>创建时间: {new Date(sosRecord.created_at).toLocaleString()}</div>
                    </div>
                </section>
            )}
        </>
    );
}
