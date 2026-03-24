export const USER_ROLES = Object.freeze(["viewer", "trader", "admin"]);

export function canPlaceOrders(role) {
  return role === "trader" || role === "admin";
}
