import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  HomeIcon,
  FolderIcon,
  CheckIcon,
  UsersIcon,
  ClockIcon,
  ChartBarIcon,
  CogIcon,
} from '@heroicons/react/24/outline';
import { useAuth } from '../contexts/AuthContext';
import { t } from '../utils/translations';

const Sidebar = () => {
  const { user, isAdmin, isDeveloper, isClient } = useAuth();

  const adminNavigation = [
    { name: t('dashboard', 'Tableau de bord'), href: '/app/admin', icon: HomeIcon },
    { name: t('projects', 'Projets'), href: '/app/admin/projects', icon: FolderIcon },
    { name: t('tasks', 'Tâches'), href: '/app/admin/tasks', icon: CheckIcon },
    { name: t('users', 'Utilisateurs'), href: '/app/admin/users', icon: UsersIcon },
    { name: 'Statistiques de Pointage', href: '/app/admin/pointage', icon: ClockIcon },
  ];

  const developerNavigation = [
    { name: t('dashboard', 'Tableau de bord'), href: '/app/developer', icon: HomeIcon },
    { name: 'Mes Tâches', href: '/app/developer/tasks', icon: CheckIcon },
    { name: t('pointage', 'Pointage'), href: '/app/developer/pointage', icon: ClockIcon },
  ];

  const clientNavigation = [
    { name: t('dashboard', 'Tableau de bord'), href: '/app/client', icon: HomeIcon },
    { name: 'Mes Projets', href: '/app/client/projects', icon: FolderIcon },
  ];

  const getNavigation = () => {
    if (isAdmin) return adminNavigation;
    if (isDeveloper) return developerNavigation;
    if (isClient) return clientNavigation;
    return [];
  };

  const navigation = getNavigation();

  return (
    <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-64 lg:flex-col">
      <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-primary-600 px-6 pb-4">
        <div className="flex h-16 shrink-0 items-center">
          <h1 className="text-white text-xl font-bold">IT Project Manager</h1>
        </div>
        <nav className="flex flex-1 flex-col">
          <ul role="list" className="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" className="-mx-2 space-y-1">
                {navigation.map((item) => (
                  <li key={item.name}>
                    <NavLink
                      to={item.href}
                      className={({ isActive }) =>
                        `group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold ${
                          isActive
                            ? 'bg-primary-700 text-white'
                            : 'text-primary-200 hover:text-white hover:bg-primary-700'
                        }`
                      }
                    >
                      <item.icon
                        className="h-6 w-6 shrink-0"
                        aria-hidden="true"
                      />
                      {item.name}
                    </NavLink>
                  </li>
                ))}
              </ul>
            </li>
            <li className="mt-auto">
              <div className="flex items-center gap-x-4 px-2 py-3 text-sm font-semibold leading-6 text-primary-200">
                <div className="h-8 w-8 rounded-full bg-primary-700 flex items-center justify-center">
                  <span className="text-white text-sm font-medium">
                    {user?.first_name?.[0]}{user?.last_name?.[0]}
                  </span>
                </div>
                <div className="flex flex-col">
                  <span className="text-white text-sm">
                    {user?.first_name} {user?.last_name}
                  </span>
                  <span className="text-primary-300 text-xs">
                    {user?.role === 'admin' ? 'Administrateur' : 
                     user?.role === 'developer' ? 'Développeur' : 'Client'}
                  </span>
                </div>
              </div>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
