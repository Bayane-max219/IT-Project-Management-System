import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';

// Pages d'authentification
import LoginPage from './pages/auth/LoginPage';
import RegisterWithKeyPage from './pages/auth/RegisterWithKeyPage';

// Pages Admin
import AdminDashboard from './pages/admin/AdminDashboard';
import ProjectsPage from './pages/admin/ProjectsPage';
import TasksPage from './pages/admin/TasksPage';
import UsersPage from './pages/admin/UsersPage';
import PointageStatsPage from './pages/admin/PointageStatsPage';
import PointageStatsPageNew from './pages/admin/PointageStatsPageNew';

// Pages Développeur
import DeveloperDashboard from './pages/developer/DeveloperDashboard';
import MyTasksPage from './pages/developer/MyTasksPage';
import PointagePage from './pages/developer/PointagePage';

// Pages Client
import ClientDashboard from './pages/client/ClientDashboard';
import ClientProjectsPage from './pages/client/ClientProjectsPage';

// Pages communes
import ProfilePage from './pages/common/ProfilePage';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="App">
          <Routes>
            {/* Routes publiques */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/admin/pointage" element={<PointageStatsPage />} />
            <Route path="/admin/pointage-fixed" element={<PointageStatsPageNew />} />
            <Route path="/register" element={<RegisterWithKeyPage />} />
            <Route path="/" element={<Navigate to="/login" replace />} />
            
            {/* Routes protégées avec Layout */}
            <Route path="/app" element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }>
              {/* Routes Admin */}
              <Route path="admin" element={
                <ProtectedRoute requiredRole="admin">
                  <AdminDashboard />
                </ProtectedRoute>
              } />
              <Route path="admin/projects" element={
                <ProtectedRoute requiredRole="admin">
                  <ProjectsPage />
                </ProtectedRoute>
              } />
              <Route path="admin/tasks" element={
                <ProtectedRoute requiredRole="admin">
                  <TasksPage />
                </ProtectedRoute>
              } />
              <Route path="admin/users" element={
                <ProtectedRoute requiredRole="admin">
                  <UsersPage />
                </ProtectedRoute>
              } />
              <Route path="admin/pointage" element={
                <ProtectedRoute requiredRole="admin">
                  <PointageStatsPage />
                </ProtectedRoute>
              } />
              <Route path="admin/pointage-fixed" element={
                <ProtectedRoute requiredRole="admin">
                  <PointageStatsPageNew />
                </ProtectedRoute>
              } />
              
              {/* Routes Développeur */}
              <Route path="developer" element={
                <ProtectedRoute requiredRole="developer">
                  <DeveloperDashboard />
                </ProtectedRoute>
              } />
              <Route path="developer/tasks" element={
                <ProtectedRoute requiredRole="developer">
                  <MyTasksPage />
                </ProtectedRoute>
              } />
              <Route path="developer/pointage" element={
                <ProtectedRoute requiredRole="developer">
                  <PointagePage />
                </ProtectedRoute>
              } />
              
              {/* Routes Client */}
              <Route path="client" element={
                <ProtectedRoute requiredRole="client">
                  <ClientDashboard />
                </ProtectedRoute>
              } />
              <Route path="client/projects" element={
                <ProtectedRoute requiredRole="client">
                  <ClientProjectsPage />
                </ProtectedRoute>
              } />
              
              {/* Route commune - Profil accessible à tous les utilisateurs connectés */}
              <Route path="profile" element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              } />
            </Route>
            
            {/* Route par défaut */}
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
          
          <ToastContainer
            position="top-right"
            autoClose={5000}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
            theme="light"
          />
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
