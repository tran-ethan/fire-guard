<script lang="ts">
    // Imports
    import * as Collapsible from "$lib/components/ui/collapsible";
    import ChevronsUpDown from "lucide-svelte/icons/chevrons-up-down";
    import { Button } from "$lib/components/ui/button/index.js";
    import CalendarIcon from "lucide-svelte/icons/calendar";
    import {
        DateFormatter,
        type DateValue,
        getLocalTimeZone
    } from "@internationalized/date";
    import { cn } from "$lib/utils.js";
    import { Calendar } from "$lib/components/ui/calendar/index.js";
    import * as Popover from "$lib/components/ui/popover/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    
    // Calendar
    const df = new DateFormatter("en-US", {
        dateStyle: "long"
    });
    
    let value: DateValue | undefined = undefined;

</script>

<div style="position: absolute; z-index: 30;">
    <Collapsible.Root class="w-[350px] space-y-2">
      <div class="flex items-center justify-between space-x-4 px-4">
        <h1 class="text-xl font-semibold">Filter by date</h1>
        <Collapsible.Trigger asChild let:builder>
          <Button builders={[builder]} variant="ghost" size="sm" class="w-9 p-0">
            <ChevronsUpDown class="h-4 w-4" />
            <span class="sr-only">Toggle</span>
          </Button>
        </Collapsible.Trigger>
      </div>
      <Collapsible.Content class="space-y-2">
        <Popover.Root>
            <Popover.Trigger asChild let:builder>
                <Button
                variant="outline"
                class={cn(
                    "w-[280px] justify-start text-left font-normal",
                    !value && "text-muted-foreground"
                )}
                builders={[builder]}
                >
                <CalendarIcon class="mr-2 h-4 w-4" />
                {value ? df.format(value.toDate(getLocalTimeZone())) : "Pick a start date"}
                </Button>
            </Popover.Trigger>
            <Popover.Content class="w-auto p-0">
                <Calendar bind:value initialFocus />
            </Popover.Content>
        </Popover.Root>
        <Popover.Root>
            <Popover.Trigger asChild let:builder>
                <Button
                variant="outline"
                class={cn(
                    "w-[280px] justify-start text-left font-normal",
                    !value && "text-muted-foreground"
                )}
                builders={[builder]}
                >
                <CalendarIcon class="mr-2 h-4 w-4" />
                {value ? df.format(value.toDate(getLocalTimeZone())) : "Pick an end date"}
                </Button>
            </Popover.Trigger>
            <Popover.Content class="w-auto p-0">
                <Calendar bind:value initialFocus />
            </Popover.Content>
        </Popover.Root>
      </Collapsible.Content>
    </Collapsible.Root>
    <Collapsible.Root class="w-[350px] space-y-2">
      <div class="flex items-center justify-between space-x-4 px-4">
        <h1 class="text-xl font-semibold">Coordinates</h1>
        <Collapsible.Trigger asChild let:builder>
          <Button builders={[builder]} variant="ghost" size="sm" class="w-9 p-0">
            <ChevronsUpDown class="h-4 w-4" />
            <span class="sr-only">Toggle</span>
          </Button>
        </Collapsible.Trigger>
      </div>
      <Collapsible.Content class="space-y-2">
        <Input type="number" placeholder="Latitude" class="max-w-xs" />
        <Input type="number" placeholder="Longitude" class="max-w-xs" />
      </Collapsible.Content>
    </Collapsible.Root>
  </div>