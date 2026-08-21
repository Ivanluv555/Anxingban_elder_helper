import { useState, useEffect } from 'react';
import './App.css';
import { ToastProvider } from './components/Toast';
import { WelcomeScreen } from './components/WelcomeScreen';
import { LiquidOrbs } from './components/LiquidOrbs';
import { CornerRibbon } from './components/CornerRibbon';
import { Header } from './components/Header';
import { HomeView } from './components/views/HomeView';
import { ProfileView } from './components/views/ProfileView';
import { TripView } from './components/views/TripView';
import { SOSView } from './components/views/SOSView';
import { TaskView } from './components/views/TaskView';
import { GuideView } from './components/views/GuideView';
import { CardView } from './components/views/CardView';
import { ScenicListView, ScenicDetailView } from './components/views/ScenicViews';

function App() {
    const [appEntered, setAppEntered] = useState(false);
    const [currentView, setCurrentView] = useState('home');
    const [profileId, setProfileId] = useState(null);
    const [tripId, setTripId] = useState(null);
    const [taskId, setTaskId] = useState(null);
    const [presetDestination, setPresetDestination] = useState('');

    useEffect(() => {
        const hash = window.location.hash.replace('#', '');
        if (hash && appEntered) {
            setCurrentView(hash);
        }
    }, [appEntered]);

    useEffect(() => {
        if (appEntered) {
            const bodyClasses = document.body.classList;
            bodyClasses.remove('view-home-active', 'view-sub-active');
            if (currentView === 'home') {
                bodyClasses.add('view-home-active');
            } else {
                bodyClasses.add('view-sub-active');
            }

            const hash = currentView === 'home' ? '' : `#${currentView}`;
            window.history.pushState(null, '', `${window.location.pathname}${hash}`);
        }
    }, [currentView, appEntered]);

    useEffect(() => {
        if (appEntered) {
            document.body.classList.add('app-entered');
        }
    }, [appEntered]);

    const handleNavigate = (view) => {
        setCurrentView(view);
    };

    const handleAddToTrip = (destination) => {
        setPresetDestination(destination);
    };

    const renderView = () => {
        switch (currentView) {
            case 'home':
                return <HomeView onNavigate={handleNavigate} />;
            case 'profile':
                return <ProfileView onNavigate={handleNavigate} onProfileCreated={setProfileId} />;
            case 'trip':
                return (
                    <TripView
                        onNavigate={handleNavigate}
                        profileId={profileId}
                        onTripCreated={setTripId}
                        presetDestination={presetDestination}
                    />
                );
            case 'sos':
                return <SOSView onNavigate={handleNavigate} profileId={profileId} tripId={tripId} />;
            case 'task':
                return (
                    <TaskView
                        onNavigate={handleNavigate}
                        profileId={profileId}
                        tripId={tripId}
                        onTaskCreated={setTaskId}
                    />
                );
            case 'guide':
                return <GuideView onNavigate={handleNavigate} />;
            case 'card':
                return <CardView onNavigate={handleNavigate} tripId={tripId} />;
            case 'scenic-list':
                return <ScenicListView onNavigate={handleNavigate} />;
            case 'scenic-hongyadong':
            case 'scenic-ciqikou':
            case 'scenic-wulong':
            case 'scenic-cableway':
                return (
                    <ScenicDetailView
                        scenic={currentView}
                        onNavigate={handleNavigate}
                        onAddToTrip={handleAddToTrip}
                    />
                );
            default:
                return <HomeView onNavigate={handleNavigate} />;
        }
    };

    const dockItems = [
        { view: 'profile', label: '建档' },
        { view: 'trip', label: '行程' },
        { view: 'sos', label: 'SOS' },
        { view: 'task', label: '任务' },
        { view: 'guide', label: '导游' },
        { view: 'card', label: '卡片' },
    ];

    return (
        <ToastProvider>
            <LiquidOrbs />
            <CornerRibbon appEntered={appEntered} />

            {!appEntered && <WelcomeScreen onEnter={() => setAppEntered(true)} />}

            <div className="device-shell">
                <Header
                    currentView={currentView}
                    profileId={profileId}
                    tripId={tripId}
                    taskId={taskId}
                />

                <main className="app-views" id="app-views">
                    <section className={`view ${currentView === 'home' ? 'active' : ''}`} id="view-home">
                        {currentView === 'home' && renderView()}
                    </section>
                    <section className={`view ${currentView !== 'home' ? 'active' : ''}`}>
                        {currentView !== 'home' && renderView()}
                    </section>
                </main>

                {currentView !== 'home' && (
                    <div className="bottom-dock glass-panel">
                        {dockItems.map((item) => (
                            <button
                                key={item.view}
                                type="button"
                                className={`dock-item ${currentView === item.view ? 'active' : ''}`}
                                onClick={() => handleNavigate(item.view)}
                            >
                                {item.label}
                            </button>
                        ))}
                    </div>
                )}
            </div>
        </ToastProvider>
    );
}

export default App;
