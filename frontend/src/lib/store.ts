import { writable } from "svelte/store";

export const filtersRotated = writable<boolean>(false);
export const coordinatesY = writable<number>(3);

export const showPopup= writable<boolean>(false);