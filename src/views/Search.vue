<template>
  <div class="about">
    <h1>Buscador de links</h1>
    <buscador></buscador>
  </div>
</template>

<script>
// @ is an alias to /src
import Buscador from '@/components/Buscador.vue'

export default {
  name: 'Home',
  components: {
    Buscador
  }
}
</script>
