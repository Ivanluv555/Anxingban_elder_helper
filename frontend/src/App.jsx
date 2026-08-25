import { useState, useEffect } from 'react';
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

    useEffect(() => {
        if (appEntered) {
            document.body.classList.add('app-entered');
            if (currentView === 'home') {
                document.body.classList.add('view-home-active');
                document.body.classList.remove('view-sub-active');
            } else {
                document.body.classList.add('view-sub-active');
                document.body.classList.remove('view-home-active');
            }
        }
    }, [appEntered, currentView]);

    const handleNavigate = (view) => setCurrentView(view);

    const renderView = () => {
        const props = { onNavigate: handleNavigate, profileId, tripId, taskId };
        switch (currentView) {
            case 'home':
                return <HomeView {...props} />;
            case 'profile':
                return <ProfileView {...props} onProfileCreated={setProfileId} />;
            case 'trip':
                return <TripView {...props} onTripCreated={setTripId} />;
            case 'sos':
                return <SOSView {...props} />;
            case 'task':
                return <TaskView {...props} onTaskCreated={setTaskId} />;
            case 'guide':
                return <GuideView {...props} />;
            case 'card':
                return <CardView {...props} />;
            case 'scenic-list':
                return <ScenicListView {...props} />;
            case 'scenic-hongyadong':
            case 'scenic-ciqikou':
            case 'scenic-wulong':
            case 'scenic-cableway':
                return <ScenicDetailView {...props} scenic={currentView} />;
            default:
                return <HomeView {...props} />;
        }
    };

    return (
        <ToastProvider>
            {!appEntered && <WelcomeScreen onEnter={() => setAppEntered(true)} />}
            <LiquidOrbs />
            <CornerRibbon />
            <div className="device-shell">
                <Header currentView={currentView} profileId={profileId} tripId={tripId} taskId={taskId} />
                <main className="app-views">{renderView()}</main>
            </div>
        </ToastProvider>
    );
}

export default App;
