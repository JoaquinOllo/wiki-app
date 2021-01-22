require(['axios.min'], function (axios) {
  // 1. Define route components.
  // These can be imported from other files
  const Home = { template: '<inicio></inicio>' }
  const Crear = { template: '<creador-links></creador-links>' }
  const Buscar = { template: '<buscador></buscador>' }


  const server = "http://127.0.0.1:5000/";
  
  const getLinksParams = {
    URL: "links/alias/<linkSought>",
    method: "GET"
  };

  const extractParams = (text) => {
    const regExp = RegExp("(?<=<).+?(?=>)", "gi");
    params = Array.from(text.matchAll(regExp));
    return params;
  };

  /**
   * 
   * @param {String} URL a string with the unformatted URL with empty params
   * @param {Array} paramsArray paramsArray should contain field-value pairings
   *
   */
  const fillinURLParams = (URL, paramsArray) => {
    let newURL = URL;
    paramsArray.forEach(param => {
      let regExpPattern = `<${param.field}>`;
      let regExp = RegExp(regExpPattern, "gi");
      newURL = newURL.replace(regExp, param.value)
    });
    return newURL;
  }

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
    data() {
      return {
        link: "hola"
      }
    },
    computed: {
      serviceParams(){
        return getLinksParams;
      }
    },
    watch: {
      link(newLink, oldLink){
        console.log (newLink)
        console.log (oldLink)
      }
    },
    methods: {
      buscar(event) {
        let params = extractParams(this.serviceParams.URL);
        let paramsArray = []
        params.forEach(param => {
          paramsArray.push({"field": param, "value": event})
        });
        axios({
          method: this.serviceParams.method,
          url: server + fillinURLParams(this.serviceParams.URL, paramsArray)
        })
          .then(function (res) {
            $vm.data.link = res.data.links
            console.log ($vm.data.link)
          })
          .catch(function (err) {
            console.log(err)
          })
      }
    },
    template: `
    <div>
      <buscador-input v-on:buscar="buscar($event)"></buscador-input>
      <link-display v-bind:link="link"></link-display>
    </div>`
  })

  app.component('buscador-input', {
    data() {
      return {
        busqueda: ""
      }
    },
    methods: {
      buscar() {
        this.$emit("buscar", this.busqueda);
      }
    },
    template: `
    <div>
      <p>{{busqueda}}</p>
      <label for="busqueda">Ingrese un nombre del link</label>
      <input v-model="busqueda" type="text" name="busqueda">
      <button v-on:click="buscar" >Buscar</button>
    </div>`
  })

  app.component('link-display', {
    props:{
      link: Object
    },
    watch: {
      link(newLink, oldLink){
        console.log (newLink)
        console.log (oldLink)
      }
    },
    template: `
    <div>
      {{link}}
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
});