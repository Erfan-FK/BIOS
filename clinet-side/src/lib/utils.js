import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export function slotToString(slot) {
  switch (slot) {
    case 0:
      return "9:00";
    case 1:
      return "11:30";
    case 2:
      return "14:00";
    case 3:
      return "16:00";
    default:
      return "Invalid Slot";
  }
}
