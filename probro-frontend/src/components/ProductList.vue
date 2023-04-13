<script lang="ts">
import { PropType, defineComponent } from "vue";
import { DefaultApi, Environment, Product } from "../../build/generated/openapi/index";

export default defineComponent({
  name: "ProductList",
  props: {
    product: {
      type: Object as PropType<Product>
    } 
  },
  data() {
    const api = new DefaultApi();

    return {
      api,
      environments: [] as Environment[]
    }
  },
  created() {
    this.api.getEnvironments(this.product!.id).then(it => this.environments = it.data)
  }
});

</script>

<template>
  <div v-for="env in environments">
    <h2>Name: {{ env.name }}</h2>
    <ul class="list-group">
      <li class="list-group-item">ID: {{ env.id }}</li>
      <li class="list-group-item">Status: {{ env.status }}</li>
    </ul>  
  </div>
</template>

<style scoped>
</style>
