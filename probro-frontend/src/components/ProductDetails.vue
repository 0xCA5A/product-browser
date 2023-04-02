<script lang="ts">
import {defineComponent, PropType} from "vue";
import {DefaultApi, Environment, EnvironmentStatusEnum, Product} from "../../build/generated/openapi/index";

export default defineComponent({
  name: "ProductDetails",
  computed: {
    EnvironmentStatusEnum() {
      return EnvironmentStatusEnum
    }
  },
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
  <div v-for="environment in environments"
       :style="{color: environment.status === EnvironmentStatusEnum.Up  ? 'green' : 'red'}"
       class="col-md-5 padding">
    <h2>Environment Name: {{ environment.name }}</h2>
    <ul class="list-group">
      <li style="background-color:lightcyan" class="list-group-item">ID: {{ environment.id }}</li>
      <li style="background-color:lightcyan" class="list-group-item">Status: {{ environment.status }}</li>
    </ul>
  </div>
</template>

<style scoped>
.padding {
  margin: 10px;
  padding: 10px;
}
</style>
