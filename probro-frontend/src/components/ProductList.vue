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
  <h1>{{ product?.name }}</h1>

  <div v-for="env in environments">
  <pre>{{ JSON.stringify(env) }}</pre>
  
  </div>
</template>

<style scoped>
</style>
