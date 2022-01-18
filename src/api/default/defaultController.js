const { slipValidate } = require('./defaultModel')
const { successed, failed } = require('../../functions/response')

class defaultController {

    async slipValidate(req, res) {
        try {
            const { img64, name, date, time } = req.body
            const data = { name, date, time }
            const result = await slipValidate({
                img64,
                data
            })

            successed(res, result)
        } catch (err) {
            failed(res, err)
        }

    }
}

module.exports = new defaultController()