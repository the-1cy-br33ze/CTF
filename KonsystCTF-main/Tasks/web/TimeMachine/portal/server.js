const express = require('express');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const app = express();

const { createProxyMiddleware } = require('http-proxy-middleware');

// Fix 1: Подключаем парсеры ДО маршрутов
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/ftp', createProxyMiddleware({
  target: 'http://ftp:3001',
  changeOrigin: true,
  pathRewrite: { '^/ftp': '' }
}));

app.use(cookieParser());
app.use(express.static('public'));
app.set('view engine', 'ejs');

app.use(session({
  secret: 'supersecret',
  resave: false,
  saveUninitialized: true,
  cookie: { 
    secure: false,
    sameSite: 'lax'
  }
}));

const accessChecks = {
  check1: (req) => {
    const ua = req.get('User-Agent') || '';
    return ['Mozilla/4', 'Netscape', 'Windows NT 5', 'Windows NT 4', 'Mozilla/2', 'Mozilla/3', 'MSIE 3.0', 'MSIE 2', 'MSIE 1', 'Windows XP']
      .some(p => ua.includes(p));
  },
  check2: (req) => {
    const allowed = [[1024,768], [800,600], [640,480]];
    const w = req.session.width;
    const h = req.session.height;
    console.log('check 2: ', allowed.some(([aw, ah]) => w === aw && h === ah));
    return allowed.some(([aw, ah]) => w === aw && h === ah);s

  },
  check3: (req) => {
    const clientDate = new Date(req.session.clientDate);
    const cutoffDate = new Date('2001-01-01T00:00:00');
    console.log('ClientDate: ', clientDate);
    console.log('cuttofDate: ', cutoffDate);
    console.log('check 3: ', clientDate < cutoffDate);
    return clientDate < cutoffDate;
  }
};

app.use((req, res, next) => {
  if(!req.cookies.theme) res.cookie('theme', 'modern', { maxAge: 31536000000 });
  
  res.locals.checks = {
    check1: accessChecks.check1(req),
    check2: accessChecks.check2(req),
    check3: accessChecks.check3(req)
  };
  
  res.locals.theme = req.cookies.theme === 'retro' && 
                     res.locals.checks.check1 && 
                     res.locals.checks.check2 &&
                     res.locals.checks.check3 
                     ? 'retro' : 'modern';
  next();
});

app.post('/api/screen', (req, res) => {
  const {width, height} = req.body;
  if(width && height) {
    req.session.width = parseInt(width, 10);
    req.session.height = parseInt(height, 10);
  }
  res.header('Access-Control-Allow-Origin', req.headers.origin);
  res.header('Access-Control-Allow-Credentials', 'true');
  res.sendStatus(200);
});

app.post('/api/date', (req, res) => {
  const { date } = req.body;
  if(date) {
    req.session.clientDate = date;
  }
  res.header('Access-Control-Allow-Origin', req.headers.origin);
  res.header('Access-Control-Allow-Credentials', 'true');
  res.sendStatus(200);
});

app.get('/toggle-theme', (req, res) => {
  const newTheme = req.cookies.theme === 'retro' ? 'modern' : 'retro';
  const errors = [];
  
  if(newTheme === 'retro') {
    if(!res.locals.checks.check1) errors.push('1');
    if(!res.locals.checks.check2) errors.push('2');
    if(!res.locals.checks.check3) errors.push('3');
  }
  
  if(errors.length) {
    res.cookie('themeError', 'blocked', {maxAge: 1000});
  } else {
    res.cookie('theme', newTheme, {maxAge: 31536000000});
  }
  res.redirect('back');
});

app.use((req, res, next) => {
  res.locals.themeErrors = (req.cookies.themeError || '').split(',').filter(Boolean);
  if(req.cookies.themeError) res.clearCookie('themeError');
  next();
});

app.get('/', (req, res) => res.render('index'));
app.get('/about', (req, res) => res.render('about'));
app.get('/contact', (req, res) => res.render('contact'));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));