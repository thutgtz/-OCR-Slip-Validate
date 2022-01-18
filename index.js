const express = require('express');
const bodyparser = require('body-parser');
const { createApi } = require('./src/api/index')
const http = require('http');
require('dotenv').config();
const app = express();

/*###################### SETTING ######################*/

app.use(bodyparser.urlencoded({ extended: true, limit: '50mb' }));
app.use(bodyparser.json({ limit: '50mb' }));


/*###################### DEBUG ######################*/
app.use((req, res, next) => {
    let ip;
    if (req.headers['x-forwarded-for']) {
        ip = req.headers['x-forwarded-for'].split(",")[0];
    } else if (req.connection && req.connection.remoteAddress) {
        ip = req.connection.remoteAddress;
    } else {
        ip = req.ip;
    }
    console.log('client IP is', ip.replace(/[:f ]/g, ''));
    console.log(`api is callled %o`, req.originalUrl);
    next();
});
/*###################### CREATE API ######################*/

createApi(app);

const server = http.createServer(app)
server.listen(process.env.PORT, () => {
    console.log(`Server is running port ${process.env.PORT}`)
});

module.exports = server