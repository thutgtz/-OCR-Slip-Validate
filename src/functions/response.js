exports.successed = (res, result, message = 'สำเร็จ', status = 200) => res.status(status).send({
    message,
    result
})

exports.failed = (res, error, message = 'ไม่สำเร็จ', status = 400) => res.status(status).send({
    message,
    error
})