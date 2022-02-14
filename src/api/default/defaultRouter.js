const { Router } = require('express')
const defaultController = require('./defaultController')
const route = Router()

route.post('/slip-validate',
    defaultController.slipValidate
)
route.post('/validate-QRcode',
    defaultController.ValidateQR
)
route.get('/check',
    defaultController.Check
)

module.exports = route;