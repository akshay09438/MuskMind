export const PLANETS = [
  {
    id: 'earth',
    name: 'Earth',
    color: '#3fa9f5',
    gravityScale: 1.0,
    available: true,
    sublevels: [
      { name: 'Twig', hp: 3, radius: 32, color: '#c9975a', motion: 'static', comboWindow: 0.9, timeTarget3: 5, timeTarget2: 10 },
      { name: 'Branch', hp: 5, radius: 38, color: '#b5824a', motion: 'static', comboWindow: 0.85, timeTarget3: 7, timeTarget2: 13 },
      { name: 'Log', hp: 8, radius: 46, color: '#8f6539', motion: 'drift', comboWindow: 0.75, timeTarget3: 10, timeTarget2: 17 },
      { name: 'Knotted Trunk', hp: 12, radius: 52, color: '#6e4c2a', motion: 'drift', comboWindow: 0.65, timeTarget3: 13, timeTarget2: 22, guard: true, guardOpenDuration: 1.4, guardClosedDuration: 0.6 },
      { name: 'Ironwood Stump', hp: 18, radius: 58, color: '#4a3220', motion: 'swing', comboWindow: 0.55, timeTarget3: 17, timeTarget2: 28, guard: true, guardOpenDuration: 1.1, guardClosedDuration: 0.8 }
    ]
  },
  { id: 'mercury', name: 'Mercury', color: '#9c9c9c', gravityScale: 0.38, available: false, sublevels: [] },
  { id: 'venus', name: 'Venus', color: '#e8c37e', gravityScale: 0.9, available: false, sublevels: [] },
  { id: 'mars', name: 'Mars', color: '#c1440e', gravityScale: 0.38, available: false, sublevels: [] },
  { id: 'jupiter', name: 'Jupiter', color: '#d8ae70', gravityScale: 2.53, available: false, sublevels: [] },
  { id: 'saturn', name: 'Saturn', color: '#e3c078', gravityScale: 1.07, available: false, sublevels: [] },
  { id: 'uranus', name: 'Uranus', color: '#8fd1d9', gravityScale: 0.89, available: false, sublevels: [] },
  { id: 'neptune', name: 'Neptune', color: '#4b6cb7', gravityScale: 1.14, available: false, sublevels: [] }
];

export function getPlanet(id) {
  return PLANETS.find((p) => p.id === id);
}
