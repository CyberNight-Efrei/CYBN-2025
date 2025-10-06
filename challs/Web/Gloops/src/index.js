import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import * as config from './config.js';
import { expressjwt } from "express-jwt";
import jwt from 'jsonwebtoken';

const app = express();
app.use(cors());
app.use(bodyParser.json());

function auth(req, res, next) {
  return expressjwt({ secret: process.env.JWT_SECRET, algorithms: ["HS256"] })(req, res, next);
}

function isAdmin(user, organization) {
  return config.organizations.some(org => org.admins.includes(user.sub));
}

app.use(express.static('public', { extensions: ['html'] }));

app.get('/organizations/:id', (req, res) => {
  const org = config.organizations.find(org => org.id === req.params.id);
  if (!org) {
    return res.redirect('/');
  }
  res.sendFile(process.cwd() + '/public/organizations/index.html');
});

app.get('/admin/organizations/:id', (req, res) => {
  const org = config.organizations.find(org => org.id === req.params.id);
  if (!org) {
    return res.redirect('/');
  }
  res.sendFile(process.cwd() + '/public/admin/organizations/index.html');
});

app.post('/api/login', (req, res) => {
  console.log(req.body)
  const { login, password } = req.body;
  const user = config.users.find(user => user.login === login && user.password === password);
  if (!user) {
    return res.status(401).send({ error: 'Invalid credentials' });
  }
  const token = jwt.sign({ sub: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
  res.send({ token });
})

app.get('/api/organizations/', auth, (req, res) => {
  res.send(config.organizations.map(org => ({
    id: org.id,
    name: org.name,
    publicDescription: org.publicDescription,
    admins: org.admins.map(adminId => config.users.find(user => user.id === adminId))
  })));
});

app.get('/api/organizations/:id', auth, (req, res) => {
  const org = config.organizations.find(org => org.id === req.params.id);
  if (!org) {
    return res.status(404).send({ error: 'Organization not found' });
  }
  res.send({
    id: org.id,
    name: org.name,
    publicDescription: org.publicDescription,
    admins: org.admins.map(adminId => config.users.find(user => user.id === adminId))
  });
});

app.get('/api/admin/organizations/', auth, (req, res) => {
  if (!isAdmin(req.auth, null)) return res.status(403).send({ error: 'Forbidden' });
  res.send(config.organizations.filter(org => org.admins.includes(req.auth.sub)).map(org => ({
    ...org,
    admins: org.admins.map(adminId => config.users.find(user => user.id === adminId))
  })));
});

app.get('/api/admin/organizations/:id', auth, (req, res) => {
  if (!isAdmin(req.auth, null)) return res.status(403).send({ error: 'Forbidden' });
  const org = config.organizations.find(org => org.id === req.params.id);
  if (!org) {
    return res.status(404).send({ error: 'Organization not found' });
  }
  res.send({
    ...org,
    admins: org.admins.map(adminId => config.users.find(user => user.id === adminId))
  });
});

app.listen(process.env.PORT || 8000, () => {
  console.log(`Server is running on port ${process.env.PORT || 8000}`);
});