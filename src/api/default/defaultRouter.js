const { Router } = require('express')
const defaultController = require('./defaultController')
const route = Router()

route.post('/slip-validate',
    defaultController.slipValidate
)

route.get('/check',
    defaultController.Check
)

module.exports = route;