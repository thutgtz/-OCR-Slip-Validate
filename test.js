const chai = require('chai')
const chaiHttp = require('chai-http')
const expect = chai.expect
require('dotenv').config();
const app = require('./index');

chai.use(chaiHttp);


describe("Check Test", function () {

    describe("Check status api", function () {
        it("check true", function (done) {
            // Send some Form Data
            chai.request(app)
                .get('/check')
                .send({})
                .end(function (err, res) {
                    expect(JSON.stringify(res.body)).to.equal(JSON.stringify({ "message": "สำเร็จจ" }));
                    done();
                });
        });
    });


})