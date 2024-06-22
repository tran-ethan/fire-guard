<script lang="ts">
  import "./counter.css";
  let count: number = 0;
  const increment = () => {
    count += 1;
  };
</script>

<button on:click={increment} class="bg-gray-800 text-white p-4;">
  count is {count}
</button>
