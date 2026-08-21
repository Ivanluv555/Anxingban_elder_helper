export function ScenicListView({ onNavigate }) {
    return (
        <>
            <section className="glass-panel view-head">
                <button type="button" className="back-btn" onClick={() => onNavigate('home')}>
                    ← 返回首页
                </button>
                <h2>景区推荐</h2>
            </section>
            <section className="glass-panel module">
                <p className="hint">点击任意景区帖子可查看详情，并可一键加入行程。</p>
                <section className="scenic-grid" aria-label="重庆景区推荐">
                    <button
                        type="button"
                        className="scenic-card scenic-hongyadong"
                        onClick={() => onNavigate('scenic-hongyadong')}
                    >
                        <span className="scenic-fav">☆</span>
                        <span className="scenic-region">渝中区</span>
                        <span className="scenic-name">洪崖洞夜景</span>
                    </button>

                    <button
                        type="button"
                        className="scenic-card scenic-ciqikou"
                        onClick={() => onNavigate('scenic-ciqikou')}
                    >
                        <span className="scenic-fav">☆</span>
                        <span className="scenic-region">沙坪坝区</span>
                        <span className="scenic-name">磁器口古镇</span>
                    </button>

                    <button
                        type="button"
                        className="scenic-card scenic-wulong"
                        onClick={() => onNavigate('scenic-wulong')}
                    >
                        <span className="scenic-fav">☆</span>
                        <span className="scenic-region">武隆区</span>
                        <span className="scenic-name">武隆天生三桥</span>
                    </button>

                    <button
                        type="button"
                        className="scenic-card scenic-cableway"
                        onClick={() => onNavigate('scenic-cableway')}
                    >
                        <span className="scenic-fav">☆</span>
                        <span className="scenic-region">南岸区</span>
                        <span className="scenic-name">长江索道</span>
                    </button>
                </section>
            </section>
        </>
    );
}

export function ScenicDetailView({ scenic, onNavigate, onAddToTrip }) {
    const scenicData = {
        'scenic-hongyadong': {
            title: '洪崖洞夜景',
            image: '/poster/hongyadong.jpg',
            location: '渝中区 · 建议游玩 1.5-2 小时',
            description: '洪崖洞依山就势而建，夜幕亮灯后层层吊脚楼会倒映在嘉陵江边，适合长辈边走边看。建议从上层步行慢慢下行，减少反复爬坡。',
            tips: [
                '19:00 后灯光层次更好，拍照效果更稳定。',
                '周末人流较大，建议错峰到访并提前约定集合点。',
                '可结合千厮门大桥步行道，安排轻量散步路线。',
            ],
            destination: '洪崖洞',
        },
        'scenic-ciqikou': {
            title: '磁器口古镇',
            image: '/poster/ciqikou.jpg',
            location: '沙坪坝区 · 建议游玩 2-3 小时',
            description: '磁器口古镇保留了明清时期的建筑风格，街道两旁小吃店铺林立。适合长辈体验传统文化，品尝重庆小吃。',
            tips: [
                '建议避开节假日高峰期，工作日游览体验更佳。',
                '古镇内道路较窄，注意人流密集时的安全。',
                '可以品尝陈麻花、毛血旺等当地特色美食。',
            ],
            destination: '磁器口古镇',
        },
        'scenic-wulong': {
            title: '武隆天生三桥',
            image: '/poster/wulong.jpg',
            location: '武隆区 · 建议游玩 3-4 小时',
            description: '武隆天生三桥是世界最大的天生桥群，自然风光壮丽。景区内有观光电梯，减轻爬山负担，适合长辈游览。',
            tips: [
                '景区较大，建议穿着舒适的运动鞋。',
                '可选择乘坐观光车节省体力。',
                '春秋季节气候宜人，是最佳游览时间。',
            ],
            destination: '武隆天生三桥',
        },
        'scenic-cableway': {
            title: '长江索道',
            image: '/poster/changjiangsuodao.jpg',
            location: '南岸区 · 建议游玩 0.5-1 小时',
            description: '长江索道是重庆的标志性交通工具，横跨长江，可以俯瞰两江四岸的美景。单程约5分钟，适合长辈体验。',
            tips: [
                '建议提前在线购票，避免现场排队。',
                '早上或傍晚人流较少，景色也更美。',
                '乘坐时注意安全，听从工作人员指引。',
            ],
            destination: '长江索道',
        },
    };

    const data = scenicData[scenic] || scenicData['scenic-hongyadong'];

    return (
        <>
            <section className="glass-panel view-head">
                <button type="button" className="back-btn" onClick={() => onNavigate('scenic-list')}>
                    ← 返回推荐
                </button>
                <h2>{data.title}</h2>
            </section>
            <section className="glass-panel module scenic-detail">
                <img className="scenic-detail-image" src={data.image} alt={`${data.title}照片`} />
                <p className="scenic-detail-location">{data.location}</p>
                <p className="scenic-detail-text">{data.description}</p>
                <ul className="scenic-detail-list">
                    {data.tips.map((tip, i) => (
                        <li key={i}>{tip}</li>
                    ))}
                </ul>
                <button
                    type="button"
                    className="scenic-plan-btn"
                    onClick={() => {
                        onAddToTrip(data.destination);
                        onNavigate('trip');
                    }}
                >
                    加入行程
                </button>
            </section>
        </>
    );
}
