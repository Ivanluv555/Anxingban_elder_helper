import { useNetworkStatus } from '../hooks/useNetworkStatus';

export function Header({ currentView, profileId, tripId, taskId }) {
    const isOnline = useNetworkStatus();

    const getViewTitle = () => {
        const titles = {
            home: '首页 · 重庆景区推荐',
            'scenic-list': '景区推荐 · 重庆',
            'scenic-hongyadong': '景区 · 洪崖洞夜景',
            'scenic-ciqikou': '景区 · 磁器口古镇',
            'scenic-wulong': '景区 · 武隆天生三桥',
            'scenic-cableway': '景区 · 长江索道',
            profile: '家庭建档',
            trip: '创建行程',
            sos: '紧急求助',
            task: '亲子任务',
            guide: '景点讲解',
            card: '回忆卡片',
        };
        return titles[currentView] || '首页 · 功能总览';
    };

    return (
        <header className="glass-panel topbar">
            <p className="kicker">安行伴</p>
            <h1>安行伴</h1>
            <p className="subtitle" id="current-view-label">{getViewTitle()}</p>
            <div className="status-row">
                <span className={`pill ${isOnline ? 'online' : 'offline'}`}>
                    网络状态：{isOnline ? '在线' : '离线'}
                </span>
            </div>
            <p className="context-meta">
                档案ID：{profileId || '-'} ｜ 行程ID：{tripId || '-'} ｜ 任务ID：{taskId || '-'}
            </p>
        </header>
    );
}
