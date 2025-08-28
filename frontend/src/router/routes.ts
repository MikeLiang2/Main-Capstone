
import type { RouteRecordRaw } from 'vue-router'

export const constantRoute: RouteRecordRaw[] = [

    // login route
    // This route is used for the login page
    {
        path: '/login',
        name: 'login',
        component: () => import('@/views/login/index.vue'),
        meta: {
            title: 'Login',
            hidden: true, // This route is hidden in the menu
            icon: 'Avatar', // Icon for the login page
        }
    },

    {
        path: '/',
        name: 'layout',
        component: () => import('@/layout/index.vue'),
        meta: {
            title: 'Home',
            hidden: false, // This route is not hidden in the menu
            icon: 'House', // Icon for the layout
        },
        redirect: '/home', // Redirect to home page
        children: [
            {
                path: '/home',
                name: 'home',
                component: () => import('@/views/home/index.vue'),
                meta: {
                    title: 'Home',
                    hidden: false, // This route is not hidden in the menu
                    icon: 'House', // Icon for the home page
                }
            }
        ]
    },

    // 404 route
    {
        path: '/404',
        name: '404',
        component: () => import('@/views/404/index.vue'),
        meta: {
            title: '404 Not Found',
            hidden: true, // This route is hidden in the menu
        }
    },

    // other routes
    {
        path: '/:pathMatch(.*)*',
        redirect: '/404',
        name: 'Any',
        meta: {
            title: 'Any Route',
            hidden: true, // This route is hidden in the menu
        }
    },

    {
        path: '/checklist',
        name: 'checklist',
        component: () => import('@/layout/index.vue'),
        meta: {
            title: 'Checklist',
            hidden: false, // This route is not hidden in the menu
            icon: 'FolderChecked', // Icon for the checklist page
        },
        children: [
            {
                path: '/checklist/editchecklist',
                name: 'ChecklistManage',
                component: () => import('@/views/checklist/editchecklist/editchecklist.vue'),
                meta: {
                    title: 'Edit Checklist',
                    hidden: false, // This route is not hidden in the menu
                    icon: 'EditPen', // Icon for the edit checklist page
                }
            },
            {
                path: '/checklist/addchecklist',
                name: 'AddChecklist',
                component: () => import('@/views/checklist/addchecklist/index.vue'),
                meta: {
                    title: 'Add Checklist',
                    hidden: false, // This route is not hidden in the menu
                    icon: 'DocumentAdd', // Icon for the add checklist page
                }
            },
            {
                path: '/checklist/ai-generate',
                name: 'AIGenerateChecklist',
                component: () => import('@/views/checklist/ai-generate/index.vue'),
                meta: {
                    title: 'AI Checklist',
                    hidden: false,
                    icon: 'Cpu',
                }
            },
            {
                path: '/checklist/editchecklist/:id', // 动态参数 :id
                name: 'EditChecklist',
                component: () => import('@/views/checklist/addchecklist/index.vue'),
                meta: {
                    title: 'Edit Checklist',
                    hidden: true,
                    icon: 'EditPen'
                }
            }
        ]
    },

    {
        path: '/people',
        name: 'people',
        component: () => import('@/layout/index.vue'),
        meta: {
            title: 'People management',
            hidden: false, // This route is not hidden in the menu
            icon: 'UserFilled', // Icon for the people page
        },
        children: [
            {
                path: '/people/premission',
                component: () => import('@/views/people/premission/index.vue'),
                meta: {
                    title: 'Permission',
                    hidden: false, // This route is not hidden in the menu
                    icon: 'Lock', // Icon for the add permission page
                }
            },
            {
                path: '/people/role',
                component: () => import('@/views/people/role/role.vue'),
                meta: {
                    title: 'Role',
                    hidden: false, // This route is not hidden in the menu
                    icon: 'User', // Icon for the add role page
                }
            }

        ]

    },

    {
        path: '/',
        name: 'settings',
        component: () => import('@/layout/index.vue'),
        meta: {
            title: 'Settings',
            hidden: false, 
            icon: 'Setting', 
        },
        redirect: '/settings',
        children: [
            {
                path: '/settings',
                name: 'all settings',
                component: () => import('@/views/settings/index.vue'),
                meta: {
                    title: 'Settings',
                    hidden: false, 
                    icon: 'Setting',
                }
            }
        ]
    },

    {
        path: '/register',
        name: 'register',
        component: () => import('@/views/register/register.vue'),
        meta: {
            title: 'Register',
            hidden: true
        }
    }
    // {
    //     path: '/checklist/view/:id',
    //     name: 'ViewChecklist',
    //     component: () => import('@/views/checklist/viewchecklist/ChecklistPage.vue'),
    //     meta: { title: 'View Checklist' }
    // }


]
