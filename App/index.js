const axios = require('axios').default;

// 1. Define route components.
// These can be imported from other files
const Home = { template: '<inicio></inicio>' }
const Crear = { template: '<creador-links></creador-links>' }
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

app.component('buscador', {
  template: `
    <div>
      <buscador-input></buscador-input>
      <link-display></link-display>
    </div>`
})

app.component('buscador-input', {
  data() {
    return {
      busqueda: ""
    }
  },
  methods: {
    buscar () {
      this.$emit
    }
  },
  template: `
    <div>
      <p>{{busqueda}}</p>
      <label for="busqueda">Ingrese un nombre del link</label>
      <input v-model="busqueda" type="text" name="busqueda">
      <button v-on:click="buscar()" >Buscar</button>
    </div>`
})

app.component('link-display', {
  template: `
    <div>
      Aquí el link!
    </div>`
})

app.component('creador-links', {
  template: `
    <div>
      Aquí el creador de links
    </div>`
})

app.component('inicio', {
  template: `
    <div>
      Inicio de la aplicación
    </div>`
})

app.use(router);

app.mount('#app');