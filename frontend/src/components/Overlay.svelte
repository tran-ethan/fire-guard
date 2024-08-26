<script lang="ts">
    // Imports
    import * as Collapsible from "$lib/components/ui/collapsible";
    import ChevronsUpDown from "lucide-svelte/icons/chevrons-up-down";
    import { Button } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import CalendarIcon from "lucide-svelte/icons/calendar";
    import type { DateRange } from "bits-ui";
    import {
      CalendarDate,
      DateFormatter,
      type DateValue,
      getLocalTimeZone
    } from "@internationalized/date";
    import { cn } from "$lib/utils.js";
    import { RangeCalendar } from "$lib/components/ui/range-calendar/index.js";
    import * as Popover from "$lib/components/ui/popover/index.js";

    // Calendar

  const df = new DateFormatter("en-US", {
    dateStyle: "medium"
  });
 
  let value: DateRange | undefined = {
    start: new CalendarDate(2022, 1, 20),
    end: new CalendarDate(2022, 1, 20).add({ days: 20 })
  };
 
  let startValue: DateValue | undefined = undefined;
  
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
        <div class="grid gap-2">
          <Popover.Root openFocus>
            <Popover.Trigger asChild let:builder>
              <Button
                variant="outline"
                class={cn(
                  "w-[300px] justify-start text-left font-normal",
                  !value && "text-muted-foreground"
                )}
                builders={[builder]}
              >
                <CalendarIcon class="mr-2 h-4 w-4" />
                {#if value && value.start}
                  {#if value.end}
                    {df.format(value.start.toDate(getLocalTimeZone()))} - {df.format(
                      value.end.toDate(getLocalTimeZone())
                    )}
                  {:else}
                    {df.format(value.start.toDate(getLocalTimeZone()))}
                  {/if}
                {:else if startValue}
                  {df.format(startValue.toDate(getLocalTimeZone()))}
                {:else}
                  Pick a date
                {/if}
              </Button>
            </Popover.Trigger>
            <Popover.Content class="w-auto p-0" align="start">
              <RangeCalendar
                bind:value
                bind:startValue
                initialFocus
                numberOfMonths={2}
                placeholder={value?.start}
              />
            </Popover.Content>
          </Popover.Root>
        </div>
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
        <Input type="number" placeholder="Latitude" class="font-lilita-one mx-[10px] my-0 px-[10px] py-[5px] w-[100px] max-h-[30px] text-[18px] border border-[rgba(180,159,155,0.895)] rounded-[4px] outline-none bg-transparent" />
        <Input type="number" placeholder="Longitude" class="max-w-xs font-lilita-one mx-[10px] my-0 px-[10px] py-[5px] w-[100px] max-h-[30px] text-[18px] border border-[rgba(180,159,155,0.895)] rounded-[4px] outline-none bg-transparent" />
      </Collapsible.Content>
    </Collapsible.Root>
  </div>