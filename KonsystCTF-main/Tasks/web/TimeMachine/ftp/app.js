const express = require('express');
const path = require('path');
const fs = require('fs');
const basicAuth = require('express-basic-auth');
const app = express();

const users = {
  'guest': 'guest',
  'admin': 'ITPORTAL2000'
};

app.use(basicAuth({
  users: users,
  challenge: true,
  realm: 'FTP Server',
  unauthorizedResponse: 'Неавторизованный доступ'
}));

app.use('/static', express.static(path.join(__dirname, 'public')));
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

const sanitizePath = (userDir) => (req, res, next) => {
  const basePath = path.join(__dirname, userDir);
  const param = req.query.param || '';
  
  try {
    const requestedPath = path.resolve(basePath, param);
    if (!requestedPath.startsWith(basePath)) {
      throw new Error('Path traversal attempt');
    }
    req.filePath = requestedPath;
    next();
  } catch (error) {
    res.redirect('/?error=INVALID_PATH');
  }
};

app.get('/', (req, res) => {
  const { cmd = 'LIST', param = '' } = req.query;
  let output = '';
  const username = req.auth.user;
  const userDir = username === 'admin' ? 'admin-files' : 'files';
  const basePath = path.join(__dirname, userDir);

  try {
    if (cmd === 'LIST') {
      const files = fs.readdirSync(basePath);
      output = files.map(file => {
        const stats = fs.statSync(path.join(basePath, file));
        return `
          <tr>
            <td><a href="/ftp?cmd=RETR&param=${encodeURIComponent(file)}">${file}</a></td>
            <td>${stats.mtime.toLocaleDateString('ru-RU')}</td>
            <td>${stats.size} bytes</td>
          </tr>
        `;
      }).join('');
    } else if (cmd === 'RETR') {
      const filePath = path.resolve(basePath, param);
      if (!filePath.startsWith(basePath)) {
        throw new Error('Invalid path');
      }
      output = fs.readFileSync(filePath, 'utf8');
    }
  } catch (error) {
    return res.redirect(`/ftp?error=${error.message.includes('ENOENT') ? 'FILE_NOT_FOUND' : 'SERVER_ERROR'}`);
  }

  res.render('index', {
    cmd,
    param,
    output,
    user: username,
    error: req.query.error,
    helpers: {
      rawHtml: (text) => text
    }
  });
});

app.listen(3001, () => console.log('FTP server running on 3001'));