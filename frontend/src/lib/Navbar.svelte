<script>

  import { Navbar, NavBrand, NavHamburger, NavLi, NavUl } from "flowbite-svelte";

</script>
<Navbar let:NavContainer color="primary" class="flex flex-row">
    <NavContainer class="border px-5 py-2 rounded-lg bg-white dark:bg-gray-600">
      <NavBrand href="/">
        <img src="/fireguard-logo.webp" class="size-10" alt="Fire Guard Logo" />
        <span class="self-center whitespace-nowrap text-xl font-semibold">Fire Guard</span>
      </NavBrand>
    </NavContainer>
  </Navbar>