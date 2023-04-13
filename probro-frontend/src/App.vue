<script lang="ts">
import ProductList from "./components/ProductList.vue";
import { DefaultApi, Product } from "../build/generated/openapi/index";
import { defineComponent } from "vue";

export default defineComponent({
  components: {
    ProductList
  },
  data() {
    const api = new DefaultApi();

    return {
      api,
      products: [] as Product[]
    }
  },
  created() {
    this.api.apiProductsGet().then(it => this.products = it.data)
  }
});

</script>

<template>
  <h1>ProBro</h1>
  <div v-for="product in products">
    <pre>{{JSON.stringify(product)}}</pre>
    <ProductList :product="product" ></ProductList>
  </div>
</template>

<style scoped>
.logo {
  height: 60em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
