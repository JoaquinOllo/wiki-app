<template>
  <div>
    <buscador-input v-on:buscar="buscar($event)"></buscador-input>
    <link-display v-bind:link="link"></link-display>
  </div>
</template>

<script>
import BuscadorInput from '@/components/BuscadorInput.vue'
import LinkDisplay from '@/components/LinkDisplay.vue'
import axios from 'axios'
const server = 'https://rpg-wiki-apis.herokuapp.com/'

const getLinksParams = {
  URL: 'links/alias/<linkSought>',
  method: 'GET'
}

const extractParams = (text) => {
  let params = []
  const regExp = RegExp('(?<=<).+?(?=>)', 'gi')
  params = Array.from(text.matchAll(regExp))
  return params
}

const fillinURLParams = (URL, paramsArray) => {
  let newURL = URL
  paramsArray.forEach((param) => {
    const regExpPattern = `<${param.field}>`
    const regExp = RegExp(regExpPattern, 'gi')
    newURL = newURL.replace(regExp, param.value)
  })
  return newURL
}

export default {
  name: 'buscador',
  components: {
    BuscadorInput,
    LinkDisplay
  },
  data () {
    return {
      link: 'hola'
    }
  },
  watch: {
    link (newLink, oldLink) {
      console.log(newLink)
      console.log(oldLink)
    }
  },
  methods: {
    buscar (event) {
      const params = extractParams(getLinksParams.URL)
      const paramsArray = []
      const _this = this
      params.forEach((param) => {
        paramsArray.push({ field: param, value: event })
      })
      axios({
        method: getLinksParams.method,
        url: server + fillinURLParams(getLinksParams.URL, paramsArray)
      })
        .then(function (res) {
          console.log(_this.link)
          _this.link = res.data.links[0]
        })
        .catch(function (err) {
          console.log(err)
        })
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
