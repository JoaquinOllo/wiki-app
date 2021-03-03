<template>
  <div>
    <p>{{ busqueda }}</p>
    <label for="busqueda">Ingrese un nombre del link</label>
    <input v-model="busqueda" type="text" name="busqueda" />
    <button v-on:click="buscar">Buscar</button>
  </div>
</template>

<script>
export default {
  name: 'buscador-input',
  data () {
    return {
      busqueda: ''
    }
  },
  methods: {
    buscar () {
      this.$emit('buscar', this.busqueda)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
