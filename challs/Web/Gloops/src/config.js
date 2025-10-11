export const users = [
  {
    id: 1,
    login: 'patpouilleux',
    password: 'verysecureadmin'
  },
  {
    id: 2,
    login: 'demo',
    password: 'demo123'
  }
];

export const organizations = [
  {
    id: '9ef9db99-4e8a-4af0-a096-7dd09d0479b8',
    name: 'Toto Energies',
    publicDescription: 'Les fermes à patate électrique',
    internalDescription: 'Les meilleures fermes à patate électrique, même si c\'est aussi les seules...',
    admins: [1]
  },
  {
    id: 'd4c6edd7-d3c2-4795-8872-78c12b7e26a0',
    name: 'Super V',
    publicDescription: 'V, les nouveaux virtualiseurs !',
    internalDescription: 'La virtualisation à tous les niveaux',
    admins: []
  },
  {
    id: 'ac1e5c19-0950-4538-bd12-0fa9609a0e14',
    name: 'Flag Corp',
    publicDescription: 'Nous possédons les drapeaux.',
    internalDescription: process.env.FLAG || 'CYBN{FAKE_FLAG_CALL_AN_ADMIN}',
    admins: []
  },
  {
    id: '9a9947b4-ef6e-4c2d-b6af-13026803ecda',
    name: 'Aux Champs',
    publicDescription: 'Et la vie est plus chère',
    internalDescription: 'Vous êtes sur la bonne voie !',
    admins: []
  }
]