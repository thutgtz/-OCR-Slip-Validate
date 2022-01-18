const defaultRouter = require('./default/defaultRouter');

exports.createApi = (app) => {
    app.use('', defaultRouter);
};
