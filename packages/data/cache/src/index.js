export function createInMemoryCache() {
  const store = new Map();

  return {
    get(key) {
      return store.get(key);
    },
    set(key, value) {
      store.set(key, value);
      return value;
    },
    has(key) {
      return store.has(key);
    }
  };
}
