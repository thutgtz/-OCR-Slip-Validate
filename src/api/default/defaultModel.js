const { PythonShell } = require('python-shell')
const path = require('path')

exports.slipValidate = (obj) => new Promise(async (resolve, reject) => {
    const script = new PythonShell(
        path.join(__dirname, '../../../scripts/slipvalidate.py'),
        { mode: 'text' }
    )
    script.send(JSON.stringify(obj));
    script.on('message', (message) => {
        if (message.slice(0, 4) == 'JSON') resolve(message);
    })
    script.end((err) => reject(err || ''));
})