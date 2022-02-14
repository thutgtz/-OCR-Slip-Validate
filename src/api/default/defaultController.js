const { slipValidate, ValidateQR } = require('./defaultModel')
const { successed, failed } = require('../../functions/response')
const fs = require('fs')

class defaultController {

    async slipValidate(req, res) {
        try {
            const { img64, dst, dst_acc, date, money, reference } = req.body
            const data = { reference, date, money, dst, dst_acc }
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


    async ValidateQR(req, res) {
        try {
            const { img64 } = req.body
            const result = await ValidateQR({
                img64
            })
            successed(res, JSON.parse(result || "[]"))
        } catch (err) {
            console.log(err)
            failed(res, err)
        }
    }

    async Check(req, res) {
        successed(res, { v: 'dev2' })

    }
}

module.exports = new defaultController()