<script lang="ts">
import ProductDetails from "./components/ProductDetails.vue";
import {DefaultApi, Product} from "../build/generated/openapi/index";
import {defineComponent} from "vue";
import '../node_modules/bootstrap/dist/css/bootstrap.css';

export default defineComponent({
  name: "App",
  components: {
    ProductDetails
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
  <div class="container-lg">
    <h1>ProBro</h1>
    <pre>The product browser</pre>
    <div v-for="product in products" style="background-color:lightblue;" class="row padding">
      <h2>Product Name: {{ product.name }}</h2>
      <pre>Product Id: {{ product.id }}</pre>

      <ProductDetails :product="product"></ProductDetails>
    </div>
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

<style scoped>
.padding {
  margin: 10px;
  padding: 10px;
}
</style>
