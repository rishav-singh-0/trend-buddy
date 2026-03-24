export function sumBy(items, selector) {
  return items.reduce((total, item) => total + selector(item), 0);
}

export function groupBy(items, selector) {
  return items.reduce((groups, item) => {
    const key = selector(item);
    groups[key] ??= [];
    groups[key].push(item);
    return groups;
  }, {});
}

export function parseCsv(text) {
  const [headerLine, ...rows] = text.trim().split("\n");
  const headers = headerLine.split(",");

  return rows.map((row) => {
    const values = row.split(",");
    return headers.reduce((record, header, index) => {
      record[header] = values[index];
      return record;
    }, {});
  });
}
