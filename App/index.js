// 1. Define route components.
// These can be imported from other files
const Home = { template: '<div>Home</div>' }
const Crear = { template: '<div>Crear</div>' }
const Buscar = { template: '<buscador></buscador>' }

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  { path: '/', component: Home },
  { path: '/crear', component: Crear },
  { path: '/buscar', component: Buscar }
]

const router = VueRouter.createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: VueRouter.createWebHashHistory(),
  routes, // short for `routes: routes`
})


const app = Vue.createApp({});

// Define a new global component called button-counter
app.component('buscador', {
  data() {
    return {
      count: 0
    }
  },
  template: `
    <div>
      Aquí el buscador
    </div>`
})

app.use(router);

app.mount('#app');