const { slipValidate } = require('./defaultModel')
const { successed, failed } = require('../../functions/response')

class defaultController {

    async slipValidate(req, res) {
        try {
            const { img64, name, date, time, money } = req.body
            const data = { name, date, time, money }
            const result = await slipValidate({
                img64,
                data
            })
            successed(res, JSON.parse(result || "[]"))
        } catch (err) {
            console.log(err)
            failed(res, err)
        }
    }

    async Check(req, res) {
        successed(res, { v: 'dev' })

    }
}

module.exports = new defaultController()