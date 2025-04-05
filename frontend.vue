<template>
  <section class="bg-blue-600 text-white flex items-center justify-center w-full px-12" style="width: 1200px; height: 800px;">
    <div class="w-1/2">
      <h1 class="text-6xl font-bold leading-tight">Supercharge Your Sales with AI-Powered Sales Forecasting</h1>
      <h4>Powered by NVIDIA RAPIDS | Built for Business Growth</h4>
      <p class="text-lg mt-6">In today’s fast-paced world, predicting sales accurately can be the difference between success and failure. 
      Kuppitek’s AI-Powered Sales Forecasting leverages cutting-edge machine learning and real-time data analytics to help businesses make smarter, faster, and more profitable decisions. 
      With the power of NVIDIA RAPIDS, our AI-driven solution analyzes market trends, customer behavior, and historical sales data to deliver precise forecasts that drive revenue growth. 
      No more guesswork—just data-backed, intelligent insights that help you stay ahead of the competition.</p>
      <div class="mt-8">
        <a href="#features" class="bg-yellow-500 text-blue-900 px-6 py-3 rounded-lg font-semibold hover:bg-yellow-600 transition">Explore Features</a>
        <a href="#contact" class="ml-4 border border-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition">Get in Touch</a>
      </div>
    </div>
    <div class="w-1/2 bg-white p-8 rounded-lg shadow-lg text-center">
      <h2 class="text-2xl font-semibold text-blue-600 mb-4">Sales Prediction Tool</h2>
      <input
        type="number"
        name="customer_interactions"
        placeholder="Customer Interactions"
        v-model.number="inputs.customer_interactions"
        class="border p-2 w-full rounded-md mb-2"
      />
      <input
        type="number"
        name="ad_spend"
        placeholder="Ad Spend ($)"
        v-model.number="inputs.ad_spend"
        class="border p-2 w-full rounded-md mb-2"
      />
      <input
        type="number"
        name="previous_sales"
        placeholder="Previous Sales ($)"
        v-model.number="inputs.previous_sales"
        class="border p-2 w-full rounded-md mb-2"
      />
      <button
        @click="handlePredict"
        :disabled="loading"
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition mt-4"
      >
        {{ loading ? "Predicting..." : "Predict Sales" }}
      </button>
      <h3 class="mt-4 text-xl font-bold text-blue-600">Predicted Sales: {{ prediction !== null ? `$${prediction.toFixed(2)}` : "N/A" }}</h3>
    </div>
  </section>
</template>

<script>
import { ref } from "vue";

export default {
  name: "HeroSection",
  setup() {
    const inputs = ref({
      customer_interactions: "",
      ad_spend: "",
      previous_sales: "",
    });
    const prediction = ref(null);
    const loading = ref(false);

    const handlePredict = async () => {
      loading.value = true;
      try {
        const response = await fetch("http://localhost:5000/predict", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            customer_interactions: [parseFloat(inputs.value.customer_interactions)],
            ad_spend: [parseFloat(inputs.value.ad_spend)],
            previous_sales: [parseFloat(inputs.value.previous_sales)],
          }),
        });

        const data = await response.json();
        prediction.value = data.predicted_sales[0];
      } catch (error) {
        console.error("Error fetching prediction:", error);
        prediction.value = "Error: Unable to predict.";
      }
      loading.value = false;
    };

    return {
      inputs,
      prediction,
      loading,
      handlePredict,
    };
  },
};
</script>

<style scoped>
section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1480px;
  height: 800px;
  margin: 0 auto;
}
</style>
